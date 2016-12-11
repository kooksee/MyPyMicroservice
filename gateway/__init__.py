# -*- coding:utf-8 -*-
from tornado import web


class JmonitorApplication(web.Application):
    def __init__(self, config):
        from gateway.settings import settings
        from gateway.urls import handlers

        self.tasks = {}
        settings.update(config)

        super(JmonitorApplication, self).__init__(handlers, **settings)
