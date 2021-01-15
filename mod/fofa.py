# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   fofa.py
@Time  :   2020/12/23 21:33:26
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import json
import time
import base64
import random
import requests
import threading
import prettytable as pt
from requests.adapters import HTTPAdapter
from config.config import fofaApi, fofaSize
from config.config import USER_AGENTS, pyVersion
from config.colors import mkPut
from config.config import threadNum
from config.data import Urls, Paths, Proxys, logger


lock = threading.Lock()


class Fofa(threading.Thread):
    def __init__(self, ip, sem):
        super(Fofa, self).__init__()
        self.email = fofaApi['email']
        self.key = fofaApi['key']
        self.headers = {
            "Cache-Control": "max-age=0",
            "User-Agent": random.choice(USER_AGENTS),
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
        self.ip = ip
        self.sem = sem

    def run(self):
        keywordsBs = base64.b64encode(self.ip.encode('utf-8'))
        keywordsBs = keywordsBs.decode('utf-8')
        url = "https://fofa.so/api/v1/search/all?email={0}&key={1}&qbase64={2}&full=false&fields=ip,title,port,domain,protocol,host&size={3}".format(
            self.email, self.key, keywordsBs, fofaSize)
        try:
            req = requests.Session()
            req.keep_alive = False
            req.headers = self.headers
            if Proxys.proxyList:
                if pyVersion < "3.8":
                    req.proxies = {'https': '{0}'.format(
                        random.choice(Proxys.scheme))}
                else:
                    req.proxies = {
                        "https": 'https://{0}'.format(random.choice(Proxys.scheme))}
            req.mount("https://", HTTPAdapter(max_retries=2))
            target = req.get(url, timeout=10)
            lock.acquire()
            logger.info("正在检测IP: {0}".format(self.ip))
            logger.info("正在通过API获取信息...")
            datas = json.loads(target.text)
            self.ipInfo(datas['results'])
            req.close()
            lock.release()
        except requests.exceptions.ReadTimeout:
            logger.error("请求超时")
        except requests.exceptions.ConnectionError:
            logger.error("网络超时")
        except json.decoder.JSONDecodeError:
            logger.error("获取失败，请重试")
            lock.release()
        self.sem.release()

    def ipInfo(self, datas):
        logger.info("Success")
        tb = pt.PrettyTable()
        tb.field_names = ['IP', 'Title', 'Port', 'Domain', 'Protocol', 'Host']
        logger.info("Url信息：")

        for data in datas:
            tb.add_row(data)
            for keys in data:
                if "http" == keys or "https" == keys:
                    Urls.url.append("{0}://{1}/".format(data[4], data[5]))
                    logger.info("{0}://{1}/".format(data[4], data[5]))
        logger.info("全部信息：")
        print(tb)
        print()


def fmain(ips):
    if fofaApi['email'] and fofaApi['key']:
        pass
    else:
        logger.warning("请修改配置文件{0}中fofaApi为您的API地址".format(Paths.config_py))
        exit(0)
    threads = []
    sem = threading.Semaphore(threadNum)
    try:
        for ip in ips:
            if '/' in ip:
                ip = 'ip="{0}"'.format(ip)
            sem.acquire()
            t = Fofa(ip, sem)
            t.setDaemon(True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass
