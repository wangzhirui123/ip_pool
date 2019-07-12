#encoding:utf8

import pymongo
from Queue import Queue
import gevent
import gevent.monkey
import urlparse
gevent.monkey.patch_socket()
from lxml import etree
import setting
import requests

conn = pymongo.MongoClient(setting.MONGO_HOST)
DB = conn[setting.MONGO_DB]
TB = DB[setting.MONGO_TB]


detail_Q = Queue()
headers = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding':'gzip, deflate',
    'Accept-Language':'zh-CN,zh;q=0.9',
    'Cache-Control':'max-age=0',
    'Connection':'keep-alive',
    'Cookie':'__guid=165339577.3712093674758733000.1559268955766.2935; monitor_count=1',
    'Host':'www.xsdaili.com',
    'If-Modified-Since':'Thu, 30 May 2019 21:00:05 GMT',
    'If-None-Match':'W/"5cf04455-617b"',
    'Upgrade-Insecure-Requests':'1',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'

}
def get_link(url):
    html = requests.get(url,headers = headers)

    html_xpath = etree.HTML(html.content)
    links = html_xpath.xpath('//div[@class="col-md-12"]/div[@class="table table-hover panel-default panel ips "]/div[@class="title"]/a/@href')
    for i in links:
        detail_Q.put(urlparse.urljoin('http://www.xsdaili.com',i))

def get_ip():
    while detail_Q.qsize() > 0:
        url = detail_Q.get()
        print url
        html = requests.get(url,headers = setting.headers)
        html_xpath = etree.HTML(html.content)
        ip_obj = html_xpath.xpath('//div[@class="cont"]/text()')
        for i in ip_obj:
            try:
                ip = {'ip':i.split(':')[0],'port':i.split(':')[1].split('@')[0],'agreement':i.split('@')[-1].split('#')[0],'ischeck':0,'response_time':'0'}
            except:
                continue
        result = TB.find(ip)
        if len(list(result)) > 0:
            print u'已经存在了'
        else:
            TB.insert(ip)

def start():

    task = [gevent.spawn(get_link('http://www.xsdaili.com/dayProxy/{}.html'.format(i))) for i in range(2,87)]
    gevent.joinall(task)
    gevent.spawn(get_ip())
    conn.close()
if __name__ == '__main__':
    start()









