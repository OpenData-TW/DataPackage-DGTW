# data.gov.tw/node to .json
# https://data.gov.tw/dataset/28387
# 高中職以上學校學生就學貸款統計
# https://data.gov.tw/dataset/6287
# 大專校院校地校舍面積統計 + 活化應用

import requests
from bs4 import BeautifulSoup as BS4
import json
import sys
import os
import pprint
import re
import node
node_list = node.node_list

# get_node = 6179 72311 78625
# node_list = [72311]

# rename labels
label_list = {
    '資料集描述': 'DESC',
    '主要欄位說明': 'SCHEMA',
    '提供機關': 'AGENCY',
    '提供機關聯絡人': 'AGENCY_CONTACT',
    '更新頻率': 'UPDATE_FREQ',
    '授權方式': 'LICENCE',
    '計費方式': 'CHARGE',
    '上架日期': 'DATE_PUBLISH',
    '資料集類型': 'DATA_TYPE',
    '詮釋資料更新時間': 'DATE_UPDATE_META',
    '關鍵字': 'KEYWORDS',
    '主題分類': 'CATEGORY',
    '服務分類': 'SERVICE_TYPE',
    '相關網址': 'SOURCE_URL',
    '備註': 'NOTES',
    '瀏覽次數': 'VIEWS',
    '下載次數': 'DOWNLOAD',
    '意見數': 'COMMENTS',
    '檔案格式': 'RES_FILETYPE',
    '編碼': 'RES_ENCODE',
    '資料量': 'REC_COUNT',
    '資源網址': 'RES_URL',
    '資源描述': 'RES_DESC',
    '資料資源更新時間': 'RES_DATE_UPDATE_META',
    'CSV 下載': 'CSV',
    'XLSX 下載': 'XLSX',
    'ODS 下載': 'ODS',
    'XML 下載': 'XML',
    'JSON 下載': 'JSON',
    '活化應用': 'APP',
    '創作者': 'CREATOR',
    '摘要': 'EXCERPT'

}


def res_rename(label_name):
    try:
        return label_list[label_name]
    except:
        return label_name


# def get_dq(node_number):
# 	res_donwnlaod = {}
#     dq_url = 'https://quality.data.gov.tw/dq_event.php?nid=' + node_number
#     reutrn res_donwnlaod


def clean_name(title):
    replace_list = {
        '/': '_',
        ':': '_',
        '\t': '',
        '\r': '',
        '>': '&gt;',
        '<': '&lt;',
    }
    for i, k in replace_list.items():
        title = title.replace(i, k)
    return title


