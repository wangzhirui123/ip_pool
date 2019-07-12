# -*- coding: utf-8 -*-
__author__ = 'Px'

import pymongo
import gevent
import gevent.monkey
gevent.monkey.patch_socket()

import requests
import sys
conn = pymongo.MongoClient('localhost')
DB = conn['proxy_db']
TB = DB['proxy_tb']

reload(sys)
sys.setdefaultencoding('utf8')


def HTTP_GET():

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Content-Length': '203',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'Hm_lvt_1fe64df7c1a8fed68f5186ce1f28782b=1560828191; _daili_sesfdasion=N1UvdGVZZTVzc3hBSnk1TWs5S3Q1T1JqaDVQV2hzaWNudmhvb25RN0pPMUk3dFlLclptd1RsZENaR3YwSWlhcFFoK3FhdUVqZG01RHVPZmhYczF2cEIvTTBpSGxHeXJhVzBwTmMwQnBzQS9XdkVPS1RzU3pFUy9vSjRtTFBUa2hybmtQUHY2VDlua1hCeGk0a0J0RC9PaXJLU2RGVUJ1aDZQK09tWUxMTnpQSjYzQlVZc21OVGtibGVPSkN6RGRzOGJ4QnZCRTh3Q1dCWUxhQWNJOU5TbFVVMUNHSDRpL1JITk84N1RhK0Y4QkNML0NteFhaekV6a3h4cEtUeFpQOUZvWk5IdlNVNklLbFIrR0plSncwb2krb2VKeXdqWCtkbG9ZWWtKZG5DQjJjamljYk5mT2hwK3g5RTN6MTZhaHBJSTJkWWs2OTcrZzh2R2NqMjhTa3RZTFZSWVBWc1RLSHhQTlhFOUlzdHRqK2VsQnhzMWpUTlFpRWttTkgvVytUSWlXTFdKaWU1akNOMzVIYitGMnBKUW9zdlEwcGVmNytDcENSZk56L0xIeG9SQW9NcVQ2N0tvYzIxeHU0SUZpVVNDZ1hPRmYwUWhIaUREUytEeVVzL2ZEVys5Uy83ZHF6KzNab0VGbCtoZzlmQUdxUHNGUmt1SjJGMjc3eFgzVlgtLW52YU03cUluT3g1bERtd2VlQ0I1dmc9PQ%3D%3D--bafcc17c97fb8b14b65a57dfe4c84fb508313ff8; Hm_lpvt_1fe64df7c1a8fed68f5186ce1f28782b=1560829425',
        'Host': 'www.daxiangdaili.com',
        'Origin': 'http://www.daxiangdaili.com',
        'Pragma': 'no-cache',
        'Referer': 'http://www.daxiangdaili.com/web?tid=555121938720927',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'

    }

    form_data = "tid=555121938720927&num=100&area=&foreign=all&operator=%E7%94%B5%E4%BF%A1&operator=%E8%81%94%E9%80%9A&operator=%E7%A7%BB%E5%8A%A8&ports=&exclude_ports=8090%2C8123&category=2&protocol=&filter=on&download="
    html =requests.post('http://www.daxiangdaili.com/pick/',headers=headers,data=form_data).content
    with open('ip.txt','w')as f:
        f.write(html)

def get_ip():
    with open('ip.txt','a+')as f:
        ip_list = f.readlines()
        for i in ip_list:
            i=i.replace('\r','')
            ip = {'ip':i.split(':')[0],'port':i.split(':')[1].replace('\n',''),'agreement':"HTTP",'ischeck':0,'response_time':'0'}

            result = TB.find(ip)
            if len(list(result)) > 0:
                print u'已经存在了'
            else:
                TB.insert(ip)

if __name__ == '__main__':

    HTTP_GET()
    get_ip()