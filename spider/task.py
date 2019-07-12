# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import re
import urllib2
import time
import requests
import MySQLdb
from lxml import etree
from bs4 import BeautifulSoup
import setting
reload(sys)
sys.setdefaultencoding('utf8')

Proxy_hander = urllib2.ProxyHandler({'http':'110.18.153.182:6410'})
opener = urllib2.build_opener(Proxy_hander)
urllib2.install_opener(opener)
req = urllib2.Request('https://www.baidu.com/s?wd=ip',headers=setting.headers)
html = urllib2.urlopen(req).read()
print html

