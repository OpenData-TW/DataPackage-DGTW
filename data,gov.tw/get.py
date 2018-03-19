# data.gov.tw/node to .json
# https://data.gov.tw/dataset/28387
# 高中職以上學校學生就學貸款統計
#
#

import requests
from bs4 import BeautifulSoup as BS4
import json
import sys
import os
import pprint


# get_node = 6179
# node_list = [28387, 6179, 26870]
node_list = [11271]

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
}


def res_rename(label_name):
    try:
        return label_list[label_name]
    except:
        return label_name


def get_json(get_node, c=True):
    get_url = 'https://data.gov.tw/dataset/' + str(get_node)

    node_file = requests.get(get_url)
    node_file = BS4(node_file.content.decode('utf-8'), 'lxml')
    json_title = node_file.find('h1', 'node-title').text.replace('/', '_').replace(':', '_')

    node_file = node_file.find('div', 'node-content')

    node_label = []

    # get the keywords list
    node_keywords = node_file.find_all('div', 'tag-wrapper')
    node_key_list = []
    for k in node_keywords:
        node_key_list.append(k.text)

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

    # get contents
    node_content = []
    node_content_temp = node_file.find_all('div', 'field-item')

    for k, i in enumerate(node_content_temp):
        node_content.append(i.text.replace('\xa0', '').replace('\n', ''))

    # split stats line
    stats = node_content[-1].split(' ')
    for i in range(3):
        node_label.append(res_rename(stats[i*2].strip(':')))
        node_content.append(stats[i*2+1])

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

    # AGENCY to end
    for k in range(res_list[-1], len(node_label)):
        if 'KEYWORD' in node_label[k]:
            if 'KEYWORDS' == node_label[k]:
                node_content[k] = node_key_list
                node_matrix[node_label[k]] = node_content[k]
        else:
            node_matrix[node_label[k]] = node_content[k]

    # print('resources :: -----------------------------------')
    res_matrix = []
    for k in range(1, len(res_list)-1):
        res_temp = {}
        for l in range(res_list[k]+1, res_list[k+1]):
            res_temp[node_label[l]] = node_content[l]

        res_matrix.append(res_temp)

    node_matrix['RESOURCE'] = res_matrix

    json_file = str(get_node) + '. ' + node_matrix['AGENCY'] + '_' + json_title + '.json'
    if c:
        with open(json_file, 'w', encoding = 'utf-8') as j_file:
            json.dump(node_matrix, j_file, ensure_ascii=False, indent=4)
            return json_file
    else:
        pprint.pprint(node_matrix, indent = 4)

# main ----------------------------------------
# get_json(node_list)


if len(sys.argv) == 2:
    get_json(int(sys.argv[1]), c=False)
elif len(sys.argv) == 3:
    get_json(int(sys.argv[1]), c=sys.argv[2])
else:
    print('Node : ' + str(len(node_list)))
    for node_item in node_list:
        json_name = get_json(node_item)
        if os.path.exists(json_name):
            print(json_name)
        else:
            print(json_name + ' :: error')
