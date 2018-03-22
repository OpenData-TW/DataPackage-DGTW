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


# get directory file list for node list
def get_list(get_path='.'):
    dir_files = [f for f in listdir(get_path) if isfile(join(get_path, f))]
    dir_list = []
    for k in dir_files:
        j = k.split('. ')[0]
        dir_list.append((j, k))
    return dir_list


# check
def dq_download(dq_node):
    # dq_node = 10100
    dq_url = 'https://quality.data.gov.tw/dq_event.php?nid=' + str(dq_node)

    dq_file = requests.get(dq_url)
    dq_file = dq_file.content.decode('utf-8')
    dq_index = dq_file.index('event: done') + 11
    dq_json = '{' + dq_file[dq_index:] + '}'
    dq_json = dq_json.replace('data:', '"data":')

    dq_json = json.loads(dq_json)
    dq_downloadable = dq_json['data']['result']['dataset']['downloadable']

    return dq_downloadable


# get_resource - download
def get_res(node_id):
    oid_path = 'RAW\\' + node_id[0]
    print(oid_path)
    try:
        os.makedirs(oid_path)
    except OSError:
        pass


#
# --------------------------------------------------------------------
#


error_list = []
node_list = []

node_id_list = get_list('RAW')

for i in node_list:
    if dq_download(i[0]):
        get_res(i)
    else:
        error_list.append(i[0])


print('error : ')
pprint.pprint(error_list)


