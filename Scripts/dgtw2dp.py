# encoding: utf-8
# 2017.10.06
# node to datapackage
#

import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, tzinfo
from time import sleep

nodeList = [10340]
baseURL = '..\\temp\\'

for k in nodeList:
    # node = xxxxx / http://data.gov.tw/node/xxxxx
    nodeNum = str(k)
    node_url = "http://data.gov.tw/node/" + nodeNum


    r = requests.get(node_url)
    r = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')

    # get resources Count
    resCount = int(len(r.find_all('a', class_='dgresource')) / 2)
    resCount1 = resCount

    # get keywords count
    keyCount = r.find_all('div', class_='tag-wrapper')

    # get all field label
    nodeContent = r.find_all("div", class_="field-label")
    nodeTitle = r.select("h1.node-title")

    # set up field label list
    labelCont = []

    # remove beginning ':' and trim space
    for i in nodeContent:
        labelCont.append(i.get_text().strip().replace(':', ''))

    # defaut resCount = 1, so remove 1 = remove default one
    resCount -= 1
    posAdd = 11

    # if resCount > 1 - add new field label and rename field label + count number
    while resCount != 0:
        labelCont.insert(posAdd, '資料資源_' + str(resCount))
        for i in range(1, 8):
            labelCont[i + posAdd] = labelCont[i + posAdd] + '_' + str(resCount)
        resCount -= 1
        posAdd += 8

    # if keyCount != 0
    keyPos = [i for i, x in enumerate(labelCont) if x == '關鍵字']
    keyPos = int(keyPos[0])
    if len(keyCount) != 0:
        for i in range(0, len(keyCount)):
            labelCont.insert(keyPos + 1, '關鍵字_' + str(i))

    labelCont.append('統計')


    nodeContent = r.find_all("div", class_="field-item")
    labelCont[2] = '主要欄位說明_0'
    jData = {}
    jTitle = r.title.get_text().replace(' | 政府資料開放平臺', '')
    jData['title'] = jTitle
    jData['node'] = str(k)
    jData['created'] = str(datetime.now())[:-7]

    for i in range(1, len(labelCont)):
        textCont = nodeContent[i].get_text()
        textCont.replace('\r\n', '')
        if '資料資源' in labelCont[i]: continue
        # print('{:2d} - {} : {}'.format(i, labelCont[i], textCont))
        jData[labelCont[i]] = textCont.strip('\n\t\r')

    # 新增欄位
    # 資源數量 : resCount1
    # 關鍵字數量 : keyCount[]
    # 備註拆解 + 授權說明網址
    jData['resource'] = resCount1
    jData['keywords'] = int(len(keyCount))
    if '備註' not in jData.keys():
        jData['備註'] = ''
    jData['授權說明網址'] = ''
    if '授權說明網址' in jData['備註']:
        jData['授權說明網址'] = jData['備註'][8:]



    jFile = baseURL + nodeNum + ' - ' + jData['提供機關'] + '.' + jTitle + '.json'
    print(jFile)
    f = open(jFile, 'w', encoding='utf-8')
    json.dump(jData, f, ensure_ascii=False, indent=4)
    f.close()

    sleep(1)


# encoding: utf-8
# data quality check
# get answer from http://quality.data.gov.tw/
# /dq_event.php?nid=xxxx
# ex : http://quality.data.gov.tw/dq_event.php?nid=31111
#
# good : 55521
# wrong : 55523
# bad : 45709


for k in nodeList:
    nodeNum = str(k)
    dq_url = "http://quality.data.gov.tw/dq_event.php?nid=" + nodeNum

    r = requests.get(dq_url)
    f = open(baseURL + nodeNum + ' - DQ.json', 'w', encoding='utf-8')
    print(baseURL + nodeNum + ' - DQ.json')

    rContent = r.text[1:].strip()  # remove first ':' character and space

    if 'event: done' in rContent:
        rIndex = rContent.index('done')
        rResult = rContent[rIndex + 21:-1]
        jData = json.JSONDecoder().decode(rResult)

        json.dump(jData, f, ensure_ascii=False, indent=4)
        f.close()

    else:
        if 'event: nop' in rContent:
            rResult = '{ "status" : "wrong node" }'
        else:
            rResult = "non 'event : done'\n" + rContent
        f.write(rResult)
        f.close()

    if k % 10 == 0:
        sleep(1)

print("----------------------------- end -----------------------------------")