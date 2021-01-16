# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   rulesCli.py
@Time  :   2020/12/26 18:14:58
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import re
import time
from config.colors import mkPut
from config.data import WebInfos, OutInfos, logger
from config.rules import ruleDatas


class ruleInfo():
    def __init__(self):
        self.rex = re.compile('<title>(.*?)</title>')

    def main(self):
        for rule in ruleDatas:
            cms = rule[0]
            rulesRegex = rule[2]
            if 'headers' == rule[1]:
                self.heads(rulesRegex, cms)
            elif 'cookie' == rule[1]:
                self.cookieInfo(rulesRegex, cms)
            else:
                self.bodys(rulesRegex, cms)
        webTitle = ""
        webServer = ""
        webCms = "None"
        for key in WebInfos:
            if 'server' in WebInfos[key][0]:
                webServer = WebInfos[key][0]['server']
            else:
                webServer = "None"
            webTitles = re.findall(self.rex, WebInfos[key][1])
            if webTitles:
                webTitle = webTitles[0]
            else:
                webTitle = "None"
            OutInfos[key] = webCms, webServer, WebInfos[key][2], webTitle
            logger.success("{} {} {} {}".format(mkPut.green(webServer), mkPut.yellow(
                WebInfos[key][2]), key, mkPut.blue(webTitle)))

    def heads(self, rulesRegex, cms):
        webTitle = ""
        webServer = ""
        for key in list(WebInfos):
            if 'server' in WebInfos[key][0]:
                webServer = WebInfos[key][0]['server']
            else:
                webServer = "None"
            webTitles = re.findall(self.rex, WebInfos[key][1])
            if webTitles:
                webTitle = webTitles[0]
            else:
                webTitle = "None"
            for head in WebInfos[key][0]:
                resHeads = re.findall(rulesRegex, WebInfos[key][0][head])
                if resHeads:
                    logger.success("{} {} {} {} {}".format(mkPut.red(cms), mkPut.green(
                        webServer), mkPut.yellow(WebInfos[key][2]), key, mkPut.blue(webTitle)))
                    OutInfos[key] = cms, webServer, WebInfos[key][2], webTitle
                    WebInfos.pop(key)
                    break

    def bodys(self, rulesRegex, cms):
        webTitle = ""
        webServer = ""
        for key in list(WebInfos):
            if 'server' in WebInfos[key][0]:
                webServer = WebInfos[key][0]['server']
            else:
                webServer = "None"
            webTitles = re.findall(self.rex, WebInfos[key][1])
            if webTitles:
                webTitle = webTitles[0]
            else:
                webTitle = "None"
            resCodes = re.findall(rulesRegex, WebInfos[key][1])
            if resCodes:
                logger.success("{} {} {} {} {}".format(mkPut.red(cms), mkPut.green(
                    webServer), mkPut.yellow(WebInfos[key][2]), key, mkPut.blue(webTitle)))
                OutInfos[key] = cms, webServer, WebInfos[key][2], webTitle
                WebInfos.pop(key)
                # break

    def cookieInfo(self, rulesRegex, cms):
        webTitle = ""
        webServer = ""
        for key in list(WebInfos):
            if 'server' in WebInfos[key][0]:
                webServer = WebInfos[key][0]['server']
            else:
                webServer = "None"
            webTitles = re.findall(self.rex, WebInfos[key][1])
            if webTitles:
                webTitle = webTitles[0]
            else:
                webTitle = "None"
            for cookie in WebInfos[key][3]:
                resCookies = re.findall(rulesRegex, cookie)
                if resCookies:
                    logger.success("{} {} {} {} {}".format(mkPut.red(cms), mkPut.green(
                        webServer), mkPut.yellow(WebInfos[key][2]), key, mkPut.blue(webTitle)))
                    OutInfos[key] = cms, webServer, WebInfos[key][2], webTitle
                    WebInfos.pop(key)
                    break


def ruleMain():
    start = ruleInfo()
    start.main()
