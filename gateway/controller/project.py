# -*- coding:utf-8 -*-
import functools
import json
import logging

import thriftpy
from thriftpy.rpc import make_client
from tornado import web

from gateway.settings import project_thrift, project

logger = logging.getLogger()


class ProjectClient(object):
    def __init__(self):
        self.project = self.get_client()

    def get_client(self, numretry=3):
        _numretry = numretry

        while _numretry > 0:
            try:
                p = make_client(
                    thriftpy.load(project_thrift,
                                  module_name="project_thrift").ProjectHandle,
                    port=project["port"])
                res = p.ping()
                if res == 'ok':
                    return p
            except Exception, e:
                logger.error(e.message)
                _numretry -= 1
        else:
            logger.error("had retried {} times, but still error".format(numretry))
            return

    def add_projects(self, data):
        self.project = self.project or self.get_client()
        res = self.project.add_projects(data)
        return res

    def remove_projects(self, data):
        self.project = self.project or self.get_client()
        res = self.project.remove_projects(data)
        return res

    def get_projects(self, data):
        self.project = self.project or self.get_client()
        res = self.project.get_projects(data)
        return res

    def update_project(self, data):
        self.project = self.project or self.get_client()
        res = self.project.update_project(data)
        return res

    def do_actions(self, data):
        res = self.project.do_actions(data)
        return res


class ProjectsHandler(web.RequestHandler):
    project = ProjectClient()

    def post(self, *args, **kwargs):

        if __debug__:
            print self.request.body

        body = json.loads(self.request.body)
        if not isinstance(body, list):
            return self.write(json.dumps(dict(
                status="fail",
                msg=u"参数不正确"
            )))
        self.write(self.project.add_projects(self.request.body))

    def delete(self, *args, **kwargs):

        if __debug__:
            print self.request.body

        body = json.loads(self.request.body)
        self.write(self.project.remove_projects(
            json.dumps(body.get("programs", []))
        ))

    def get(self, *args, **kwargs):

        programs = self.get_argument("programs", "")
        programs = [] if not programs else programs.split(";")
        fields = self.get_argument("fields", [])

        if __debug__:
            print programs, fields

        self.write(self.project.get_projects(json.dumps(dict(
            programs=programs,
            fields=fields
        ))))


class ProjectsActionHandler(web.RequestHandler):
    project = ProjectClient()

    def post(self, *args, **kwargs):
        self.write(self.project.do_actions(json.dumps(dict(
            programs=self.get_argument("programs", []),
            actions=self.get_argument("actions", [])
        ))))


class ProjectHandler(web.RequestHandler):
    project = ProjectClient()

    def put(self, *args, **kwargs):
        # program = kwargs.get("program")
        body = json.loads(self.request.body)
        self.write(self.project.update_project(
            json.dumps(body)
        ))

    def post(self, *args, **kwargs):
        program = kwargs.get("program", None)
        action = kwargs.get("action", None)
        d = json.dumps(dict(
            programs=[program, ],
            actions=self.get_argument("actions", [action, ])
        ))

        if __debug__:
            print kwargs
            print d

        self.write(self.project.do_actions(d))
        self.finish()


if __name__ == '__main__':
    pass


def retry(cls, numretry=3):
    def _func(func):
        @functools.wraps(func)
        def __func(*args, **kwargs):
            cls.project = make_client(
                thriftpy.load(project_thrift,
                              module_name="project_thrift").ProjectHandle,
                port=project["port"])

            _numretry = numretry
            while _numretry > 0:
                try:
                    res = cls.project.ping()
                    if res == 'ok':
                        logger.info('calling function: {}\n'.format(func.__name__))
                        res1 = func(*args, **kwargs)
                        logger.info('return value: {}\n'.format(res1))
                        return res1
                except Exception, e:
                    logger.error(e.message)

                    cls.project = make_client(
                        thriftpy.load(project_thrift,
                                      module_name="project_thrift").ProjectHandle,
                        port=project["port"])
                    _numretry -= 1
            else:
                logger.error("had retried {} times, but still error".format(numretry))
                return

        return __func

    return _func
