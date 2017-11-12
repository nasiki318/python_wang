#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import requests
import random
from lxml import etree
import xlsxwriter
from selenium import webdriver
start_time = datetime.datetime.now()

chromePath='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
browser=webdriver.Chrome(executable_path=chromePath)
browser.get('https://www.douban.com/accounts/login?source=main')
browser.find_element_by_xpath('//*[@id="email"]').clear()
browser.find_element_by_xpath('//*[@id="email"]').send_keys('931727778@qq.com')
browser.find_element_by_xpath('//*[@id="password"]').clear()
browser.find_element_by_xpath('//*[@id="password"]').send_keys('123456789o')
browser.find_element_by_xpath('//*[@type="submit"]').submit()
cookies=browser.get_cookies()
req=requests.Session()
for cookie in cookies:
    req.cookies.set(cookie['name'],cookie['value'])

user_agent_list = [
        'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
        'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11'
            ]
user_gaent = random.choice(user_agent_list)

headers = {
'Referer': 'https://book.douban.com/review/best/?start=0',
'User-Agent': user_gaent
}


def get_url_list(page_number):
    url_list = []
    for i in range(1, page_number+1):
        url = 'https://book.douban.com/review/best/?start='+str(i*20)
        url_list.append(url)
    return url_list


def get_contents(page_number):
    book_contents_url = []
    for x in get_url_list(page_number):
        response = req.get(x)
        html = etree.HTML(response.text)
        book_url = html.xpath('//a[@class="title-link"]/@href')
        book_contents_url += book_url
    return book_contents_url

title = ['评论人','标题','书名']
workbook = xlsxwriter.Workbook('Douban comments.xlsx')
worksheet = workbook.add_worksheet()
c = 0
for y in title:
    worksheet.write(0,c,y)
    c += 1


def get_comment_text(page_number):
    row = 1
    col = 0
    for n in get_contents(page_number):
        response = req.get(n).text
        html = etree.HTML(response)
        comment_name = html.xpath('//span [@property="v:summary"]/text()')
        author = html.xpath('//span [@property="v:reviewer"]/text()')
        book_name = html.xpath('//header [@class="main-hd"]/a[2]/text()')
        comment = html.xpath('//*[@id="link-report"]/div/p/text()')
        comments = html.xpath('//div [@id="link-report"]/div/text()')
        comment = comment+comments
        for o in comment:
            with open('%s.txt'%book_name,'a',encoding='utf-8') as f :
                f.write(o)
        #print(author,comment_name,book_name,comment)
        worksheet.write(row,col,author[0])
        worksheet.write(row,col+1,comment_name[0])
        worksheet.write(row, col+2,book_name[0])
        row += 1

    workbook.close()


get_comment_text(3)

end_time = datetime.datetime.now()
print('程序耗时 ', end_time - start_time)
