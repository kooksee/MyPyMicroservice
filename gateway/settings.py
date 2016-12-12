# -*- coding:utf-8 -*-
import logging
from os.path import join as pjoin

from misc.common_settings import logs, ROOT_PATH, protocols

numretry = 3

logging.basicConfig(
    filename=logs('gateway.log'),
    format='[%(asctime)-15s] [%(processName)s:%(process)d] %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()

settings = dict(
    template_path=pjoin(ROOT_PATH, 'gateway', "templates"),
    static_path=pjoin(ROOT_PATH, 'gateway', "static"),
    xsrf_cookies=False,
    cookie_secret="jlogCFF@#$%^&*()(*^fcxfgs3245$#@$%^&*();'><,.<>FDRYTH$#$^%^&jlog",
    debug=False,
)

project = {
    "port": 6000,
    "host": "localhost",
}

project_thrift = protocols("project.thrift")

if __name__ == '__main__':
    pass
