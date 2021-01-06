# /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@File  :   output.py
@Time  :   2020/12/27 05:55:34
@Author:   Morker
@Blog  :   https://96.mk/
@Email :   i@96.mk

If you don't go through the cold, you can't get the fragrant plum blossom.
'''

import time
from config.data import Paths, OutInfos
from config.config import OS
from config.colors import mkPut


class output():
    def __init__(self):
        self.nowTime = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if OS == "Windows":
            self.path = Paths.output[0] + "{0}.txt".format(self.nowTime)
        else:
            self.path = Paths.output[0] + "{0}.txt".format(self.nowTime)

    def outTxt(self):
        with open(self.path, 'w', encoding='utf-8') as f:
            for key in OutInfos:
                f.write("{0} {1}\n".format(key, OutInfos[key]))
        print()
        print(mkPut.fuchsia("[{0}]".format(time.strftime("%H:%M:%S", time.localtime(
        )))), mkPut.green('[INFO]'), '文件输出路径为：{0}'.format(self.path))
