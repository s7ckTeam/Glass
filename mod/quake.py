# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   quake.py
@Time  :   2022/01/26 16:08:24
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
from config.config import quakeApi, quakeSize
from config.config import USER_AGENTS, pyVersion
from config.colors import mkPut
from config.config import threadNum
from config.data import Urls, Paths, Proxys, logger

lock = threading.Lock()


class Quake(threading.Thread):
    def __init__(self, ip, sem):
        super(Quake, self).__init__()
        self.ip = ip
        self.sem = sem
        self.url = "https://quake.360.cn/api/v3/search/quake_service"
        self.headers = {
            "User-Agent": random.choice(USER_AGENTS),
            "X-QuakeToken": quakeApi,
        }
        self.jsonData = {
            "query": self.ip,
            "start": 0,
            "size": quakeSize,
        }

    def run(self):
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
            target = req.post(self.url, json=self.jsonData)
            lock.acquire()
            logger.info("正在检测IP: {0}".format(self.ip))
            logger.info("正在通过API获取信息...")
            datas = json.loads(target.text)
            if datas['code'] == 1:
                logger.warning("接口积分不足")
            if datas['code'] == 2:
                logger.warning("限速了，请等待")
            self.ipInfo(datas['data'])
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
        tb.field_names = ['IP', 'Port', 'Protocol', 'Title']
        logger.info("Url信息：")

        for data in datas:
            ip = data['ip']
            port = data['port']
            protocol = data['service']['name']
            if 'http' in data['service']:
                title = data['service']['http']['title']
                if protocol == "http":
                    qkurl = "http://{0}:{1}/".format(ip, port)
                if protocol == "http/ssl":
                    qkurl = "https://{0}:{1}/".format(ip, port)
                logger.info(qkurl)
                Urls.url.append(qkurl)
            else:
                title = "None"
            tb.add_row([ip, port, protocol, title])
        Urls.url = list(dict.fromkeys(Urls.url))
        logger.info("全部信息：")
        print(tb)
        print()


def qmain(ips):
    if quakeApi:
        pass
    else:
        logger.warning("请修改配置文件{0}中quakeApi为您的API地址".format(Paths.config_py))
        exit(0)
    threads = []
    sem = threading.Semaphore(threadNum)
    try:
        for ip in ips:
            sem.acquire()
            t = Quake(ip, sem)
            t.setDaemon(True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass
