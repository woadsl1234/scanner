# -*- coding:utf-8 -*-
import argparse
import sys,os
import random
from termcolor import colored
from lib.config import banners
from lib.core.option import Options

def run(args):
    pass

if __name__ == '__main__':
    sys.path.append(os.path.abspath(os.path.join(os.getcwd(), "..")))  # 当前项目路径加入

    parser = argparse.ArgumentParser(description="scanner v1.0 ckj123")
    parser.add_argument("-d","--domain",metavar="",
        help="domain name")
    args = parser.parse_args()
    print(banners[random.randint(0,2)])
    Options(args)
    try:
        run(args)
    except KeyboardInterrupt:
        print(colored("Ctrl C - Stopping Client","red"))
        sys.exit(1)