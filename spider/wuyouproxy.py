#encoding:utf8
'''每小时更新'''
import sys
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
    print html.content
    html_xpath = etree.HTML(unicode(html.content))
    for i in html_xpath.xpath('//ul[@class="l2"]'):

        ip = {'ip':i.xpath('span[1]/li/text()')[0],'port':i.xpath('span[2]/li/text()')[0],'agreement':i.xpath('span[4]/li/text()')[0],'ischeck':0,'response_time':'0'}

        result = TB.find(ip)
        if len(list(result)) > 0:
            print u'已经存在了'
        else:
            TB.insert(ip)

def start():
    gevent.spawn(get_ip('http://www.data5u.com/free/index.shtml'))
    conn.close()
if __name__ == '__main__':

    start()







