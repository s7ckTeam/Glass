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
from config.data import Paths
from config.colors import mkPut


def todaySay():
    # fileTamp = os.path.getctime(Paths.config[0] + 'today.json')
    fileTamp = os.stat(Paths.config[0]+'today.json').st_mtime
    timeArray = time.localtime(fileTamp)
    fileTime = time.strftime("%Y%m%d", timeArray)
    osTime = time.strftime("%Y%m%d", time.localtime())
    if fileTime != osTime:
        try:
            req = requests.get(
                "https://rest.shanbay.com/api/v2/quote/quotes/today/", timeout=3)
        except requests.exceptions.ConnectionError:
            print(mkPut.fuchsia("[{0}]".format(time.strftime(
                "%H:%M:%S", time.localtime()))), mkPut.yellow("[warning]"), "更新每日一说超时")
        with open(Paths.config[0]+'today.json', 'w', encoding="utf-8") as f:
            f.write(req.text)

    with open(Paths.config[0]+'today.json', 'r', encoding="utf-8") as f:
        today = json.load(f)
        content = today['data']['content']
        translation = today['data']['translation']
        author = "--- {0}".format(today['data']['author'])

    todaySays = '''
{0}

{1}

\t\t\t\t\t\t{2}
'''.format(content, translation, author)
    return todaySays
