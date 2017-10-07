# encoding: utf-8

# 2017.10.06
# node to datapackage
#


# import pprint
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime, tzinfo
from time import sleep

nodeList = [10340, 10344, 11093, 11257, 11271, 14864, 14869, 15152, 15293, 23198, 23201,
            27495, 28983, 28987, 28988, 28993, 28994, 28995, 29021, 31159, 31251, 31818,
            31819, 31848, 31849, 31850, 31858, 31862, 36947, 38824, 42338, 42578, 44662,
            44663, 44664, 44665, 45581, 45624, 45672, 45693, 45709, 45710, 45711, 45714,
            45718, 45719, 45720, 45721, 45722, 45723, 45724, 45725, 45726, 45727, 45728,
            45729, 45730, 45732, 45745, 45749, 45750, 45751, 45756, 45757, 45758, 45811,
            46439, 46441, 46442, 46444, 46445, 46446, 46447, 46448, 48126, 48143, 48205]

for k in nodeList:
    # node = xxxxx / http://data.gov.tw/node/xxxxx
    nodeNum = str(k)
    node_url = "http://data.gov.tw/node/" + nodeNum
    baseURL = 'f:\\DataSet\\@地方\\基隆市\\Datasets\\'

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
    # pp = pprint.PrettyPrinter(indent=4)
    # print(labelCont)
    # print('=====================================================================')

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

    # print('=====================================================================')
    # print(jData)


    jFile = baseURL + nodeNum + ' - ' + jData['提供機關'] + '.' + jTitle + '.json'
    print(jFile)
    f = open(jFile, 'w', encoding='utf-8')
    json.dump(jData, f, ensure_ascii=False, indent=4)
    f.close()

    sleep(1)
print("----------------------------- end -----------------------------------")
