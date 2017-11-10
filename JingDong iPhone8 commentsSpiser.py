#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import requests
import json
start_time = datetime.datetime.now()

headers = {
    'referer': 'https://item.jd.com/5089273.html',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}


def get_comments(page):
    url = 'https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv15278&productId=5089273&score=0&sortType=5&page='+str(page)+'&pageSize=10&isShadowSku=0&rid=0&fold=1'
    r = requests.get(url, headers=headers).text
    r=r[27:-2]
    response=json.loads(r)
    return response["comments"]


def write_txt(page):
    for i in range(10):
        with open('jingdong.txt','a') as f :
            f.write(get_comments(page)[i]['content'])


for n in range(20):
    write_txt(n)


end_time = datetime.datetime.now()
print('程序耗时 ', end_time - start_time)
