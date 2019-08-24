# 2018.10.05

import csv
import random
import time
import requests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from requests import ConnectTimeout, ReadTimeout, ConnectionError, Timeout
from requests.exceptions import ProxyError


def getproxy():
    setproxy = [{"http": "http://202.103.12.29:59482"}, {"http": "http://106.75.226.36:808"},
                {"http": "http://61.135.217.7:80"}, {"http": "http://116.1.11.19:80"},
                {"http": "http://221.205.174.185:8118"}, {"http": "http://124.235.181.175:80"},
                {"http": "http://121.196.196.105:80"}, {"http": "http://106.75.169.71:3128"}]
    lens = len(setproxy)
    for i in range(lens):
        yield setproxy[i]

header ={
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "User-Agent": "IP"
}
def parse_detailjob(joburl):
    global nowproxy,proxy
    url = 'https://hr.tencent.com/' + joburl
    try:
        response = requests.get(url, headers = header, proxies = nowproxy)
        html = response.text
        selector = etree.HTML(html)
        trs = selector.xpath('//ul[@class="squareli"]')
        jobduty = trs[0].xpath('li/text()')[0]
        jobrequire = trs[1].xpath('li/text()')[0]
        return jobduty, jobrequire
    except (ConnectionError, TimeoutError,ConnectTimeout,ReadTimeout,ProxyError, Timeout):
        try:
            nowproxy = proxy.__next__()
            print(nowproxy)
            return parse_detailjob(joburl)
        except StopIteration:
            print("proxies error")

def parse_page(url):
    global nowproxy,proxy
    try:
        response = requests.get(url, headers=header, proxies=nowproxy)
        html = response.text
        selector = etree.HTML(html)
        trs = selector.xpath('//tr[@class!="h" and @class!="f"]')
        for item in trs:
            jobname = item.xpath('td/a/text()')[0]
            joburl = item.xpath('td/a/@href')[0]
            try:
                type = item.xpath('td')[1].xpath('text()')[0]
            except:
                type = ""
            numbers = item.xpath('td')[2].xpath('text()')[0]
            site = item.xpath('td')[3].xpath('text()')[0]
            date = item.xpath('td')[4].xpath('text()')[0]
            jobduty, jobrequire = parse_detailjob(joburl)
            joblist = [jobname, type, numbers, site, jobduty, jobrequire, date]
            writer.writerow(joblist)
            print(joblist)
    except (ConnectionError, TimeoutError):
        try:
            nowproxy = proxy.__next__()
            print(nowproxy)
            return parse_page(url)
        except StopIteration:
            print("proxies error")
if __name__ =="__main__":
    file = open('social jobs of tecent.csv','a',newline= '', encoding="UTF8")
    writer = csv.writer(file)
    writer.writerow(["职位名称","职位类别","招聘人数","工作地点","工作职责","招聘要求","发布日期"])
    proxy = getproxy()
    nowproxy = proxy.__next__()
    print(nowproxy)
    pool = ThreadPoolExecutor()
    def get_html(num):
        url = 'https://hr.tencent.com/position.php?&start={n}#a'.format(n=num)
        parse_page(url)
    pool.submit(get_html)
    pool.map(get_html, [num*10 for num in range(312)])
    pool.shutdown()
    file.close()


