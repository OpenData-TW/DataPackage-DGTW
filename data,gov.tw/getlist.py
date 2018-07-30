# Get all data list from data.gov.tw
# query_url = https://data.gov.tw/datasets/search?qs=dtid:22029
#
# data list download at :
# <div class="export">
# <a href="/datasets/export/csv?type=dataset&amp;order=pubdate&amp;qs=&amp;uid=&amp;tag=dtid%3A22029" class="ff-icon ff-icon-csv">csv</a>
# <a href="/datasets/export/xml?type=dataset&amp;order=pubdate&amp;qs=&amp;uid=&amp;tag=dtid%3A22029" class="ff-icon ff-icon-xml">xml</a>
# <a href="/datasets/export/json?type=dataset&amp;order=pubdate&amp;qs=&amp;uid=&amp;tag=dtid%3A22029" class="ff-icon ff-icon-json">json</a>
# </div>
#


import json
import csv
import requests
import re
from bs4 import BeautifulSoup as BS4

president = ['總統府', '國安會', '國史館', '中央研究院']
president_dtid = ['672', '800', '723', '739']

executive = ['內政部', '外交部', '國防部', '財政部', '教育部', '法務部', '經濟部', '交通部', '勞動部', '行政院農業委員會', '衛生福利部', 
             '行政院環境保護署', '文化部', '科技部', '國家發展委員會', '行政院大陸委員會', '金融監督管理委員會', '行政院海岸巡防署', '僑務委員會',
             '國軍退除役官兵輔導委員會', '原住民族委員會', '客家委員會', '行政院公共工程委員會', '行政院主計總處', '行政院人事行政總處', '中央銀行',
             '國立故宮博物院', '行政院原子能委員會', '中央選舉委員會', '公平交易委員會', '國家通訊傳播委員會', '飛航安全調查委員會',
             '行政院不當黨產處理委員會', '福建省政府', '台灣省政府', '臺灣省諮議會']
executive_dtit = ['428', '429', '430', '431', '432', '440', '442', '443', '466', '497', '493', '509', '498', '517', 
                  '489', '491', '499', '507', '504', '484', '486', '503', '506', '502', '518', '519', '495', '487',
                  '488', '496', '500', '508', '737', '16720', '847', '807', '505']

legislature = ['立法院']
legislature_dtid = ['797']

judicial = ['司法院', '公務員懲戒委員會', '智慧財產法院', '最高法院', '最高行政法院', '法官學院', '福建連江地方法院', '福建金門地方法院', 
            '福建高等法院金門分院', '臺中高等行政法院', '臺北高等行政法院', '臺灣高等法院', '高雄高等行政法院']
judicial_dtid = ['748', '832', '798', '806', '772', '837', '821', '827', '818', '770', '802', '786', '773']

control = ['監察院', '審計部']
control_dtit = ['736', '691']

examination = ['考試院', '考選部', '銓敘部', '公務人員保障暨培訓委員會', '公務人員退休撫卹基金監理委員會']
examination_dtit = ['729', '826', '820', '842', '728']

ncdr = ['國家災害防救科技中心']
ncdr_dtit = ['490']

county = ['臺北市', '新北市', '桃園市', '臺中市', '台南市', '高雄市', '新竹縣', '苗栗縣', '南投縣', '彰化縣', '雲林縣',
          '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣', '台東縣', '澎湖縣', '連江縣', '金門縣', '基隆市', '新竹市', '嘉義市']
county_dtid = ['22003', '22026', '22030', '22027', '22028', '22029', '22005', '22007', '22011', '22010', '22012',
               '22013', '22019', '22020', '22021', '22022', '22023', '22025', '22024', '22001', '22006', '22014']

dtid_url = 'https://data.gov.tw/datasets/search?qs=dtid:428'
node_file = requests.get(dtid_url)
node_file = BS4(node_file.content.decode('utf-8'), 'lxml')

data_count = node_file.find(string=re.compile('共\d*筆')).split('，')
print(data_count[0].replace('共', '').replace('筆', ''))

node_list = node_file.find('div', 'export')

node_list = node_list.find_all('a')
node_download = []
for i in node_list:
    node_download.append(i.get('href'))

node_download_url = 'https://data.gov.tw/' + node_download[0]
# r = requests.get(node_download_url)
#
# with open('list_飛航安全調查委員會.csv', 'wb') as f:
#     for chunk in r.iter_content(chunk_size=1024):
#         if chunk: # filter out keep-alive new chunks
#             f.write(chunk)


