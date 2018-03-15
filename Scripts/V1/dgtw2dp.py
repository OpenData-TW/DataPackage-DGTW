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
import urllib.parse
from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
import requests


nodeList = [74806,76892,74628,76882,76880,76879,12848,76671,13764,10424,76147,75916,75917,75918,75920,75921,44323,75808,75807,75805,
            75803,75802,67699,31241,73960,31363,45549,45573,37022,37023,37082,37100,37101,37102,49703,45570,45559,46343,45547,46404,
            45561,31484,31735,47355,47356,31485,47358,47359,46399,45544,45565,45553,45562,45550,46234,46438,46394,46363,45552,46389,
            45571,46242,31228,31235,31230,46406,31233,31229,63455,57360,57363,57364,57366,57367,57385,57386,57387,57388,57389,57452,
            58388,58471,58491,58492,62264,62077,62035,61997,61996,61936,61558,61513,31111,61926,75034,30550,56813,46279,46586,46233,
            46400,75668,75669,75670,75675,75676,75677,75678,75679,75680,75681,75682,75683,75684,75685,55071,73855,73831,75691,6514,
            67702,47103,28281,73253,73269,73270,73271,73272,6816,57164,27525,52348,33524,43282,68662,47116,26074,48532,46286,46277,
            53301,53302,53427,53433,53562,53614,53641,75757,62923,61276,48203,45239,6943,17501,55881,55879,55875,55877,55873,55870,
            55868,55866,41266,55736,55732,55733,55728,55730,55726,55724,55722,55677,55679,55680,55681,55682,55670,55674,55676,55514,
            55512,55510,55508,55506,55504,55502,55500,27462,55006,27461,31508,52884,36354,42035,29443,33342,40459,33277,26662,18233,
            32899,33275,33306,33276,41425,26061,41906,41907,41905,37371,29289,32120,43837,43772,43778,43833,6070,6051,45966,44745,
            42176,45967,36226,36339,36358,36741,37353,38700,38963,40277,40542,40548,41467,41469,41470,41471,41472,41485,41512,41513,
            41514,41515,41516,41517,41518,41519,42398,42610,42652,42653,42654,42655,42656,42664,42665,42666,42667,42668,42669,42670,
            42671,42672,43086,43255,43256,43257,44624,44744,45968,45969,45970,45971,45972,45973,45974,45975,45976,45977,45978,46842,
            46990,47045,47083,47088,47100,47101,47102,47104,47109,47112,47114,47581,47582,47583,47584,47586,49701,49702,9537,37686,
            33433,46361,45624,5984,5983,5982,5981,45251,25939,44799,7885,31903,42620,42618,42616,42615,42614,26833,41995,41996,
            41993,41994,41992,41961,41960,41923,41924,41920,6262,6644,40324,41396,41268,41267,40650,40627,35963,33645,36056,39080,
            33738,33735,33734,33737,26706,33736,39609,26548,38775,38595,36687,36706,35597,29710,28018,26631,33570,33556,33557,33559,
            33560,32715,31703,31020,30092,9501,26776,25439,24854,25133,25134,22203,21725,21046,20494,20457,17190,14574,14368,13842,
            12851,11956,11955,11954,11953,11952,11951,10566,10313,9852,9502,8682,8562,6195,6171,6157,6158,6159,6160,6161,
            6162,6163,6164,6165,6166,6167,6168,6169,6170,6571]

# baseURL = 'e:\\DevSource\\Github\\DataPackage-DGTW\\Temp\\'
baseURL = '.\\Datasets\\'

for nodeKey in nodeList:
    nodeNum = str(nodeKey)
    nodeURL = "http://data.gov.tw/node/" + nodeNum

    r = requests.get(nodeURL)
    r = BeautifulSoup(r.content.decode('utf-8'), 'html.parser')

    dataMeta = {}

    # node dataset Title
    nodeTitle = r.title.get_text()

    if '找不到網頁' in nodeTitle:
        print(nodeNum, ' : 找不到網頁')
        dataMeta = {'title': '找不到網頁'}

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
        for i in range(1, len(tempMeta)):
            nodeMeta.append(tempMeta[i].get_text().strip().replace('\xa0', ''))

        #
        # get keywords count : class = "tag-wrapper" -----------------------------------
        #

        keyCont = r.find_all('div', class_='tag-wrapper')
        keywordList = []

        if len(keyCont) > 0:
            for i in keyCont:
                keywordList.append(i.get_text())

            # keyMetaPos = nodeMeta.index(''.join(keywordList))
            keyMetaPos = nodeLabel.index('關鍵字')
            nodeMeta[keyMetaPos] = keywordList
            # remove extra keywords fields
            del nodeMeta[keyMetaPos + 1:keyMetaPos + len(keyCont) + 1]
        keywordList.insert(0, str(len(keyCont)))

        #
        # get resources Count : class="dgresource" -------------------------------------
        #

        resCont = r.find_all('a', class_='dgresource')
        resType = []
        resCount = int(len(resCont) / 2)
        for i in range(0, resCount):
            resType.append(resCont[i * 2].get_text())

        resMeta = {}
        resPos = nodeLabel.index('資料資源')
        resLen = resPos + resCount * 8 - 1
        resLabel = nodeLabel[resPos:resPos + 8]

        for i in range(0, resCount):
            resMetaSub = {}
            for j in range(1, 8):
                resMetaSub[resLabel[j]] = nodeMeta[resPos + i * 8 + j]
            resMeta['resource_' + str(i)] = resMetaSub

        del nodeMeta[resPos:resLen]
        del nodeLabel[resPos + 1:resPos + resCount * 7 + 1]
        nodeMeta[resPos] = resMeta

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

        # -- dataMeta ------------------------------------------------------------------

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

        dataURL = baseURL + nodeNum + '-' + dataMeta['提供機關'] + '_' + dataMeta['title'] + '.json'
        print(dataURL)
        f = open(dataURL, 'w', encoding='utf-8')

        json.dump(dataMeta, f, ensure_ascii=False, indent=4)
        f.close()
        
        if (nodeKey % 10) == 0 :
            sleep(2)
