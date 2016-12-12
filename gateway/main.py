# -*- coding:utf-8 -*-

import argparse
import atexit
import sys
import traceback
from os.path import dirname as pdir, abspath
from signal import signal, SIGTERM, SIGINT, SIGQUIT

sys.path.append(pdir(pdir(abspath(__file__))))

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

from misc import singleton, daemonize


@singleton
class AppManager(object):
    def __init__(self):
        self.app = None

    def start(self, option):

        if __debug__:
            print option

        from gateway import JmonitorApplication
        self.app = JmonitorApplication({
            "debug": option.debug
        })

        HTTPServer(self.app).listen(option.port)
        loop = IOLoop.instance()
        try:
            loop.start()
        except KeyboardInterrupt:
            print(" Shutting down on SIGINT!")
            loop.stop()
            traceback.format_exc()
        finally:
            pass

    def get_app(self):
        return self.app


def term_sig_handler(signum, frame):
    print 'catched singal: %d' % signum, frame
    sys.exit(0)


@atexit.register
def atexit_fun():
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)


if __name__ == "__main__":

    signal(SIGTERM, term_sig_handler)
    signal(SIGINT, term_sig_handler)
    signal(SIGQUIT, term_sig_handler)

    parser = argparse.ArgumentParser(description='gateway service')
    parser.add_argument('-p', action="store", default=6752, type=int, dest='port', help='port default 6752')
    parser.add_argument('-debug', action="store", default=True, type=bool, dest='debug', help='debug default true')
    parser.add_argument('-daemon', action="store", default=False, type=bool, dest='daemon', help='daemon default false')
    p = parser.parse_args()

    if p.daemon:
        daemonize()

    print "http://{}:{}".format("localhost", p.port)

    AppManager().start(p)
