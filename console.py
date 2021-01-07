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
import time
import random
from config.config import Banner, OS, tosayRun
from mod.fofa import fmain
from mod.website import mwebs
from mod.rulesCli import ruleInfo
from mod.output import output
from optparse import OptionParser
from config.data import Urls, Paths, WebInfos, OutInfos

Urls.url = []
Paths.root = [os.getcwd()]
WebInfos = {}
OutInfos = {}

if OS == "Windows":
    from colorama import init
    init(autoreset=True)
    Paths.config = [os.getcwd() + '\\config\\']
    Paths.output = [os.getcwd() + '\\output\\']
else:
    Paths.config = [os.getcwd() + '/config/']
    Paths.output = [os.getcwd() + '/output/']

if os.path.isdir(Paths.output[0]):
    pass
else:
    os.mkdir(Paths.output[0])


def main():
    usage = "python3 %prog -i 127.0.0.1 or 127.0.0.0/24\nUsage: python3 %prog -f ips.txt\nUsage: python3 %prog -u http://target/\nUsage: python3 %prog -w webs.txt"
    parser = OptionParser(usage)
    parser.add_option('-i', '--ip', type='string',
                      dest='ip', help='Input your ip.')
    parser.add_option('-f', '--file', type='string',
                      dest='file', help='Input your ips.txt')
    parser.add_option('-u', '--url', type='string',
                      dest='url', help='Input your url.')
    parser.add_option('-w', '--web', type='string',
                      dest='web', help='Input your webs.txt')
    options, args = parser.parse_args()
    ruleInfos = ruleInfo()
    outinfo = output()
    ips = []
    print(random.choice(Banner))
    if tosayRun:
        from config.tosay import todaySay
        print(todaySay())
    if options.ip:
        ips.append(options.ip)
        fmain(ips)
        mwebs()
        ruleInfos.main()
        outinfo.outTxt()
    elif options.file:
        with open(options.file, 'r') as f:
            for ip in f.readlines():
                if len(ip) != 1:
                    ips.append(ip.strip())
        fmain(ips)
        mwebs()
        ruleInfos.main()
        outinfo.outTxt()
    elif options.url:
        Urls.url.append(options.url)
        mwebs()
        ruleInfos.main()
        outinfo.outTxt()
    elif options.web:
        with open(options.web, 'r') as f:
            for web in f.readlines():
                if len(web) != 1:
                    Urls.url.append(web.strip())
            mwebs()
            ruleInfos.main()
            outinfo.outTxt()
    else:
        print(parser.get_usage())


if __name__ == "__main__":
    main()
