import requests
from bs4 import BeautifulSoup as BS4
import csv


node_url = 'http://opendata.e-land.gov.tw/dataset'
node_url2 = 'http://opendata.e-land.gov.tw/dataset?page='

node_label = []
for i in range(1, 19):
    node_url = node_url2 + str(i)
    node_file = requests.get(node_url, )
    node_file = BS4(node_file.content.decode('utf-8'), 'lxml')
    node_title = node_file.find_all('li', class_ = 'dataset-item')

    for j in node_title:
        node_label_temp = []
        j_get = j.find('div', class_ = 'dataset-content')
        j_text = j.find('div', class_ = 'dataset-content').text.split('\n\n')
        node_label_temp.append(j_text[1].replace(', ', '_'))
        node_label_temp.append(j_text[2].replace(', ', '_'))
        node_label_temp.append(j_get.a.get('href'))
        node_label.append(node_label_temp)

    # node_list = node_file.find_all('ul', class_ = 'dataset-resources')
    # for j, k in enumerate(node_list):
    #     node_list = k.find('li')
    #     node_label[10 * (i-1) + j].append(node_list.a.get('href'))


with open('yilan.2018.03.20.OD.csv', 'w', encoding = 'utf-8', newline='') as csvfile:
    node_write = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i in node_label:
        node_write.writerow(i)