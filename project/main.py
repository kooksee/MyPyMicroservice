# -*- coding:utf-8 -*-
import argparse
import atexit
import sys
import traceback
from signal import signal, SIGTERM, SIGINT, SIGQUIT

from project.settings import project_thrift


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

    parser = argparse.ArgumentParser(description='project service')
    parser.add_argument('-p', action="store", default=6000, type=int, dest='port', help='project port default 6000')
    parser.add_argument('-debug', action="store", default=True, type=bool, dest='debug', help='debug default true')
    parser.add_argument('-daemon', action="store", default=False, type=bool, dest='daemon', help='daemon default false')
    p = parser.parse_args()

    if p.debug:
        print p

    if p.daemon:
        from misc import daemonize

        daemonize()

    import thriftpy
    from thriftpy.rpc import make_server
    from service.project_handle import ProjectHandle

    project_thrift = thriftpy.load(project_thrift, module_name="project_thrift")
    server = make_server(project_thrift.ProjectHandle, ProjectHandle(), port=p.port)
    server.serve()
