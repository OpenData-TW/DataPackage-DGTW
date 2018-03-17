# get - 新北市開放資料
# http://data.ntpc.gov.tw/od/detail?oid=A9D43291-097E-4624-8A6E-683FD58FC1AD
#
#

import json
import requests
from bs4 import BeautifulSoup as BS4
from bs4 import Comment

base_url = 'http://data.ntpc.gov.tw/od/detail?oid='
oid = 'A9D43291-097E-4624-8A6E-683FD58FC1AD'
# oid = '54A507C4-C038-41B5-BF60-BBECB9D052C6'

node_file = requests.get(base_url + oid)
node_file = BS4(node_file.content.decode('utf-8'), 'lxml')

node_file = node_file.find('div', id='tab1')

node_label_tmp = node_file.find_all('th')
node_cont_tmp = node_file.find_all('td')


def strip_all(a_string):
    a_string = a_string.strip()
    special_chars = ['\n', '\t', '\r', ' ']
    for i in special_chars:
        a_string = a_string.replace(i, '')
    return a_string


node_label = []
for i in node_label_tmp:
    node_label.append(i.text)
node_label.insert(1, '平均評分')


node_cont = []

for i in node_cont_tmp:
    j = strip_all(i.text)
    node_cont.append(j.replace('平均評分：', ''))

for k, i in enumerate(node_cont):
    print(str(k) + ' - ' + node_label[k] + ' :: ' + i)


# Get Comments and data
comments = node_file.find_all(string=lambda text : isinstance(text, Comment))
for i in comments:
    j = i.replace('\r\n\t\t', '').replace(' ', '').strip()
    print(j.replace('	', '').replace('</p></td></tr>', '').replace('<tr><th><p>', '').replace('</th><td><p>', '').split('</p>'))
