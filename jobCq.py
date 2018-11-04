#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@python: v3.7
@author:thinking
@file: jobCq.py
@time: 2018/10/16  18:42
"""
import csv
import time

import requests
from bs4 import BeautifulSoup
import re

header ={
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "User-Agent": "IP"
    }
def parse(url, writer):
    try:
        response = requests.get(url, headers = header)
        response.encoding = 'gb2312'
        html = response.text
    except:
        pass
    else:
        bsobj = BeautifulSoup(html, 'lxml')
        job_li = bsobj.select('.job_list_li')
        for job in job_li:
            job_detail = job.select('.li_title')[0]
            job_descr = job_detail.a['onmouseover']
            job_item = re.findall(re.compile(r'<td>(.*?)</td>', re.S | re.M), job_descr)
            job_wage = job_item[0]
            job_site = job_item[1]
            job_sex = job_item[2]
            job_edu = job_item[3]
            job_type = job_item[4]
            job_welf = job_item[5]
            job_name = job_detail.a.string
            job_compa = job.select('.li_company > a')[0].string.replace(" ",'').replace("\r","").replace("\n", '')
            job_time = job.select('.li_time')[0].string.replace(" ",'').replace("\r","").replace("\n", '')
            job_url = 'http://www.kq36.com'+ job_detail.a['href']
            job_list = [job_name, job_compa, job_wage,job_welf, job_site, job_sex, job_edu, job_type, job_time, job_url]
            print(job_list)
            writer.writerow(job_list)
if __name__=='__main__':

    file = open('jobs of medical.csv','w', encoding='UTF8', newline='')
    writer = csv.writer(file)
    for num in range(1, 50):
        url =  'http://www.kq36.com/job_list.asp?page={page}&Provinceid={pid}&Cityid={cid}&Job_ClassI_Id={jid}'\
            .format(page = num , pid=27,cid=271,jid=2)
        parse(url,writer)
        time.sleep(3)
    file.close()
