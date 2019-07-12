#encoding:utf8


import pymongo
import gevent
import gevent.monkey
gevent.monkey.patch_socket()
from lxml import etree
import setting
import requests

conn = pymongo.MongoClient(setting.MONGO_HOST)
DB = conn[setting.MONGO_DB]
TB = DB[setting.MONGO_TB]
def get_ip(url):
    headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.ip3366.net',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'


    }
    print url
    html = requests.get(url,headers = headers)
    html_xpath = etree.HTML(html.content)
    for i in html_xpath.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr'):
        ip = {'ip':i.xpath('td[1]/text()')[0],'port':i.xpath('td[2]/text()')[0],'agreement':i.xpath('td[4]/text()')[0],'ischeck':0,'response_time':'0'}


        result = TB.find(ip)
        if len(list(result)) > 0:
            print u'已经存在了'
        else:
            TB.insert(ip)


def start():

    task = [gevent.spawn(get_ip('http://www.ip3366.net/?stype=1&page={}'.format(i))) for i in range(1,11)]
    gevent.joinall(task)
    conn.close()
if __name__ == '__main__':
    start()








