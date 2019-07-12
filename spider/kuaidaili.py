#encoding:utf8

import random
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
def get_ip(url,ip):
    print url

    agreement,ip,port = ip['agreement'],ip['ip'],ip['port']
    proxies  = {agreement.lower():ip+':'+port}
    try:
        html = requests.get(url,headers = setting.headers,proxies = proxies)
        html_xpath = etree.HTML(html.content)
        for i in html_xpath.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr'):
            ip = {'ip':i.xpath('td[1]/text()')[0],'port':i.xpath('td[2]/text()')[0],'agreement':i.xpath('td[4]/text()')[0],'ischeck':0,'response_time':'0'}
            result = TB.find(ip)
            if len(list(result)) > 0:
                print u'已经存在了'
            else:
                TB.insert(ip)
    except:
        print 'pass'

def start():
    ip = random.choice(list(TB.find({'ischeck':1,'response_time':{'$lt':'1'}})))
    task = [gevent.spawn(get_ip('https://www.kuaidaili.com/free/intr/{}/'.format(i),ip)) for i in range(1,80)]
    gevent.joinall(task)
    conn.close()
if __name__ == '__main__':
    start()


