# -*- coding:utf-8 -*-
from tornado import web


class MainHandler(web.RequestHandler):
    def get(self, *args, **kwargs):
        print args,kwargs
        print self.request.body
        print self.request.arguments
        self.write("ok")