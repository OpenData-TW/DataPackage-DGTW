from bs4 import BeautifulSoup as BS4
import json

with open('list.html', 'r', encoding='utf-8') as node_f:
    node_file = BS4(node_f, 'lxml')

node_list = node_file.find_all('div', class_ = 'directory_list')

for i in node_list:
    print(i.h4.text + ', ' + i.a.get('href') + ', ' + i.a.text)