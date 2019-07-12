#encoding:utf8

from concurrent import futures
import setting
import gevent
from gevent import monkey
monkey.patch_socket()
import random
import pymongo
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

}

class XiCiProxy(object):

    def __init__(self):
        self.Conn = pymongo.MongoClient(setting.MONGO_HOST)
        self.DB = self.Conn[setting.MONGO_DB]
        self.TB = self.DB[setting.MONGO_TB]

    def get_link(self):

        url_list = ['https://www.xicidaili.com/nn/{}'.format(i) for i in range(1,200)]
        return url_list

    def save_db(self,ip_dict):
        result = self.TB.find(ip_dict)
        if len(list(result)) > 0:
            print u'已经存在了'
        else:
            self.TB.insert(ip_dict)



    def get_proxy(self,url):
        import time
        import random
        import requests
        from lxml import etree


        myquery = {'ischeck':1}
        result = list(self.TB.find(myquery))
        ip_dict = random.choice(result)

        agreement,ip,port = ip_dict['agreement'],ip_dict['ip'],ip_dict['port']
        proxies  = {agreement.lower():ip+':'+port}
        html = requests.get(url,proxies=proxies,headers=headers,timeout=5)
        html_xpath = etree.HTML(html.content)
        for i in html_xpath.xpath('//table[@id="ip_list"]/tr'):
            try:

                ip = {'ip':str(i.xpath('td[2]/text()')[0]),'port':str(i.xpath('td[3]/text()')[0]),'agreement':str(i.xpath('td[6]/text()')[0]),'ischeck':0,'response_time':'0'}
                self.save_db(ip)

            except Exception as e:
                print e
                continue

        time.sleep(3)
    def check_ip(self,url):
        import urllib2
        from lxml import etree
        # print  url

        agreement,ip,port = url.split(':')
        proxy_handler = urllib2.ProxyHandler({agreement.lower():ip+':'+port})
        opener=urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
        code = urllib2.Request('http://ip.tool.chinaz.com/')
        conn = urllib2.urlopen(code)
        html = conn.read()
        html_xpath = etree.HTML(html)
        address = html_xpath.xpath('//dd[@class="fz24"]/text()')[0]
        print address,ip+':'+port

def start():
    a = XiCiProxy()
    task = [gevent.spawn(a.get_proxy(i)) for i in a.get_link()]
    gevent.joinall(task)
if __name__ == '__main__':
    start()
