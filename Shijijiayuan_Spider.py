#! /usr/bin/env python
# -*- coding: utf-8 -*-

import json
import re
import datetime
import xlsxwriter
from selenium import webdriver
from lxml import etree
import requests
starttime = datetime.datetime.now()
chromePath = r'D:\chromedriver\chromedriver.exe'
browser = webdriver.Chrome(executable_path=chromePath)
browser.get('http://www.jiayuan.com/')
browser.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[3]').clear()
browser.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[3]').send_keys('13260676629')
browser.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[4]').clear()
browser.find_element_by_xpath('//*[@id="hder_login_form_new"]/input[4]').send_keys('123456789o')
browser.find_element_by_xpath('//*[@id="hder_login_form_new"]/button').click()
cookies = browser.get_cookies()
req = requests.Session()
for cookie in cookies:
    req.cookies.set(cookie['name'], cookie['value'])

headers = {'Referer': 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=2:27.35,23:1&sn=default&sv=1&p=1&pt=947&ft=off&f=select&mt=d',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

max_page = int(input('请输入要获取的页数：'))


def get_user_id(page):
    data = {
        'sex': 'f',
        'key': '',
        'stc': '2: 18.25',
        'sn': 'default',
        'sv': '1',
        'p': page,
        'f': 'select',
        'listStyle': 'bigPhoto',
        'pri_uid': '170071932',
        'jsversion': 'v5',
        'Referer': 'http://search.jiayuan.com/v2/index.php?key=&sex=f&stc=2:27.35,23:1&sn=default&sv=1&p=1&pt=947&ft=off&f=select&mt=d',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    user_id = []
    url = 'http://search.jiayuan.com/v2/search_v2.php'
    response = requests.post(url, data=data).text
    res = json.loads(response[11:-13])
    for i in res['userInfo']:
        user_id.append(i['realUid'])
    return user_id[1:]


excl_title = ['昵称','ID','年龄','学历','身高','购车','月薪','住房','体重','星座','民族','属相','血型','吸烟','饮酒','饮食习惯','家务','宠物','择偶年龄','择偶身高','择偶学历','择偶婚姻状况','择偶民族']
row = 0
col = 0
workbook = xlsxwriter.Workbook('shijijiayuan.xlsx')
worksheet = workbook.add_worksheet()
for x in excl_title:
    worksheet.write(row, col, x)
    col += 1
r = 1


def get_usr_info(page):

    for i in get_user_id(page):
        try:
            url = 'http://www.jiayuan.com/%s' % i
            response = req.get(url, headers=headers).text
            html = etree.HTML(response)
            name_pat = '<h4>(.*?)<span>ID:'
            name = re.findall(name_pat, response)
            age = html.xpath('//h6[@class="member_name"]/text()')
            info = html.xpath('//div[@class="fl pr"]/em/text()')
            firend_info = html.xpath('//div[@class="ifno_r_con"]/text()')
            behavor = html.xpath('//div[@class="ifno_r_con"]/em/text()')
            print(info)
            global r
            worksheet.write(r, 0, name[0])
            worksheet.write(r, 1, i)
            worksheet.write(r, 2, age[0])
            worksheet.write(r, 3, info[0])
            worksheet.write(r, 4, info[1])
            worksheet.write(r, 5, info[2])
            worksheet.write(r, 6, info[3])
            worksheet.write(r, 7, info[4])
            worksheet.write(r, 8, info[5])
            worksheet.write(r, 9, info[6])
            worksheet.write(r, 10, info[7])
            worksheet.write(r, 11, info[8])
            worksheet.write(r, 12, info[9])
            worksheet.write(r, 13, behavor[0])
            worksheet.write(r, 14, behavor[1])
            worksheet.write(r, 15, behavor[3])
            worksheet.write(r, 16, info[10])
            worksheet.write(r, 17, info[11])

            worksheet.write(r, 18, firend_info[0])
            worksheet.write(r, 19, firend_info[1])
            worksheet.write(r, 20, firend_info[3])
            worksheet.write(r, 21, firend_info[5])
            worksheet.write(r, 22, firend_info[2])

            r = r+1
        except:
            pass


for m in range(max_page):
    get_usr_info(m)
workbook.close()
endtime = datetime.datetime.now()

print(("程序耗时 ", endtime-starttime))
