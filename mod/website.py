# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   website.py
@Time  :   2020/12/24 23:38:10
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import ssl
import json
import time
import random
import urllib3
import requests
import threading
from requests.adapters import HTTPAdapter
from config.data import Urls, WebInfos, Proxys, logger
from config.rules import ruleDatas
from config.config import USER_AGENTS, pyVersion
from config.config import threadNum
from config.colors import mkPut

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()
lock = threading.Lock()


class webInfo(threading.Thread):
    def __init__(self, target, sem):
        super(webInfo, self).__init__()
        self.headers = {
            "User-Agent": random.choice(USER_AGENTS),
        }
        self.target = target
        self.sem = sem

    def run(self):
        for key in self.target:
            scheme = key
            url = self.target[key]
        s = requests.Session()
        s.keep_alive = False
        s.headers = self.headers
        # s.mount("http://", HTTPAdapter(max_retries=3))
        # s.mount("https://", HTTPAdapter(max_retries=3))
        s.verify = False
        shiroCookie = {'rememberMe': '1'}
        if Proxys.proxyList:
            if pyVersion < "3.8":
                s.proxies = {scheme: "{0}".format(
                    random.choice(Proxys.scheme))}
            else:
                s.proxies = {
                    scheme: "{0}://{1}".format(scheme, random.choice(Proxys.scheme))}
        s.cookies.update(shiroCookie)
        try:
            req = s.get(url, timeout=5)
            lock.acquire()
            webHeaders = req.headers
            try:
                webCodes = req.content.decode('utf-8')
            except UnicodeDecodeError:
                webCodes = req.content.decode('gbk', 'ignore')
            WebInfos[url] = webHeaders, webCodes, req.status_code, req.cookies.get_dict()
            req.close()
            logger.info("命中{0}个链接".format(len(WebInfos)))
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


def mwebs():
    threads = []
    logger.info("共采集{0}个web链接".format(len(Urls.url)))
    logger.info("获取网页信息中")
    for url in Urls.url:
        scheme_url = url.split(':')
        scheme = scheme_url[0]
        Urls.scheme.append({scheme: url})
    sem = threading.Semaphore(threadNum)
    try:
        for url in Urls.scheme:
            sem.acquire()
            t = webInfo(url, sem)
            t.setDaemon(True)
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        pass
    print()
