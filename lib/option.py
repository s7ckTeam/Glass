# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   option.py
@Time  :   2021/01/09 17:56:34
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import os
import sys
import random
import prettytable as pt
from mod.fofa import fmain
from mod.zoomeye import zmain
from mod.quake import qmain
from mod.website import mwebs
from mod.rulesCli import ruleMain
from mod.output import outMain
from lib.proxy import checkProxyFile
from lib.update import update
from lib.common import getScheme
from colorama import init as wininit
from config.config import Version, tosayRun, Banner, fofaApi, zoomeyeApi
from config.data import Urls, Paths, WebInfos, OutInfos, Proxys, confs, logger


def initOption(usage, root, args):
    wininit(autoreset=True)
    datas_init()
    set_path(root)
    program_start(usage)
    confs_init()
    add_options(args)
    set_confs()
    runmod()


def add_options(cmdparse):
    if hasattr(cmdparse, "items"):
        cmdlines = cmdparse.items()
    else:
        cmdlines = cmdparse.__dict__.items()

    for key, value in cmdlines:
        confs[key] = value


def set_path(root):
    Paths.root = root
    Paths.output = os.path.join(root, 'output')
    Paths.config = os.path.join(root, 'config')
    Paths.config_py = os.path.join(Paths.config, 'config.py')
    Paths.proxyFile = os.path.join(root, 'proxyFile')


def program_start(usage):
    print(random.choice(Banner))
    if tosayRun:
        from config.tosay import todaySay
        if todaySay():
            print(todaySay())
    else:
        pass
    if len(sys.argv) == 1:
        print(usage)
        exit(0)


def confs_init():
    confs.version = False
    confs.url = None
    confs.file = None
    confs.ip = None
    confs.web = None
    confs.proxy = None
    confs.proxylist = None
    confs.updateprogram = False
    confs.outputTarget = None
    confs.search = None


def set_confs():
    if confs.updateprogram:
        update()
    if confs.version:
        logger.info("Version: {0}".format(Version))
        exit(0)
    if confs.search:
        searchType = ["fofa", "eye", "qk"]
        if confs.search in set(searchType):
            pass
        else:
            logger.error("参数错误，e.g.(-s fofa or -s eye or -s qk)")
            exit(0)
    if confs.outputTarget:
        outTypes = ["txt", "json", "html", "xls", "csv"]
        if confs.outputTarget in set(outTypes):
            pass
        else:
            logger.error("输出格式错误，只支持输出格式为：{0}".format(outTypes))
            exit(0)
    if confs.ip:
        Urls.ips.append(confs.ip)
    if confs.url:
        if not confs.url.startswith('http'):
            confs.url = "http://" + confs.url
        Urls.url.append(confs.url)
    if confs.file:
        with open(confs.file, 'r') as f:
            for ip in f.readlines():
                if len(ip) != 1:
                    Urls.ips.append(ip.strip())
    if confs.web:
        with open(confs.web, 'r') as f:
            for web in f.readlines():
                if len(web) != 1:
                    if not web.startswith('http'):
                        web = "http://" + web
                    Urls.url.append(web.strip())

    if isinstance(confs["proxy"], str):
        if ":" in confs["proxy"]:
            splits = confs["proxy"].split(":")
            try:
                if int(splits[2]):
                    confs["proxy"] = {splits[0]: "{0}:{1}:{2}".format(
                        splits[0], splits[1], splits[2])}
                    Proxys.proxyList.append(confs["proxy"])
            except ValueError:
                logger.error(
                    "代理地址错误，例如：http://127.0.0.1:8080 or https://127.0.0.1:8080")
                exit(0)
        elif confs["proxy"] != "all" and confs["proxy"] != "cn":
            logger.error(
                "参数错误，all表示加载全部IP，cn加载国内IP，自定义例子为：http://127.0.0.1:8080 or https://127.0.0.1:8080")
            exit(0)
        else:
            checkProxyFile(confs["proxy"])
        if len(Proxys.proxyList) == 0:
            logger.error("本地获取代理失败，请从新获取")
            message = input("是否不使用代理访问？[y/N]")
            if message != "y":
                exit(0)
        else:
            logger.info("分配IP中")
            getScheme()
    if confs.proxylist:
        if confs.proxylist == "all" or confs.proxylist == "cn":
            checkProxyFile(confs.proxylist)
            if len(Proxys.proxyList) == 0:
                logger.error("本地获取代理失败，请重新获取")
                exit(0)
            else:
                tb = pt.PrettyTable()
                tb.field_names = ['Protocol', 'Host']
                for p in Proxys.proxyList:
                    logger.info(p)
                    for i in p:
                        tb.add_row([i, p[i]])
                print(tb)
                logger.info("协议可切换，一般在代理插件里设置http协议，这样避免证书问题")
        else:
            exit(0)


def runmod():
    if Urls.ips:
        if confs.search:
            if confs.search == "fofa":
                logger.info("调用Fofa接口中")
                fmain(Urls.ips)
            if confs.search == "eye":
                logger.info("调用Zoomeye接口中")
                zmain(Urls.ips)
            if confs.search == "qk":
                logger.info("调用Quake接口中")
                qmain(Urls.ips)
        else:
            logger.error("参数错误，e.g.(-s fofa or -s eye or -s qk)")
            exit(0)
    if Urls.url:
        mwebs()
        if WebInfos:
            ruleMain()
        else:
            logger.info("获取信息失败")
    if OutInfos:
        if confs.outputTarget:
            outMain(confs.outputTarget)
        else:
            outMain("txt")


def datas_init():
    Urls.url = []
    Urls.ips = []
    Urls.scheme = []
    Proxys.proxyList = []
    Proxys.scheme = []
    WebInfos = {}
    OutInfos = {}
