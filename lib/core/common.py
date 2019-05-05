import sys
import collections
from thirdparty import six
from lib.core.settings import UNICODE_ENCODING, STDIN_PIPE_DASH
from lib.core.data import kb,conf,paths
from lib.core.exception import SqlmapSystemException
from lib.core.bigarray import BigArray
from termcolor import colored
import os

def dataToStdout(data, forceOutput=False, bold=False, content_type=None):
    """
    Writes text to the stdout (console) stream
    """

    message = data
    sys.stdout.write(colored(message, "cyan"))
    try:
        sys.stdout.flush()
    except IOError:
        pass

def setPaths(rootPath):
    """
    Sets absolute paths for project directories and files
    """

    paths.ROOT_PATH = rootPath
    # paths
    paths.PLUGIN_PATH = os.path.join(paths.ROOT_PATH, "plugin")
    paths.SETTINGS_PATH = os.path.join(paths.ROOT_PATH, "lib", "core", "settings.py")
    paths.DICS_PATH = os.path.join(paths.ROOT_PATH, "dics")
    # print(paths.values())
    for path in paths.values():
        if any(path.endswith(_) for _ in (".txt", ".xml", ".zip")):
            checkFile(path)

def checkFile(filename, raiseOnError=True):
    """
    Checks for file existence and readability

    >>> checkFile(__file__)
    True
    """

    valid = True

    if filename:
        filename = filename.strip('"\'')

    if filename == STDIN_PIPE_DASH:
        return checkPipedInput()
    else:
        try:
            if filename is None or not os.path.isfile(filename):
                valid = False
        except:
            valid = False

        if valid:
            try:
                with open(filename, "rb"):
                    pass
            except:
                valid = False

    if not valid and raiseOnError:
        raise SqlmapSystemException("unable to read file '%s'" % filename)

    return valid

def weAreFrozen():
    """
    Returns whether we are frozen via py2exe.
    This will affect how we find out where we are located.

    # Reference: http://www.py2exe.org/index.cgi/WhereAmI
    """

    return hasattr(sys, "frozen")

def getUnicode(value, encoding=None, noneToNull=False):
    """
    Return the unicode representation of the supplied value:

    >>> getUnicode('test') == u'test'
    True
    >>> getUnicode(1) == u'1'
    True
    """

    if noneToNull and value is None:
        return "NULL"

    if isinstance(value, six.text_type):
        return value
    elif isinstance(value, six.binary_type):
        # Heuristics (if encoding not explicitly specified)
        candidates = filterNone((encoding, kb.get("pageEncoding") if kb.get("originalPage") else None, conf.get("encoding"), UNICODE_ENCODING, sys.getfilesystemencoding()))
        if all(_ in value for _ in (b'<', b'>')):
            pass
        elif any(_ in value for _ in (b":\\", b'/', b'.')) and b'\n' not in value:
            candidates = filterNone((encoding, sys.getfilesystemencoding(), kb.get("pageEncoding") if kb.get("originalPage") else None, UNICODE_ENCODING, conf.get("encoding")))
        elif conf.get("encoding") and b'\n' not in value:
            candidates = filterNone((encoding, conf.get("encoding"), kb.get("pageEncoding") if kb.get("originalPage") else None, sys.getfilesystemencoding(), UNICODE_ENCODING))

        for candidate in candidates:
            try:
                return six.text_type(value, candidate)
            except UnicodeDecodeError:
                pass

        try:
            return six.text_type(value, encoding or (kb.get("pageEncoding") if kb.get("originalPage") else None) or UNICODE_ENCODING)
        except UnicodeDecodeError:
            return six.text_type(value, UNICODE_ENCODING, errors="reversible")
    elif isListLike(value):
        value = list(getUnicode(_, encoding, noneToNull) for _ in value)
        return value
    else:
        try:
            return six.text_type(value)
        except UnicodeDecodeError:
            return six.text_type(str(value), errors="ignore")  # encoding ignored for non-basestring instances

def filterNone(values):
    """
    Emulates filterNone([...]) functionality

    >>> filterNone([1, 2, "", None, 3])
    [1, 2, 3]
    """

    retVal = values

    if isinstance(values, collections.Iterable):
        retVal = [_ for _ in values if _]

    return retVal

def isListLike(value):
    """
    Returns True if the given value is a list-like instance

    >>> isListLike([1, 2, 3])
    True
    >>> isListLike('2')
    False
    """

    return isinstance(value, (list, tuple, set, BigArray))


def checkPipedInput():
    """
    Checks whether input to program has been provided via standard input (e.g. cat /tmp/req.txt | python sqlmap.py -r -)
    # Reference: https://stackoverflow.com/a/33873570
    """

    return not os.isatty(sys.stdin.fileno())