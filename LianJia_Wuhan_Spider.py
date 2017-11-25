#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import requests
import random
import xlsxwriter
from lxml import etree
start_time = datetime.datetime.now()

user_agent_list = [
        'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1',
        'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11'
            ]
user_gaent = random.choice(user_agent_list)

headers = {
'Referer': 'https://wh.lianjia.com/ershoufang/pg2/',
'User-Agent': user_gaent
}


def get_url_list(page):
    url_list = []
    for i in range(1,page+1):
        url = 'https://wh.lianjia.com/ershoufang/pg%s/'%i
        response=requests.get(url,headers=headers).text
        html=etree.HTML(response)
        house_url=html.xpath('/html/body/div[4]/div[1]/ul/li/a/@href')
        url_list +=house_url

    return url_list


def get_contents(page):
    workbook = xlsxwriter.Workbook('wuhan_ershoufang.xlsx')
    worksheet = workbook.add_worksheet()
    xlsx_title = ['标题', '户型', '位置', '小区名', '面积', '单价（元/平米）', '总价(万)']
    c = 0
    for x in xlsx_title:
        worksheet.write(0, c, x)
        c += 1
    row=1

    for i in get_url_list(page):
        try:
            response = requests.get(i,headers=headers).text
            html = etree.HTML(response)
            title = html.xpath('/html/body/div[3]/div/div/div[1]/h1/text()')
            room_info = html.xpath('/html/body/div[5]/div[2]/div[3]/div[1]/div[1]/text()')
            house_area = html.xpath('/html/body/div[5]/div[2]/div[4]/div[2]/span[2]/a/text()')
            village_name = html.xpath('/html/body/div[5]/div[2]/div[4]/div[1]/a[1]/text()')
            housing_area = html.xpath('/html/body/div[5]/div[2]/div[3]/div[3]/div[1]/text()')
            singe_price = html.xpath('/html/body/div[5]/div[2]/div[2]/div[1]/div[1]/span/text()')
            whole_price = html.xpath('/html/body/div[5]/div[2]/div[2]/span[1]/text()')
            print(title,room_info,house_area,village_name,housing_area,singe_price,whole_price)
            worksheet.write(row,0,title[0])
            worksheet.write(row,1,room_info[0])
            worksheet.write(row, 2,str(house_area))
            worksheet.write(row, 3,village_name[0])
            worksheet.write(row, 4,housing_area[0])
            worksheet.write(row, 5,singe_price[0])
            worksheet.write(row, 6,whole_price[0])
            row +=1
        except:
            pass

    workbook.close()


get_contents(1)

end_time = datetime.datetime.now()
print('程序耗时 ', end_time - start_time)