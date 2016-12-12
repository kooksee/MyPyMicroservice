# -*- coding:utf-8 -*-

from cmd_spider.settings import url
from controller import MainHandler

handlers = [
    (r"/", MainHandler),
    (r"/test", MainHandler)
]

from cmd_spider.service.cmd_handle import CmdSpiderHandle

# 添加cmd markdown爬虫
handlers += [
    (url('cmd_spiders/?'), CmdSpiderHandle)
]

from controller.project import ProjectsHandler, ProjectsActionHandler, ProjectHandler

# 添加项目路由
handlers += [
    (url('projects/?'), ProjectsHandler),
    (url('projects/actions/?'), ProjectsActionHandler),
    (url('projects/(?P<program>[^/]+)/?'), ProjectHandler),
    (url('projects/(?P<program>[^/]+)/(?P<action>[^/]+)/?'), ProjectHandler)
]

# 添加钩子路由
handlers += [
    (url('hooks/?'), ProjectsHandler),
    (url('hooks/(?P<id>[^/]+)/?'), ProjectsHandler),
]
