# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import re
import time
import requests
import MySQLdb
from lxml import etree
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf8')
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'UM_distinctid=169b432c9538b8-06890730e77645-39614101-1fa400-169b432c95413b; CNZZDATA1274609462=1007102705-1553505921-%7C1553505921',
    'Host': '103.214.168.94:8012',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'

}
proxies = {'http':'111.231.73.203:9999'}
html = requests.get('http://103.214.168.94:8012/',proxies=proxies)
print html.content

