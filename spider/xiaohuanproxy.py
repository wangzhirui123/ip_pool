# -*- coding: utf-8 -*-
__author__ = 'Px'

import sys
import pymongo
import gevent
import gevent.monkey
gevent.monkey.patch_socket()
import urllib
import setting
import requests
import re

reload(sys)
sys.setdefaultencoding('utf8')

headers = {

    'authority': 'ip.ihuan.me',
    'method': 'POST',
    'path': '/tqdl.html',
    'scheme': 'https',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    # 'accept-encoding': 'gzip, deflate, br',
    # 'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-length': '117',
    'content-type': 'application/x-www-form-urlencoded',
    'cookie': '__cfduid=d717e9097de084d8f68fc9fdd27c670471560148313; Hm_lvt_8ccd0ef22095c2eebfe4cd6187dea829=1560148313; cf_clearance=0df738f5caabdeed90825e0f43538158aa14bd22-1560148622-1800-250; statistics=8e667cc3bf7f2561b0505917e378c532; Hm_lpvt_8ccd0ef22095c2eebfe4cd6187dea829=1560149158',
    'origin': 'https://ip.ihuan.me',
    'pragma': 'no-cache',
    'referer': 'https://ip.ihuan.me/ti.html',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36'
}
conn = pymongo.MongoClient(setting.MONGO_HOST)
DB = conn[setting.MONGO_DB]
TB = DB[setting.MONGO_TB]
form_data = {
    'num': '3000',
    'port': '',
    'kill_port': '',
    'address': '',
    'kill_address': '',
    'anonymity': '2',
    'type': '0',
    'post': '',
    'sort': '1',
    'key': '1f873ed66ab42608d22b76eefd3e6423'

}

def get_ip():
    html = requests.post('https://ip.ihuan.me/tqdl.html',headers=headers,data=urllib.urlencode(form_data))
    re_com = '<br>(.*?)<br>'
    ip_list = re.findall(re_com,html.content)
    # print html.content
    for i in ip_list:
        ip = {'ip':i.split(':')[0],'port':i.split(':')[1],'agreement':'HTTP','ischeck':0,'response_time':'0'}
        result = TB.find(ip)
        if len(list(result)) > 0:
            print '已经存在了'
        else:
            TB.insert(ip)




if __name__ == '__main__':
    get_ip()



