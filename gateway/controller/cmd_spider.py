# -*- coding:utf-8 -*-

import zerorpc
from tornado import web

from gateway.settings import logger


class CmdSpiderClient(object):
    def __init__(self):
        self.client = self.get_client()

    def get_client(self, numretry=3):
        _numretry = numretry

        while _numretry > 0:
            try:
                c = zerorpc.Client()
                c.connect("tcp://127.0.0.1:{}".format(6001))
                res = c.ping()
                if res == 'ok':
                    print res
                    return c
            except Exception, e:
                logger.error(e.message)
                _numretry -= 1
        else:
            logger.error("had retried {} times, but still error".format(numretry))
            return

    def spider(self, *blog_urls):
        c = self.client or self.get_client()
        return c.spider(blog_urls)

    def get_tags(self, *tags):
        c = self.client or self.get_client()
        return c.get_tags(tags)

    def get_headers(self, *urls):
        c = self.client or self.get_client()
        return c.get_headers(urls)


class CmdSpiderHandle(web.RequestHandler):
    c = CmdSpiderClient()

    def post(self, *args, **kwargs):
        self.write(self.c.spider(self.get_body_argument("blog_urls", [])))

    def get(self, *args, **kwargs):
        tags = self.get_argument("tags", [])
        headers = self.get_argument("headers", [])

        if tags:
            self.write(self.c.get_tags(tags))
            self.finish()

        if headers:
            self.write(self.c.get_headers(headers))
            self.finish()

        self.write(dict(
            status="fail",
            msg="参数错误"
        ))


if __name__ == '__main__':
    # c = CmdSpiderClient()
    # print c.hello()

    c = zerorpc.Client()
    c.connect("tcp://127.0.0.1:{}".format(6001))
    res = c.ping()
    print res
