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

import json
import time
import random
import urllib3
import requests
import threading
from requests.adapters import HTTPAdapter
from config.data import Urls, WebInfos
from config.rules import ruleDatas
from config.config import USER_AGENTS
from config.config import threadNum
from config.colors import mkPut

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
        s = requests.Session()
        s.keep_alive = False
        s.headers = self.headers
        # s.mount("http://", HTTPAdapter(max_retries=3))
        # s.mount("https://", HTTPAdapter(max_retries=3))
        s.verify = False
        shiroCookie = {'rememberMe': '1'}
        s.cookies.update(shiroCookie)
        try:
            req = s.get(self.target, timeout=5)
            lock.acquire()
            webHeaders = req.headers
            webCodes = req.text
            WebInfos[self.target] = webHeaders, webCodes, req.status_code
            req.close()
            print(mkPut.fuchsia("[{0}]".format(time.strftime("%H:%M:%S", time.localtime(
            )))), mkPut.green("[INFO]"), "命中{0}个链接".format(len(WebInfos)), end='\r', flush=True)
            lock.release()
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.ChunkedEncodingError:
            pass
        except KeyboardInterrupt:
            pass
        self.sem.release()


def mwebs():
    threads = []
    print(mkPut.fuchsia("[{0}]".format(time.strftime("%H:%M:%S", time.localtime()))),
          mkPut.green("[INFO]"), "共采集{0}个web链接".format(len(Urls.url)))
    print(mkPut.fuchsia("[{0}]".format(time.strftime(
        "%H:%M:%S", time.localtime()))), mkPut.green("[INFO]"), "获取网页信息中")
    sem = threading.Semaphore(threadNum)
    try:
        for url in Urls.url:
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
    print()
