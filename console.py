# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   console.py
@Time  :   2020/12/24 16:36:36
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import os
import sys
import argparse
from lib.option import initOption
from config.config import pyVersion, urlVersion
from config.data import logger


def version_check():
    if pyVersion < "3.7.3":
        logger.error(
            "此Python版本 ('{0}') 不兼容,成功运行Glass你必须使用版本 >= 3.7.3 (访问 ‘https://www.python.org/downloads/’)".format(pyVersion))
        exit(0)

    if urlVersion > "1.25.8" and pyVersion > "3.8":
        logger.error("urllib3库版本 ('{0}') 不兼容，代理容易出错".format(urlVersion))
        logger.info('运行 (python3 -m pip install -U "urllib3==1.25.8") 进行库降低版本')
        logger.info(
            "或者运行 (python3 -m pip install -r requirements.txt) 进行全部库的安装")
        exit(0)


def modulePath():
    """
    This will get us the program's directory, even if we are frozen
    using py2exe
    """

    try:
        _ = sys.executable if hasattr(sys, "frozen") else __file__
    except NameError:
        _ = inspect.getsourcefile(modulePath)

    return os.path.dirname(os.path.realpath(_))


def main():
    version_check()
    parser = argparse.ArgumentParser(description="Glass scan.")
    parser.add_argument('-i', '--ip', type=str,
                        dest='ip', help='Input your ip.')
    parser.add_argument('-f', '--file', type=str,
                        dest='file', help='Input your ips.txt.')
    parser.add_argument('-u', '--url', type=str,
                        dest='url', help='Input your url.')
    parser.add_argument('-w', '--web', type=str,
                        dest='web', help='Input your webs.txt.')
    parser.add_argument('--proxy', type=str, dest='proxy',
                        help='Input your proxy options(all or cn) or proxy address(127.0.0.1:8080).')
    parser.add_argument('--proxy-list', type=str,
                        dest='proxylist', help='List the proxys.')
    parser.add_argument('-v', '--version', dest='version',
                        action='store_true', help="Show program's version number and exit.")
    parser.add_argument('--update', dest='updateprogram',
                        action='store_true', help="Update the program.")
    parser.add_argument('-o', '--output', type=str,
                        dest='outputTarget', help='Select the output format.')
    parser.add_argument('-s', '--search', type=str,
                        dest='search', help='Choose your search engine.')
    args = parser.parse_args()
    usage = '''
Usage: python3 {} -i 127.0.0.1 or 127.0.0.0/24
Usage: python3 {} -u 127.0.0.1 -s eye or fofa
Usage: python3 {} -f ips.txt
Usage: python3 {} -u https://96.mk/
Usage: python3 {} -w webs.txt
Usage: python3 {} --proxy-list all or cn
Usage: python3 {} (-i -f -u -w) 127.0.0.1 or 127.0.0.0/24 --proxy all or cn
Usage: python3 {} --update
Usage: python3 {} -u https://96.mk/ -o html
    '''.format(parser.prog, parser.prog, parser.prog, parser.prog, parser.prog, parser.prog, parser.prog, parser.prog, parser.prog)
    root = modulePath()
    initOption(usage, root, args.__dict__)
