# -*- coding:utf-8 -*-
from tornado import web


class TodosApplication(web.Application):
    def __init__(self, config):
        from todos.settings import settings
        from todos.urls import handlers

        self.tasks = {}
        settings.update(config)

        super(TodosApplication, self).__init__(handlers, **settings)
