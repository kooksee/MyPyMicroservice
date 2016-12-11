# -*- coding:utf-8 -*-
import threading
import time
from subprocess import PIPE

import psutil
from pony.orm import db_session, commit
from pony.orm.serialization import to_dict

from misc import singleton
from project.db.model import Project, Template


class Task(object):
    def __init__(self, **kwargs):
        self.program = kwargs.get("program", None)
        self.is_running = kwargs.get("is_running", False)
        self.numretry = kwargs.get("numretry", 100)
        self.timeout = kwargs.get("timeout", 5)


@singleton
class ProjectTask(object):
    def __init__(self):
        pass

    @db_session
    def start(self, program):
        t = Template[program]
        t.numretry = 30
        if not t.is_running:
            t.is_running = 1
            commit()
            threading.Thread(target=self._start, args=(program,)).start()
        else:
            from pony.orm import select
            for p in select(p for p in Project if p.program == program)[:]:
                if p.pid == 0:
                    threading.Thread(target=self._start, args=(program,)).start()

    def _start(self, program):
        while self.__start(program):
            pass

    @db_session
    def __start(self, program):
        print "Task: {0}\n".format(program)

        t = Template[program]
        if not t.is_running:
            return

        if t.numretry <= 0:
            t.is_running = 0
            return

        if __debug__:
            print to_dict(t)
        t.numretry -= 1
        self.timeout = t.timeout

        self.__start_callback(program)

        time.sleep(self.timeout)

        return True

    @db_session
    def __start_callback(self, program):
        from pony.orm import select
        for p in select(p for p in Project if p.program == program)[:]:
            try:
                pid = p.pid
                if pid and psutil.Process(p.pid).is_running():
                    continue
                else:
                    raise psutil.NoSuchProcess(pid)
            except psutil.NoSuchProcess:
                self.____start_callback(p.command, p.id)
                # threading.Thread(target=self.__start_callback, args=(p.command, p.id)).start()

    @db_session
    def ____start_callback(self, command, id):
        # daemonize()
        pp = psutil.Popen(command, stdout=PIPE, shell=True)
        Project[id].pid = pp.pid
        print "重新启动{0}:{1}".format(pp.name(), pp.pid)

    @db_session
    def stop(self, program):
        t = Template[program]
        t.numretry = 0
        if t.is_running:
            t.is_running = 0
            threading.Thread(target=self._stop, args=(program,)).start()

    @db_session
    def _stop(self, program):
        from pony.orm import select
        for p in select(p for p in Project if p.program == program)[:]:
            try:
                if p.pid and psutil.Process(p.pid).is_running():
                    _p = psutil.Process(p.pid)
                    _p.kill()
                    _p.wait()
                    raise psutil.NoSuchProcess(p.pid)
                else:
                    raise psutil.NoSuchProcess(p.pid)
            except psutil.NoSuchProcess:
                self.__kill(p.id)
                # threading.Thread(target=self.__kill, args=(p.id,)).start()

    @db_session
    def __kill(self, pid):
        Project[pid].set(pid=0)

    def restart(self, program):
        self._stop(program)
        self.start(program)
