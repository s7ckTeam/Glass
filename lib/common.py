# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   common.py
@Time  :   2021/01/14 16:26:21
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import re
import random
import requests
from config.config import USER_AGENTS
from config.data import Proxys, Urls


def getLatestRevision():
    """
    获取版本信息
    """
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
    }
    readVersion = None
    try:
        req = requests.get(
            url="https://96.mk/Glass/Glass_Version.txt", headers=headers)
        content = req.text
        readVersion = re.findall(
            "Version\s*=\s*[\"'](?P<result>[\d.]+)", content)
    except:
        pass

    return readVersion[0]


def getScheme():
    if Proxys.proxyList:
        for key in Proxys.proxyList:
            for i in key:
                host = key[i].split('/')[2]
                Proxys.scheme.append(host)
