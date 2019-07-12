#encoding:utf8
import pymongo
import setting
from concurrent import futures

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'

}

def get_ip():

    result = list(TB.find())
    # print type(result)
    return result

def check_ip(ip_dict):
    import time
    import requests
    from lxml import etree

    agreement,ip,port = ip_dict['agreement'],ip_dict['ip'],ip_dict['port']
    proxies  = {agreement.lower():ip+':'+port}
    start_time = time.time()
    # code = requests.get('http://ip.tool.chinaz.com/',proxies =proxies,headers=headers,timeout=5)
    code = requests.get('http://103.214.168.94:8012/',proxies =proxies,headers=headers,timeout=5)
    end_time = time.time()
    # html_xpath = etree.HTML(code.content)
    # address = html_xpath.xpath('//dd[@class="fz24"]/text()')[0]
    if code.content == ip.strip():
        myquery = {'ip':ip}
        new_value = {'$set':{'ischeck':1,'response_time':str(abs(end_time-start_time))}}
        TB.update(myquery,new_value)
        print code.content,ip+':'+port


if __name__ == '__main__':
    conn = pymongo.MongoClient()
    DB = conn[setting.MONGO_DB]
    TB = DB[setting.MONGO_TB]
    myquery = {}
    TB.update_many(myquery,{'$set':{'ischeck':0}})
    with futures.ThreadPoolExecutor(200)as P:

        P.map(check_ip,get_ip())



