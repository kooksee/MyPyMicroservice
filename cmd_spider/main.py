# -*- coding:utf-8 -*-

import atexit
import sys
import traceback
from os.path import dirname as pdir, abspath
from signal import signal, SIGTERM, SIGINT, SIGQUIT
sys.path.append(pdir(pdir(abspath(__file__))))

import zerorpc




def term_sig_handler(signum, frame):
    print 'catched singal: %d' % signum, frame
    sys.exit(0)


@atexit.register
def atexit_fun():
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_tb)


if __name__ == '__main__':

    signal(SIGTERM, term_sig_handler)
    signal(SIGINT, term_sig_handler)
    signal(SIGQUIT, term_sig_handler)

    import argparse

    parser = argparse.ArgumentParser(description='project service')
    parser.add_argument('-p', action="store", default=6001, type=int, dest='port', help='project port default 6001')
    parser.add_argument('-debug', action="store", default=True, type=bool, dest='debug', help='debug default true')
    parser.add_argument('-daemon', action="store", default=False, type=bool, dest='daemon', help='daemon default false')
    p = parser.parse_args()

    if p.debug:
        print p

    if p.daemon:
        from misc import daemonize

        daemonize()

    from cmd_spider.service.cmd_handle import CmdHandle

    s = zerorpc.Server(CmdHandle())
    s.bind("tcp://0.0.0.0:{}".format(p.port))
    s.debug = True
    s.run()
