# -*- coding:utf-8 -*-

import os
import socket
import sys


def daemonize():
    try:
        # this process would create a parent and a child
        pid = os.fork()
        if pid > 0:
            # take care of the first parent
            sys.exit(0)
    except OSError, err:
        sys.stderr.write("Fork 1 has failed --> %d--[%s]\n" % (err.errno,
                                                               err.strerror))
        sys.exit(1)

    # change to root
    os.chdir('/')
    # detach from terminal
    os.setsid()
    # file to be created ?
    os.umask(0)
    try:
        # this process creates a parent and a child
        pid = os.fork()
        if pid > 0:
            print "Daemon process pid %d" % pid
            # bam
            sys.exit(0)
    except OSError, err:
        sys.stderr.write("Fork 2 has failed --> %d--[%s]\n" % (err.errno,
                                                               err.strerror))
        sys.exit(1)

    sys.stdout.flush()
    sys.stderr.flush()


def daemonize1(stdout='/dev/null', stderr=None, stdin='/dev/null',
               pidfile=None, startmsg='started with pid %s'):
    '''''
         This forks the current process into a daemon.
         The stdin, stdout, and stderr arguments are file names that
         will be opened and be used to replace the standard file descriptors
         in sys.stdin, sys.stdout, and sys.stderr.
         These arguments are optional and default to /dev/null.
        Note that stderr is opened unbuffered, so
        if it shares a file with stdout then interleaved output
         may not appear in the order that you expect.
     '''
    # flush io
    sys.stdout.flush()
    sys.stderr.flush()
    # Do first fork.
    try:
        pid = os.fork()
        if pid > 0: sys.exit(0)  # Exit first parent.
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # Decouple from parent environment.
    os.chdir("/")
    os.umask(0)
    os.setsid()
    # Do second fork.
    try:
        pid = os.fork()
        if pid > 0: sys.exit(0)  # Exit second parent.
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s\n" % (e.errno, e.strerror))
        sys.exit(1)
    # Open file descriptors and print start message
    if not stderr: stderr = stdout
    si = file(stdin, 'r')
    so = file(stdout, 'a+')
    se = file(stderr, 'a+', 0)  # unbuffered
    pid = str(os.getpid())
    sys.stderr.write("\n%s\n" % startmsg % pid)
    sys.stderr.flush()
    if pidfile: file(pidfile, 'w+').write("%s\n" % pid)
    # Redirect standard file descriptors.
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())


def get_host_ip():
    myname = socket.getfqdn(socket.gethostname())
    return socket.gethostbyname(myname)


def gen_fields(name, fields):
    if not fields:
        return name

    return ",".join(["{0}.{1}".format(name, p) for p in fields])


def singleton(cls):
    instances = {}

    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


if __name__ == '__main__':
    print get_host_ip()  # 主机ip地址

    # print gen_fields("ss", ["dd", "dffff"])
