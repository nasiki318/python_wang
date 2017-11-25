#! /usr/bin/env/python
# -*- coding: utf-8 -*-
import datetime
import requests
import re
import time
import json
from selenium import webdriver
start_time = datetime.datetime.now()


def login():
    browser = webdriver.Chrome(executable_path='C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
    browser.get('https://qzone.qq.com/')
    browser.switch_to.frame('login_frame')
    browser.find_element_by_xpath('//*[@id="switcher_plogin"]').click()
    browser.find_element_by_xpath('//*[@id="u"]').clear()
    browser.find_element_by_xpath('//*[@id="u"]').send_keys('931727778')
    browser.find_element_by_xpath('//*[@id="p"]').clear()
    browser.find_element_by_xpath('//*[@id="p"]').send_keys('zhenmafan..')
    browser.find_element_by_xpath('//*[@id="login_button"]').click()
    time.sleep(5)
    browser.find_element_by_xpath('//*[@id="QM_Profile_Mood_Cnt"]').click()
    cookies = browser.get_cookies()
    cookie = {}
    for i in cookies:
        cookie[i['name']] = i['value']
    def getGTK(cookie):
        """ 根据cookie得到GTK """
        hashes = 5381
        for letter in cookie['p_skey']:
            hashes += (hashes << 5) + ord(letter)

        return hashes & 0x7fffffff
    html = browser.page_source
    g_qzonetoken = re.search(r'window\.g_qzonetoken = \(function\(\)\{ try\{return (.*?);\} catch\(e\)',html)

    gtk = getGTK(cookie)

    return (cookie, gtk, g_qzonetoken.group(1))


cookie, gtk, qzonetoken = login()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'referer': 'https://qzs.qq.com/qzone/app/mood_v6/html/index.html',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.8'
}


def get_contents(page):
    url = 'https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin=1679842437'

    for i in range(page):
        try:
            params = {
                'uin': 1679842437,
                'inCharset': 'utf-8',
                'outCharset': 'utf-8',
                'sort': '0',
                'pos': i*10,
                'num': '20',
                'code_version': '1',
                'format': 'jsonp',
                'need_private_comment': '1',
                'g_tk': gtk,
                'qzonetoken': qzonetoken
            }
            r = requests.session()
            response = r.get(url, headers=headers, params=params, cookies=cookie).text
            res = json.loads(response[10:-2])
            for x in res['msglist']:

                message_content = x['content']
                creat_time = x['createTime']
                source_name = x['source_name']
                comment_list = []
                try:
                    for y in range(len(x['commentlist'])):
                        commenter_time = x['commentlist'][y]['createTime']
                        commenter_name = x['commentlist'][y]['name']
                        commenter_content = x['commentlist'][y]['content']
                        comment_list.append(commenter_time)
                        comment_list.append(commenter_name)
                        comment_list.append(commenter_content)
                        for o in range(len(x['commentlist'][y]['list_3'])):
                            response_name = x['commentlist'][y]['list_3'][o]['name']
                            response_content = x['commentlist'][y]['list_3'][o]['content']

                            comment_list.append(response_name)
                            comment_list.append(response_content)

                    print(message_content,   creat_time,   source_name,   comment_list)
                except:
                    print(message_content,   creat_time,   source_name  ,'获取评论出错')
                    pass
        except:
            print('已全部爬完。')
            break

get_contents(100)

end_time = datetime.datetime.now()
print('程序耗时 ', end_time - start_time)
