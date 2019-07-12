# -*- coding: utf-8 -*-
__author__ = 'Px'

import pymongo
import gevent
import gevent.monkey
gevent.monkey.patch_socket()
from lxml import etree
import setting
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')
conn = pymongo.MongoClient(setting.MONGO_HOST)
DB = conn[setting.MONGO_DB]
TB = DB[setting.MONGO_TB]
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': 'Hm_lvt_04016d42f1ac9e7b86c5b8519f2c0518=1560138164; Hm_lpvt_04016d42f1ac9e7b86c5b8519f2c0518=1560138298',
    'Host': 'www.nimadaili.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'

}

def get_ip(url):
    html = requests.get(url,headers = headers).content
    html_xpath = etree.HTML(html)
    for i in html_xpath.xpath('//table[@class="fl-table"]/tbody/tr'):

        ip = {'ip':i.xpath('td[1]/text()')[0].split(':')[0],'port':i.xpath('td[1]/text()')[0].split(':')[1],'agreement':i.xpath('td[2]/text()')[0].split(',')[0].replace('代理',''),'ischeck':0,'response_time':'0'}
        result = TB.find(ip)
        if len(list(result)) > 0:
            print '已经存在了'
        else:
            TB.insert(ip)

def start():
        tasks = [gevent.spawn(get_ip('http://www.nimadaili.com/gaoni/{}/'.format(i))) for i in range(1,2001)]
        gevent.joinall(tasks)



if __name__ == '__main__':
    start()


