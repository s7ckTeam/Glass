# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   tosay.py
@Time  :   2020/12/25 21:36:58
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import os
import json
import time
import requests
from config.data import Paths, logger
from config.colors import mkPut


def todaySay():
    files = os.path.join(Paths.config, 'today.json')
    if os.path.isfile(files):
        fileTamp = os.stat(files).st_mtime  # 获取文件创建时间
        timeArray = time.localtime(fileTamp)
        fileTime = time.strftime("%Y%m%d", timeArray)
        osTime = time.strftime("%Y%m%d", time.localtime())
        if fileTime != osTime:
            getpage(files)
    else:
        getpage(files)
    try:
        with open(files, 'r', encoding="utf-8") as f:
            today = json.load(f)
            content = today['content']
            translation = today['translation']
            author = "--- {0}".format(today['author'])
        todaySays = '''
{0}

{1}

\t\t\t\t\t\t{2}
'''.format(content, translation, author)
        return todaySays
    except FileNotFoundError:
        logger.error("未找到每日一说（today.json）文件")


def getpage(files):
    try:
        req = requests.get(
            "https://apiv3.shanbay.com/weapps/dailyquote/quote/", timeout=5)
        with open(files, 'w', encoding="utf-8") as f:
            f.write(req.text)
    except requests.exceptions.ConnectionError:
        logger.warning("更新每日一说超时")
    except requests.exceptions.ReadTimeout:
        logger.warning("更新每日一说超时")
