# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   zoomeye.py
@Time  :   2021/01/18 19:31:14
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import json
import random
import requests
import threading
import prettytable as pt
from requests.adapters import HTTPAdapter
from config.config import USER_AGENTS, pyVersion, zoomeyeApi
from config.colors import mkPut
from config.config import threadNum
from config.data import Urls, Paths, Proxys, logger


lock = threading.Lock()


class Zoomeye(threading.Thread):
    def __init__(self, ip, sem):
        super(Zoomeye, self).__init__()
        self.headers = {
            "Cache-Control": "max-age=0",
            "User-Agent": random.choice(USER_AGENTS),
            "Upgrade-Insecure-Requests": "1",
            "API-KEY": zoomeyeApi,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
        self.ip = ip
        self.sem = sem

    def run(self):
        if "/" in self.ip:
            self.ip = "cidr:{0}".format(self.ip)
        else:
            self.ip = "ip:{0}".format(self.ip)
        url = "https://api.zoomeye.org/host/search?query={0}".format(self.ip)

        try:
            req = requests.Session()
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
            self.ipInfo(datas['matches'])
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
        tb.field_names = ['IP', 'Title', 'Port', 'Protocol', 'Host']
        for i in datas:
            dataIp = i['ip']
            dataTitle = i['portinfo']['title']
            if dataTitle:
                dataTitle = dataTitle[0]
            dataPort = i['portinfo']['port']
            dataProtocol = i['portinfo']['service']
            dataHost = "{0}:{1}".format(dataIp, dataPort)
            if "http" == dataProtocol or "https" == dataProtocol:
                Urls.url.append(
                    "{0}://{1}:{2}/".format(dataProtocol, dataIp, dataPort))
                logger.info(
                    "{0}://{1}:{2}/".format(dataProtocol, dataIp, dataPort))
            tb.add_row([dataIp, dataTitle, dataPort, dataProtocol, dataHost])
        logger.info("全部信息：")
        print(tb)
        print()


def zmain(ips):
    if zoomeyeApi:
        pass
    else:
        logger.warning("请修改配置文件{0}中zoomeyeApi为您的API地址".format(Paths.config_py))
        exit(0)
    threads = []
    sem = threading.Semaphore(threadNum)
    try:
        for ip in ips:
            sem.acquire()
            t = Zoomeye(ip, sem)
            t.setDaemon(True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass
