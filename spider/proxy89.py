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
    print url
    html = requests.get(url,headers = setting.headers)
    html_xpath = etree.HTML(html.content)
    for i in html_xpath.xpath('//table[@class="layui-table"]/tbody/tr'):

        ip = {'ip':i.xpath('td[1]/text()')[0].replace('\r','').replace('\n','').replace('\t',''),'port':i.xpath('td[2]/text()')[0].replace('\r','').replace('\n','').replace('\t',''),'agreement':'HTTP','ischeck':0,'response_time':'0'}
        print ip
        result = TB.find(ip)
        if len(list(result)) > 0:
            print u'已经存在了'
        else:
            TB.insert(ip)

def start():
    task = [gevent.spawn(get_ip('http://www.89ip.cn/index_{}.html'.format(i))) for i in range(1,16)]
    gevent.joinall(task)
    conn.close()

if __name__ == '__main__':
    start()









