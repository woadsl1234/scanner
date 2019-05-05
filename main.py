# -*- coding:utf-8 -*-
import sys,os
import random
from termcolor import colored
from lib.core.config import banners
from lib.core.option import Options
from lib.core.common import weAreFrozen, setPaths, dataToStdout
import inspect
from lib.core.settings import UNICODE_ENCODING
from lib.core.common import getUnicode
from lib.core.data import logger
from lib.parse.Parameter import Parameter

def modulePath():
    """
    This will get us the program's directory, even if we are frozen
    using py2exe
    """

    try:
        _ = sys.executable if weAreFrozen() else __file__
    except NameError:
        _ = inspect.getsourcefile(modulePath)

    return getUnicode(os.path.dirname(os.path.realpath(_)), encoding=sys.getfilesystemencoding() or UNICODE_ENCODING)

def checkEnvironment():
    try:
        os.path.isdir(modulePath())
    except UnicodeEncodeError:
        errMsg = "your system does not properly handle non-ASCII paths. "
        errMsg += "Please move the sqlmap's directory to the other location"
        logger.critical(errMsg)
        raise SystemExit


if __name__ == '__main__':

    checkEnvironment()
    setPaths(modulePath())
    dataToStdout(banners[random.randint(0, 2)])
    try:
        Options(Parameter())
    except KeyboardInterrupt:
        print(colored("Ctrl C - Stopping Client", "red"))
        sys.exit(1)
