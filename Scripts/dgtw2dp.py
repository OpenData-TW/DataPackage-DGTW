# encoding: utf-8
#
# 2017.10.09 v0.5
#
# DGTW2DP : Data.gov.tw to DataPackage
# datasets - metadata
# http://data.gov.tw/node/XXXXXX : XXXXXX = node number
# datasets - resources check / download
# http://quality.data.gov.tw/dq_event.php?nid=XXXXXX : XXXXXX = node number
#
# output : XXXXXX-dataPublisher_dataTitle.json
#


import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import urllib.parse
from time import sleep
import nodeList

# nodeList = ['25956', '25960']

baseURL = 'e:\\DevSource\\Github\\DataPackage-DGTW\\Temp\\TY\\'

for nodeNum in nodeList:
    nodeURL = "http://data.gov.tw/node/" + nodeNum

    r = requests.get(nodeURL)
    r = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')

    dataMeta = {}

    # node dataset Title
    nodeTitle = r.title.get_text()

    if '找不到網頁' in nodeTitle:
        print(nodeNum, ' : 找不到網頁 - ', nodeURL)
        dataMeta = {'title': '找不到網頁'}
    elif '拒絕存取' in nodeTitle:
        print(nodeNum, ' : 拒絕存取 - ', nodeURL)
        dataMeta = {'title': '拒絕存取'}

    else:
        # get datasets metadata labels : nodeLabel
        tempLabel = r.find_all("div", class_='field-label')
        nodeLabel = []
        for i in range(1, len(tempLabel)):
            nodeLabel.append(tempLabel[i].get_text().replace(':\xa0', ''))
        nodeLabel.append('stats')

        # get datasets metadata content : nodeMeta
        tempMeta = r.find_all("div", class_='field-item')

        nodeMeta = []
        keyMetaPos = 0
        for i in range(1, len(tempMeta)):
            if keyMetaPos == 0 and "search" in str(tempMeta[i].a):
                keyMetaPos = i - 1

            nodeMeta.append(tempMeta[i].get_text().strip().replace('\xa0', ''))

        #
        # get keywords count : class = "tag-wrapper" -----------------------------------
        #

        keyCont = r.find_all('div', class_='tag-wrapper')
        keywordList = []

        if len(keyCont) > 0:
            # keyMetaPos = tempMeta('<div class="tag-wrapper">' + keyCont[0] + '</div>') - 1

            for i in keyCont:
                keywordList.append(i.get_text())

            # keyMetaPos = nodeMeta.index(''.join(keywordList))
            # keyMetaPos = len(nodeMeta) - 1 - nodeMeta[::-1].index(keywordList[0])
            nodeMeta[keyMetaPos] = keywordList
            # remove extra keywords fields
            del nodeMeta[keyMetaPos + 1:keyMetaPos + len(keyCont) + 1]
        keywordList.insert(0, str(len(keyCont)))

        #
        # get resources Count : class="dgresource" -------------------------------------
        #

        resCont = r.find_all('a', class_='dgresource')
        resMeta = {}

        if 'CSV 下載' in nodeLabel:
            resCount = len(resCont) // 5
            resPos = nodeLabel.index('資料資源')
            resLen = resPos + resCount * 11
            resLabel = nodeLabel[resPos:resPos + 11]

            for i in range(0, resCount):
                resMetaSub = {}
                for j in range(1, 11):
                    resMetaSub[resLabel[j]] = nodeMeta[resPos + i * 11 + j]
                resMeta['resource_' + str(i)] = resMetaSub

            del nodeMeta[resPos:resLen - 1]
            del nodeLabel[resPos + 1:resPos + resCount * 10 + 1]

        else:
            resType = []
            resCount = int(len(resCont) / 2)
            for i in range(0, resCount):
                resType.append(resCont[i * 2].get_text())

            resPos = nodeLabel.index('資料資源')
            resLen = resPos + resCount * 8
            resLabel = nodeLabel[resPos:resPos + 8]

            for i in range(0, resCount):
                resMetaSub = {}
                for j in range(1, 8):
                    resMetaSub[resLabel[j]] = nodeMeta[resPos + i * 8 + j]
                resMeta['resource_' + str(i)] = resMetaSub

            del nodeMeta[resPos:resLen - 1]
            del nodeLabel[resPos + 1:resPos + resCount * 7 + 1]

        nodeMeta[resPos] = resMeta

        #         for i in range(len(nodeLabel)) :
        #             print('{} - {} : {}'.format(i, nodeLabel[i], nodeMeta[i]))
        #
        # add title, node number, created time -----------------------------------------
        #

        dataMeta['title'] = nodeTitle.replace(' | 政府資料開放平臺', '')
        dataMeta['node'] = nodeNum
        dataMeta['datapackage_version'] = str(datetime.now())[:-7]

        # add dataMeta body
        for i in range(0, len(nodeLabel)):
            dataMeta[nodeLabel[i]] = nodeMeta[i]

        # add Resrource files type
        dataMeta['resource_type'] = resType

        # reformat stats
        statsMeta = dataMeta['stats'].split(' ')
        statsTemp = {}

        for i in range(0, 3):
            statsTemp[statsMeta[i * 2]] = statsMeta[i * 2 + 1]
        dataMeta['stats'] = statsTemp

        # -- dataMeta -------------------------------------------------------------------------------------------

        dqURL = "http://quality.data.gov.tw/dq_event.php?nid=" + nodeNum
        r = requests.get(dqURL)

        dqContent = r.text[1:].strip().split('\n')  # remove first ':' character and space
        dqTemp = []
        dqDone = {}

        resMeta = ['linkable', 'downloadable', 'structure', 'encoding_match', 'desc_match', 'csv',
                   'fields', 'encoding', 'file_type', 'amount', 'check_time', 'messages', ]

        for i in dqContent:
            if i == '': continue
            dqTemp.append(i)

        for i in range(0, len(dqTemp)):
            if 'event: done' in dqTemp[i]:
                dqDone = json.JSONDecoder().decode(dqTemp[i + 1][5:])
                break
            else:
                dqDone = {}
        if dqDone == {}:
            dataMeta['download'] = 'error'
            print("{}-{}{} download - error".format(nodeNum, dataMeta['提供機關'], dataMeta['title']))
        else:
            dqRList = list(dqDone['result']['resources'].keys())
            dqRList2 = []
            for i in range(0, len(dqRList)):
                dqRList2.append(urllib.parse.unquote(dqRList[i]))

            for i in range(0, resCount):
                resURL = dataMeta['資料資源']['resource_' + str(i)]['資源網址']
                try:
                    index_value = dqRList2.index(resURL)
                except ValueError:
                    index_value = -1
                if index_value == -1:
                    dataMeta['資料資源']['resource_' + str(i)]['dq_check'] = 'error'
                else:
                    dataMeta['資料資源']['resource_' + str(i)]['dq_check'] = 'checked'
                    for j in resMeta:
                        dataMeta['資料資源']['resource_' + str(i)][j] = \
                            dqDone['result']['resources'][dqRList[index_value]]['resource'][j]

        dataURL = baseURL + nodeNum + '-' + dataMeta['提供機關'].replace('/', '_') + '_' + dataMeta['title'].replace('/',
                                                                                                                 '_') + '.json'
        print(dataURL)
        f = open(dataURL, 'w', encoding='utf-8')

    json.dump(dataMeta, f, ensure_ascii=False, indent=4)
    f.close()

    if (int(nodeNum) % 10) == 0:
        sleep(2)

print("--------------------- end --------------------------------")