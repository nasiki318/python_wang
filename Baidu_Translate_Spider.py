#! /usr/bin/env python
# -*- coding: utf-8 -*-
import requests,json,os
from bs4 import BeautifulSoup
from urllib import *
word = input('请输入一个单词:')
def get_url_contents():
    try:
        headers = {
            'Referer': 'http://fanyi.baidu.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
        }
        data = {
            'from': 'en',
            'to': 'zh',
            'query': word,
            'transtyp': 'translang',
            'simple_means_flag': '3'
        }
        url='http://fanyi.baidu.com/v2transapi'
        r=requests.post(url,data=data,headers=headers).text
        r=json.loads(r)

        res=(r['dict_result']['simple_means']['symbols'])
        for i in res:
            result=i
        return result
    except:
        print('这个单词不存在')

def get_means():
    try:
        content_info=[word]

        contents=get_url_contents()
        translation=contents['parts']

        nane_info=('英 [%s]   美 [%s]'%(contents['ph_en'],contents['ph_am']))
        content_info.append(nane_info)
        for n in translation:
            means='%s %s' %(n['part'],';'.join(n['means']))
            content_info.append(means)
        # content_info=['%s \n' % x for x in content_info]   列表生成式没有解决换行问题！！！\n
        for i in content_info:
            print(i)

        en_url = 'http://fanyi.baidu.com/gettts?lan=en&text=%s&spd=3&source=web'%word
        uk_url = 'http://fanyi.baidu.com/gettts?lan=uk&text=%s&spd=3&source=web'%word
        uk_mp3=requests.get(uk_url).content
        en_mp3=requests.get(en_url).content
        save_words(content_info, word,en_mp3,uk_mp3)
    except :
        print('请检查后再输入！')

def save_words(content_info,word,en_mp3,uk_mp3):
    #如果不存在，创建文件夹，注意if不检查后缀，有word.txt也算存在
    if not os.path.exists(word):
        os.makedirs(word)
    file_path=os.path.join(word,'%s.txt'%word)
    #写入数据编码UTF-8否则报错
    with open(file_path,'w',encoding='utf-8') as f:
        f.writelines(content_info)
    en_path=os.path.join(word,'%sen.mp3'%word)
    uk_path=os.path.join(word,'%suk.mp3'%word)
    with open(uk_path,'wb') as f :
        f.write(uk_mp3)
    with open(en_path,'wb') as f :
        f.write(en_mp3)

get_means()
