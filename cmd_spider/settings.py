# -*- coding:utf-8 -*-

import logging
import urlparse
from os.path import dirname as pdir

ROOT_PATH = pdir(pdir(__file__))

from misc.common_settings import databases, logs

DB_PATH = databases('cmd_spider.db')
BASE_BLOG_PAGE = 'https://www.zybuluo.com/bergus/note/588035'
logging.basicConfig(
    filename=logs('cmd_spider.log'),
    format='[%(asctime)-15s] [%(processName)s:%(process)d] %(name)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger()

prefix = '/v1/api/'


def __url(url=None):
    return urlparse.urljoin(prefix, url)


url = __url


if __name__ == '__main__':
    print url("dldd")
    print url("/dldd")
    print url("dldd/?sdd")