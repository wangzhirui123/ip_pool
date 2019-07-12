#encoding:utf8
import sys
from Queue import Queue
import pymongo
import gevent
import gevent.monkey
gevent.monkey.patch_socket()
from lxml import etree
import setting
import requests
reload(sys)
sys.setdefaultencoding('utf8')

conn = pymongo.MongoClient(setting.MONGO_HOST)
DB = conn[setting.MONGO_DB]
TB = DB[setting.MONGO_TB]
def get_ip(url):
    print url
    html = requests.get(url,headers = setting.headers)
    html_xpath = etree.HTML(unicode(html.content))
    for i in html_xpath.xpath('//table[@class="table table-bordered proxy-index-table"]/tr')[1:]:

        ip = {'ip':i.xpath('td[1]/text()')[0],'port':i.xpath('td[2]/text()')[0],'agreement':i.xpath('td[4]/text()')[0].split(',')[-1],'ischeck':0,'response_time':'0'}
        result = TB.find(ip)
        if len(list(result)) > 0:
            print u'已经存在了'
        else:
            TB.insert(ip)

def start():
    gevent.spawn(get_ip('http://lab.crossincode.com/proxy/'))
    conn.close()
if __name__ == '__main__':

    start()






