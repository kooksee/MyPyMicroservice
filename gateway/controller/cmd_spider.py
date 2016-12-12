# -*- coding:utf-8 -*-
import logging

import zerorpc

logger = logging.getLogger()


class CmdSpiderClient(object):
    def __init__(self):
        self.project = self.get_client()

    def get_client(self, numretry=3):
        _numretry = numretry

        while _numretry > 0:
            try:
                c = zerorpc.Client()
                c.connect("tcp://127.0.0.1:{}".format(6001))
                res = c.ping()
                if res == 'ok':
                    return c
            except Exception, e:
                logger.error(e.message)
                _numretry -= 1
        else:
            logger.error("had retried {} times, but still error".format(numretry))
            return

    def hello(self):
        c = self.project or self.get_client()
        return c.hello("RPC")
