# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   proxy.py
@Time  :   2021/01/11 10:22:10
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import re
import os
import ssl
import time
import json
import random
import urllib3
import requests
import threading
from requests.adapters import HTTPAdapter
from config.config import USER_AGENTS, threadNum, pyVersion
from config.data import Proxys, logger, Paths


ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()
lock = threading.Lock()


class ProxyInfo(threading.Thread):
    def __init__(self, types, host, port, sem):
        super(ProxyInfo, self).__init__()
        self.types = types
        self.host = host
        self.port = port
        self.sem = sem
        self.headers = {
            "User-Agent": random.choice(USER_AGENTS),
        }

    def run(self):
        s = requests.Session()
        s.headers = self.headers
        if pyVersion < "3.8":
            s.proxies = {self.types: "{0}:{1}".format(self.host, self.port)}
        else:
            s.proxies = {
                self.types: "{0}://{1}:{2}".format(self.types, self.host, self.port)}
        try:
            req = s.get("https://httpbin.org/ip", timeout=5)
            lock.acquire()
            codes = req.text
            if ',' in codes:
                pass
            elif self.host in codes:
                Proxys.proxyList.append(
                    {self.types: "{0}://{1}:{2}".format(self.types, self.host, self.port)})
            req.close()
            lock.release()
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.ChunkedEncodingError:
            pass
        except KeyboardInterrupt:
            lock.release()
            pass
        self.sem.release()


def getPage(country):
    s = requests.Session()
    s.headers = {
        "User-Agent": random.choice(USER_AGENTS),
    }
    s.keep_alive = False
    proxyGit = "https://raw.githubusercontent.com/fate0/proxylist/master/proxy.list"
    proxyPage = "http://proxylist.fatezero.org/proxy.list"
    try:
        target = s.get(proxyGit)
    except requests.exceptions.ConnectionError:
        try:
            target = s.get(proxyPage)
        except requests.exceptions.ConnectionError:
            logger.error("网络超时，获取失败，请重新获取")
            exit(0)
    datas = target.text.split('\n')
    proxyDatas = []
    for proxy_str in datas:
        if proxy_str:
            proxy_json = json.loads(proxy_str)
            if country == "cn":
                if proxy_json['country'] == "CN":
                    host = proxy_json['host']
                    port = proxy_json['port']
                    types = proxy_json['type']
                    proxyDatas.append([types, host, port])
            else:
                host = proxy_json['host']
                port = proxy_json['port']
                types = proxy_json['type']
                proxyDatas.append([types, host, port])
    return proxyDatas


def getProxy(country, files):
    logger.info("正在获取代理IP")
    proxyDatas = getPage(country)
    logger.info("总共获取{0}条IP".format(len(proxyDatas)))
    logger.info("正在验证高质量IP")
    threads = []
    sem = threading.Semaphore(threadNum)
    try:
        for i in proxyDatas:
            types = i[0]
            host = i[1]
            port = i[2]
            sem.acquire()
            t = ProxyInfo(types, host, port, sem)
            t.setDaemon(True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass
    if Proxys.proxyList:
        logger.info("获取{0}条高质量IP".format(len(Proxys.proxyList)))
        for p in Proxys.proxyList:
            with open(files, 'a', encoding="utf-8") as f:
                f.write(str(p))
                f.write('\n')
    else:
        logger.error("在线获取失败")


def checkProxyFile(country):
    if os.path.isdir(Paths.proxyFile):
        pass
    else:
        os.mkdir(Paths.proxyFile)
    files = os.path.join(Paths.proxyFile, 'proxy.txt')
    if os.path.isfile(files):
        fileTamp = os.stat(files).st_mtime  # 获取文件创建时间
        timeArray = time.localtime(fileTamp)
        fileTime = time.strftime("%Y%m%d%H%M", timeArray)
        osTime = time.strftime("%Y%m%d%H%M", time.localtime())
        contrast = int(osTime) - int(fileTime)
        if contrast >= 15:
            os.remove(files)
            getProxy(country, files)
        else:
            try:
                with open(files, 'r', encoding="utf-8") as f:
                    for pro in f.readlines():
                        p = pro.strip()
                        _proxy = eval(p)
                        Proxys.proxyList.append(_proxy)
            except FileNotFoundError:
                pass
    else:
        getProxy(country, files)
