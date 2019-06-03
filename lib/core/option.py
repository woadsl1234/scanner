from lib.core.log import MY_LOGGER
from lib.core.data import conf
import os,sys

def Options(args):
    init()
    _ = args.__dict__.items()
    for key, value in _:
        conf[key] = value

    if conf.domain:
        MY_LOGGER.info("start domain search")
        # subdomain()
        pass
    sys.exit(0)

def init():
    _initconf()

def _initconf():
    conf.mutiurl = []
    with open('../../dics/domain/domain.txt') as f:
        conf.sub = f.readlines()
    conf.process = 5

def pluginScan(args):
    pass

if __name__ == '__main__':
    pass