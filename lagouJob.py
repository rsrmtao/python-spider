#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@python: v3.7
@author:thinking
@file: lagouJob.py
@time: 2018/10/07  21:46
"""
import csv
import requests
from lxml import etree
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
import  time
from pyquery import PyQuery as pq

def parse_page(browser, writer):
    doc = browser.page_source
    selector = etree.HTML(doc)
    joblist = selector.xpath('//li[@class="con_list_item default_list"]')
    for list in joblist:
        # print(list)
        comname = list.xpath('div//div[@class="company_name"]/a/text()')[0]
        comurl = list.xpath('div//div[@class="company_name"]/a/@href')[0]
        jobname = list.xpath('div//h3/text()')[0]
        joburl = list.xpath('div//a[@class="position_link"]/@href')[0]
        comdescr = list.xpath('div//div[@class="industry"]/text()')[0].replace("\n","").replace(" ","")
        jobsalary = list.xpath('div//div[@class="li_b_l"]/span[@class="money"]/text()')[0].replace("\n","").replace(" ","")
        requires = list.xpath('div//div[@class="li_b_l"]/text()')
        jobrequ = ""
        for word in requires:
            word = word.replace("\n","").replace(" ","")
            if word !="":
                jobrequ = jobrequ + word
        jobtime = list.xpath('div//span[@class="format-time"]/text()')[0]
        joblist = [comname,comurl,jobname,joburl, comdescr, jobsalary, jobrequ, jobtime]
        writer.writerow(joblist)
        print(comname,comurl,jobname,joburl, comdescr, jobsalary, jobrequ, jobtime)
if __name__=="__main__":
    file = open('social jobs of lagou.csv', 'a', newline='', encoding="UTF8")
    writer = csv.writer(file)
    writer.writerow(["公司","公司介绍", "职位名称","职位网址","公司标签", "薪水", "工作经验","发布时间"])
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    browser = webdriver.Chrome('D:\Program\chromedriver\chromedriver.exe', options=options)
    wait = WebDriverWait(browser, 2)
    url = "https://www.lagou.com/jobs/list_python?px=default&city=深圳#filterBox"
    browser.get(url)
    input = wait.until(ec.presence_of_element_located((By.CSS_SELECTOR,'#keyword')))
    submit = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR,'#submit')))
    input.clear()
    input.send_keys('python')
    submit.click()
    time.sleep(2)
    doc = browser.page_source
    selector = etree.HTML(doc)
    num = selector.xpath('//ul[@class="order"]//span[@class="span totalNum"]/text()')[0]
    num = int(num)
    # wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR, '#s_position_list > div.item_con_pager > div > span.pager_next')))
    for i in range(num):
        parse_page(browser, writer)
        print("".center(40,"-"))
        clickpage = wait.until(ec.element_to_be_clickable((By.CSS_SELECTOR,'#order > li > div.item.page > div.next_disabled.next')))
        clickpage.click()
        time.sleep(2)
    file.close()

