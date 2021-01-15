# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   log.py
@Time  :   2021/01/11 11:51:44
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import sys
import logging
from config.colors import mkPut
from colorama import init


class LoggingLevel:
    SUCCESS = 9
    SYSINFO = 8
    ERROR = 7
    WARNING = 6


init(autoreset=True)

logging.addLevelName(LoggingLevel.SUCCESS, mkPut.cyan("[+]"))
logging.addLevelName(LoggingLevel.SYSINFO, mkPut.green("[INFO]"))
logging.addLevelName(LoggingLevel.ERROR, mkPut.red("[ERROR]"))
logging.addLevelName(LoggingLevel.WARNING, mkPut.yellow("[WARNING]"))

LOGGER = logging.getLogger("GlassLog")

formatter = logging.Formatter(
    "%(asctime)s %(levelname)s %(message)s",
    datefmt=mkPut.fuchsia("[%H:%M:%S]")
)
LOGGER_HANDLER = logging.StreamHandler(sys.stdout)
LOGGER_HANDLER.setFormatter(formatter)
LOGGER.addHandler(LOGGER_HANDLER)
LOGGER.setLevel(LoggingLevel.WARNING)


class MY_LOGGER:
    def info(msg):
        return LOGGER.log(LoggingLevel.SYSINFO, msg)

    def error(msg):
        return LOGGER.log(LoggingLevel.ERROR, msg)

    def warning(msg):
        return LOGGER.log(LoggingLevel.WARNING, msg)

    def success(msg):
        return LOGGER.log(LoggingLevel.SUCCESS, msg)


# MY_LOGGER.info("TEST")
