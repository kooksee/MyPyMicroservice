# -*- coding:utf-8 -*-

from controller import MainHandler
from controller.project import ProjectsHandler, ProjectsActionHandler, ProjectHandler

handlers = [
    (r"/", MainHandler),
    (r"/test", MainHandler),
    (r"/api/projects/?", ProjectsHandler),
    (r"/api/projects/actions/?", ProjectsActionHandler),
    (r"/api/projects/(?P<program>[^/]+)/?", ProjectHandler),
    (r"/api/projects/(?P<program>[^/]+)/(?P<action>[^/]+)/?", ProjectHandler),
]

# 添加对钩子的支持
handlers += [
    (r"/api/hooks/?", ProjectsHandler),
    (r"/api/hooks/(?P<id>[^/]+)/?", ProjectsHandler),
]
