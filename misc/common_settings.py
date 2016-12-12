# -*- coding:utf-8 -*-

import sys
from os.path import dirname as pdir
from os.path import join as pjoin

ROOT_PATH = pdir(pdir(__file__))
sys.path.append(ROOT_PATH)

reload(sys)
sys.setdefaultencoding('utf-8')

files = pjoin(ROOT_PATH, 'files')


def __logs(log_path=None):
    return pjoin(files, 'logs', 'default.logs' if not log_path else log_path)


def __dbs(db_path=None):
    return pjoin(files, 'databases', 'default.db' if not db_path else db_path)


def __protocols(db_protocol=None):
    return pjoin(files, 'protocols', 'default.thrift' if not db_protocol else db_protocol)


logs = __logs
databases = __dbs
protocols = __protocols

if __name__ == '__main__':
    print pdir(pdir(__file__))
    print sys.path
