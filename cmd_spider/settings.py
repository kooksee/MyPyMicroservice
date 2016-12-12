# -*- coding:utf-8 -*-

import logging
from os.path import join as pjoin

from misc.common_settings import logs, databases

DB_PATH = pjoin(databases, 'cmd_spider.json')
BASE_BLOG_PAGE = 'https://www.zybuluo.com/bergus/note/588035'
logging.basicConfig(
    filename=logs('project.log'),
    format='[%(asctime)-15s] [%(processName)s:%(process)d] %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.INFO
)
