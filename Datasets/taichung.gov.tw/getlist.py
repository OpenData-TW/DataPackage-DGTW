from bs4 import BeautifulSoup as BS4
import json

with open('list.html', 'r', encoding='utf-8') as node_f:
    node_file = BS4(node_f, 'lxml')

node_list = node_file.find_all('li')

for i in node_list:
    print(i.a.text + ', http://data.taichung.gov.tw/wSite/' + i.a.get('href'))
