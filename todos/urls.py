# -*- coding:utf-8 -*-

from controller import MainHandler, HealthCheckHandler

handlers = [
    (r"/", MainHandler),
    (r"/health", HealthCheckHandler)
]

# 添加路由
from todos.controller.todos_handle import TodoHandler, TodosHandler

handlers += [
    ('/api/todos/?', TodosHandler),
    ('/api/todos/(?P<id>[^/]+)/?', TodoHandler),
]
