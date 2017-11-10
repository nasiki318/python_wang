#! /usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from os import  path
import jieba.analyse
import matplotlib.pyplot as plt
from wordcloud import WordCloud,ImageColorGenerator
from PIL import Image,ImageSequence
import numpy as np
start_time = datetime.datetime.now()
d=path.dirname(__file__)
filename='jingdong.txt'
with open(filename) as f:
    mytext=f.read()

jieba_text=jieba.analyse.textrank(mytext,topK=50,withWeight=True)
keywords = dict()
for i in jieba_text:
    keywords[i[0]]=i[1]
print(keywords)
del keywords['还有']
del keywords['应该']
del keywords['觉得']
del keywords['有点']
del keywords['感觉']
del keywords['越做越']
del keywords['没有']

graph = np.array(Image.open(path.join(d,'1.jpg')))
wc = WordCloud(font_path='字体管家楷体.ttf',background_color='white',max_words=50,mask=graph)
wc.generate_from_frequencies(keywords)

plt.imshow(wc)
plt.axis("off")
plt.show()

end_time = datetime.datetime.now()
print('程序耗时 ', end_time - start_time)
