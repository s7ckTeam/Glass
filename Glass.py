# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   Glass.py
@Time  :   2020/12/23 17:37:25
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import sys
sys.dont_write_bytecode = True

try:
    from config.data import logger
    import console

    console.main()
except ModuleNotFoundError as ex:
    moduleName = str(ex).split("'")[1]
    logger.error("未找到相关模块 {0}".format(moduleName))
    logger.info(
        "输入：python3 -m pip install {0}，或者：pip3 install {1} 进行安装".format(moduleName, moduleName))
