#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from lib.core.enums import CUSTOM_LOGGING

logging.addLevelName(CUSTOM_LOGGING.SYSINFO, "INFO")
logging.addLevelName(CUSTOM_LOGGING.SUCCESS, "SUCCESS")
logging.addLevelName(CUSTOM_LOGGING.ERROR, "ERROR")
logging.addLevelName(CUSTOM_LOGGING.WARNING, "WARNING")
logging.addLevelName(CUSTOM_LOGGING.DEBUG, "DEBUG")
LOGGER = logging.getLogger("TookitLogger")

LOGGER_HANDLER = None

from thirdparty.ansistrm.ansistrm import ColorizingStreamHandler

LOGGER_HANDLER = ColorizingStreamHandler(sys.stdout)
LOGGER_HANDLER.level_map[logging.getLevelName("INFO")] = (None, "cyan", False)
LOGGER_HANDLER.level_map[logging.getLevelName("SUCCESS")] = (None, "green", False)
LOGGER_HANDLER.level_map[logging.getLevelName("ERROR")] = (None, "red", False)
LOGGER_HANDLER.level_map[logging.getLevelName("WARNING")] = (None, "yellow", False)
LOGGER_HANDLER.level_map[logging.getLevelName("DEBUG")] = (None, "white", False)


FORMATTER = logging.Formatter("\r[%(levelname)s] %(message)s", "%H:%M:%S")

LOGGER_HANDLER.setFormatter(FORMATTER)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(CUSTOM_LOGGING.WARNING)


class MY_LOGGER:
    @staticmethod
    def success(msg):
        return LOGGER.log(CUSTOM_LOGGING.SUCCESS, msg)

    @staticmethod
    def info(msg):
        return LOGGER.log(CUSTOM_LOGGING.SYSINFO, msg)

    @staticmethod
    def warning(msg):
        return LOGGER.log(CUSTOM_LOGGING.WARNING, msg)

    @staticmethod
    def error(msg):
        return LOGGER.log(CUSTOM_LOGGING.ERROR, msg)

    @staticmethod
    def critical(msg):
        return LOGGER.log(CUSTOM_LOGGING.ERROR, msg)

    @staticmethod
    def debug(msg):
        return LOGGER.log(CUSTOM_LOGGING.DEBUG, msg)

    @staticmethod
    def security_note(msg, k=''):
        MY_LOGGER.info(msg)

    @staticmethod
    def security_warning(msg, k=''):
        MY_LOGGER.warning(msg)

    @staticmethod
    def security_hole(msg, k=''):
        MY_LOGGER.success(msg)

    @staticmethod
    def security_info(msg, k=''):
        MY_LOGGER.info(msg)

