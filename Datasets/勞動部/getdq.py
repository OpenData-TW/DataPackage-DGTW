#
# 1. 取得目前目錄內檔案清單 + oid
# 2. 檢查資源是否可下載 : dq - downloadable = 1
# 3. 建立 oid 子目錄
# 4. 下載
#

import requests
import json
import pprint
import os
from os import listdir
from os.path import isfile, join
import re


# get directory file list for node list
def get_list(get_path='.'):
    dir_files = [f for f in listdir(get_path) if isfile(join(get_path, f))]
    dir_list = []
    for k in dir_files:
        j = k.split('. ')[0]
        dir_list.append((j, k))
    return dir_list


# remove characters
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


# check
def dq_download(dq_list):
    # dq_node = 10100
    dq_url = 'https://quality.data.gov.tw/dq_event.php?nid=' + str(dq_list[0])

    dq_file = requests.get(dq_url)
    dq_file = dq_file.content.decode('utf-8')
    try:
        dq_index = dq_file.index('event: done') + 11

        dq_json = '{' + dq_file[dq_index:] + '}'
        dq_json = dq_json.replace('data:', '"data":')

        dq_json = json.loads(dq_json)
        dq_downloadable = dq_json['data']['result']['dataset']['downloadable']
    except ValueError:
        dq_downloadable = 2
        dq_json = dq_file

    oid_path = data_path + '\\DATA\\' + dq_list[0]
    try:
        os.makedirs(oid_path)
    except OSError:
        pass

    with open(oid_path + '\\' + dq_list[0] + '.[dq].json', 'w', encoding='utf-8') as f:
        json.dump(dq_json, f, ensure_ascii=False, indent=4)

    with open(data_path + '\\' + dq_list[1], 'r', encoding='utf-8') as r_node:
        r_json = json.load(r_node)
        with open(oid_path + '\\' + dq_list[1], 'w', encoding='utf-8') as w_node:
            json.dump(r_json, w_node, ensure_ascii=False, indent=4)

    return dq_downloadable


# get_resource - download
def get_res(node_id):
    oid_path = data_path + '\\DATA\\' + node_id[0]
    try:
        os.makedirs(oid_path)
    except OSError:
        pass

    with open(data_path + '\\' + node_id[1], 'r', encoding='utf-8') as r_node:
        r_json = json.load(r_node)
        for k in r_json['RESOURCE']:
            response = requests.get(k['RES_URL'])
            response.encoding = 'utf-8'
            try:
                d = response.headers['Content-Disposition']
                f_name = re.findall("filename=(.+)", d)
                fname = f_name[0].replace('"', '')
            except KeyError:
                if len(k['RES_DESC']) < 30:
                    fname = clean_name(k['RES_DESC'] + '.' + k['RES_FILETYPE'].lower())
                else:
                    fname = clean_name(r_json['TITLE'] + '.' + k['RES_FILETYPE'].lower())
            with open(oid_path + '\\' + fname, "wb") as handle:
                for data in response.iter_content():
                    handle.write(data)


#
# --------------------------------------------------------------------
#


error_list = []
data_path = 'RAW'

node_id_list = get_list(data_path)

for i in node_id_list:
    dq_download_able = dq_download(i)
    if dq_download_able:
        print(i)
        get_res(i)
        if dq_download_able == 2:
            error_list.append(i[0])
    else:
        error_list.append(i[0])


print('error : ')
pprint.pprint(error_list)


