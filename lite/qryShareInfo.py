#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@python: v3.7
@author:thinking
@file: qryShareInfo.py
@time: 2019/04/17  22:23
"""
import csv
import re
import urllib.request
import urllib.parse
import time, random
headers = {
"Origin": "http://www.phsciencedata.cn",
"Referer": "http://www.phsciencedata.cn/Share/qryShareInfo.jsp",
"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
}
form = {
    "page": 1
}
total = 1+1
csvfile = open(r'E:\1.csv', 'w', encoding='UTF-8',newline='')
writer = csv.writer(csvfile)
lst = ['DT_CREATE','NAME','STATUS','REALNAME','ENGNAME','ismail','ID','ACCEPTED','USERNAME','BBSID','PIC_STATE','TYPE','TITLE','ORG']
writer.writerow(lst)
for i in range(1, total):
    form = {
        "page": i
    }
    url = "http://www.phsciencedata.cn/Share/shareGetList/"
    data = bytes(urllib.parse.urlencode(form), encoding='utf8')
    req = urllib.request.Request(url=url, data=data, headers=headers, method='POST')
    response = urllib.request.urlopen(req)
    print(response.getcode())
    if response.getcode()!=200:
        i -= 1
        continue
    orgin = response.read().decode('utf-8')
    print(orgin)

    reg = r'{(.*?)}'
    patten = re.compile(reg)
    items = re.findall(patten, orgin)
    for item in items:
        # print(item)
        item = item.replace(r'\"', '')
        print(item)
        reg = r'DT_CREATE:(.*?),NAME:(.*?),STATUS:(.*?),REALNAME:(.*?),ENGNAME:(.*?),ismail:(.*?),ID:(.*?),ACCEPTED:(.*?),USERNAME:(.*?),BBSID:(.*?),PIC_STATE:(.*?),TYPE:(.*?),TITLE:(.*?),ORG:(.*?)'
        patten = re.compile(reg, re.S|re.M)
        values = re.findall(patten, item)
        if values:
            # print(type(values))
            # print(values)
            # print(type(values[0]))
            # print(list(values[0]))
            writer.writerow(list(values[0]))
    time.sleep(random.randint(1, 20))
csvfile.close()