def get_json(get_node, c=True):
    get_url = 'https://data.gov.tw/dataset/' + str(get_node)

    try:
        node_file = requests.get(get_url)
        node_file = BS4(node_file.content.decode('utf-8'), 'lxml')
        json_title = node_file.find('h1', 'node-title').text
        if json_title.strip() != '找不到網頁':
            node_file = node_file.find('div', 'node-content')

            node_label = []

            # get APP list
            node_app_list = []
            app_count = 0
            node_app = node_file.find_all('div', id = re.compile('node-.*'))
            app_count = len(list(node_app))
            if app_count:
                print('app : ' + str(app_count))
            app_name = ['EXCERPT', 'CREATOR']
            if node_app:
                for a in node_app:
                    node_app_temp = {}
                    node_app_temp['NODE'] = a.h2.a.get('href')
                    node_app_temp['TITLE'] = a.h2.text
                    name_count = 0
                    b = a.find_all('div', 'field-item')
                    for c in b:
                        node_app_temp[app_name[name_count % 2]] = c.text.strip()
                        name_count += 1
                    node_app_list.append(node_app_temp)

            # get the keywords list
            node_keywords = node_file.find_all('div', 'tag-wrapper')
            node_key_list = []
            if node_keywords:
                for k in node_keywords:
                    node_key_list.append(k.text)
            else:
                node_key_list = []

            # get labels
            node_label_temp = node_file.find_all('div', 'field-label')
            res_count = 0
            res_list = [1]

            for k, i in enumerate(node_label_temp):
                i = i.text.replace('\xa0', '').replace(':', '')
                i = res_rename(i)
                if '資料資源' == i:
                    node_label.append('RESOURCE-' + str(res_count))
                    res_count += 1
                    res_list.append(len(node_label) - 1)
                elif 'SCHEMA' == i and k > 4:
                    node_label.append('RESOURCE-' + str(res_count))
                    node_label.append(i)
                    res_count += 1
                    res_list.append(len(node_label) - 2)
                else:
                    node_label.append(i)

                if 'KEYWORDS' == i and len(node_keywords) > 0:
                    for j in range(len(node_keywords)):
                        node_label.append('KEYWORD-' + str(j))
                if 'AGENCY' == i:
                    res_list.append(len(node_label) - 1)

            node_label.append('Stats')

            # for k in range(len(list(node_app))):
            #     node_label.remove('CREATOR')
            #     node_label.remove('EXCERPT')


            # get contents
            node_content = []
            node_content_temp = node_file.find_all('div', 'field-item')
            for i in node_content_temp:
                i_v = i.text.replace('\xa0', '').replace('\n', '')
                node_content.append(i_v)

            # split stats line
            stats = node_content[-1].split(' ')
            for i in range(3):
                node_label.append(res_rename(stats[i * 2].strip(':')))
                node_content.append(stats[i * 2 + 1])

            # print out
            # if len(node_label) == len(node_content):
            #     for k, i in enumerate(node_content):
            #         print(str(k) + ' : ' + node_label[k] + ' :: ' + i)

            node_matrix = dict()

            node_matrix['TITLE'] = json_title
            node_matrix['NODE'] = str(get_node)
            # 0-3

            for k in range(res_list[0], res_list[1]):
                if 'SCHEMA' == node_label[k] and '、' in node_content[k]:
                    node_content[k] = node_content[k].split('、')
                node_matrix[node_label[k]] = node_content[k]

            # AGENCY to APP pos
            for k in range(res_list[-1], len(node_label)):
                if 'KEYWORD' in node_label[k]:
                    if 'KEYWORDS' == node_label[k]:
                        if node_key_list:
                            node_content[k] = node_key_list
                            node_matrix[node_label[k]] = node_content[k]
                        else:
                            node_matrix[node_label[k]] = ''
                            # node_content.insert(k, '')
                elif 'APP' in node_label[k]:
                    node_content[k] = node_app_list
                    node_matrix[node_label[k]] = node_content[k]
                else:
                    node_matrix[node_label[k]] = node_content[k]

            # print('resources :: -----------------------------------')
            res_matrix = []
            for k in range(1, len(res_list) - 1):
                res_temp = {}
                for l in range(res_list[k] + 1, res_list[k + 1]):
                    res_temp[node_label[l]] = node_content[l]

                res_matrix.append(res_temp)

            node_matrix['RESOURCE'] = res_matrix
            json_title = clean_name(json_title)
            json_file = str(get_node) + '. ' + node_matrix['AGENCY'] + '_' + json_title.strip() + '.json'

            # remove extra APP content
            if app_count:
                del node_matrix['CREATOR']
                del node_matrix['EXCERPT']

            # check resources status
            # node_res_download = get_dq(node_matrix['NODE'])

            if c:
                with open(json_file, 'w', encoding='utf-8') as j_file:
                    json.dump(node_matrix, j_file, ensure_ascii=False, indent=4)
                    return json_file
            else:
                pprint.pprint(node_matrix, indent=4)
                return '---------- done -----------'
        else:
            return str(get_node) + ' does not exist'
    except requests.exceptions.SSLError as e:
        print('connection error')
        return 'file error'

# main ----------------------------------------
# get_json(node_list)


if len(sys.argv) == 1:
    print('Node : ' + str(len(node_list)))
    for node_item in node_list:
        json_name = get_json(node_item)
        if os.path.exists(json_name):
            print(json_name)
        else:
            print(json_name + ' :: error')
elif len(sys.argv) == 2:
    get_json(int(sys.argv[1]), c=False)
elif len(sys.argv) == 3:
    get_json(int(sys.argv[1]), c=sys.argv[2])
else:
    print('syntax : get [node_id] [True|False]')
