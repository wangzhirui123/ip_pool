# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import os
dir_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(dir_path)
from spider import ip13366,jiangxianliproxy,kuaidaili,mianfeiproxy,proxy66,proxy89,wuyouproxy,xiaoshuproxy,XiCiproxy,xilaprxy
reload(sys)
sys.setdefaultencoding('utf8')

spider_list = [mianfeiproxy,proxy66,proxy89,wuyouproxy,xiaoshuproxy,XiCiproxy,xilaprxy,ip13366,jiangxianliproxy]
if __name__ == '__main__':

    for i in spider_list:
        try:
            i.start()
        except Exception as e:
            print e
            continue

