from lib.core.log import MY_LOGGER
from lib.core.data import conf
from lib.subdomain.subdomain import subdomain
import os,sys

def Options(args):
    init()
    _ = args.__dict__.items()
    for key, value in _:
        conf[key] = value

    if conf.domain:
        MY_LOGGER.info("start domain search")
        subdomain(args.domain, conf.process, args.domains).run()

    sys.exit(0)

def init():
    _initconf()

def _initconf():
    conf.mutiurl = []
    conf.process = 20

def pluginScan(args):
    pass

if __name__ == '__main__':
    pass