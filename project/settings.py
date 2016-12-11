# -*- coding:utf-8 -*-

import logging

from misc.common_settings import logs, databases, protocols

project_thrift = protocols("project.thrift")
DB_PATH = databases("project.db")
logging.basicConfig(
    filename=logs('project.log'),
    format='[%(asctime)-15s] [%(processName)s:%(process)d] %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.INFO
)
