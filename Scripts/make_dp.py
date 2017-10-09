# encoding: utf-8
#
# 2017.10.09 v0.1
# MAKE_DP : from dp.json - create download json
#

import json
import requests
import urllib.parse
from os import walk

nodeList = ['12639']
baseURL = 'e:\\DevSource\\Github\\DataPackage-DGTW\\Temp\\'

resMeta = ['資源網址', 'linkable', 'downloadable', 'structure', 'encoding', 'file_type']

for nodeKey in nodeList:
    nodeNum = nodeKey
    jURL = ''
    rData = {}
    reqHeaders = {
        'User-Agent': 'Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02'
    }

    # get all files in the directory
    f = []
    for (dirpath, dirnames, filenames) in walk(baseURL):
        f.extend(filenames)
        break

    for i in f:
        if '[r]' in i: continue
        if nodeNum in i:
            jURL = baseURL + i
            rData['node'] = i[:-5]
            break

    if jURL != '':
        print(jURL, end='\n\n')
        jFile = open(jURL, 'r', encoding='utf-8')
        jContent = json.loads(jFile.read())
        rFile = open(jURL[:-5] + '[r].json', 'w', encoding='utf-8')

        resNum = len(jContent['資料資源'])
        for i in range(0, resNum):
            resID = 'resource_' + str(i)
            rData['res_name_' + str(i)] = jContent['資料資源'][resID]['資源描述']
            rData['filetype_' + str(i)] = jContent['資料資源'][resID]['file_type'].lower()
            rData['encoding_' + str(i)] = jContent['資料資源'][resID]['編碼'].lower()

            rData[resID + '_url'] = jContent['資料資源'][resID]['資源網址']
            if jContent['資料資源'][resID]['linkable'] == 0 or jContent['資料資源'][resID]['downloadable'] == 0:
                print(resID + ': ' + jContent['資料資源'][resID]['資源網址'] + ' - not downloadable')
                rData[resID + '_filename'] = False
            else:
                print(resID + ': ' + jContent['資料資源'][resID]['資源網址'])
                resR = requests.get(jContent['資料資源'][resID]['資源網址'], headers=reqHeaders)
                print(resR.status_code)
                print(resR.headers)
                try:
                    print(urllib.parse.unquote(resR.headers['content-disposition']))
                    rData[resID + '_filename'] = urllib.parse.unquote(resR.headers['content-disposition'][21:-1])
                except KeyError:
                    print('non default file name')
                    rData[resID + '_filename'] = 'no default'

        json.dump(rData, rFile, ensure_ascii=False, indent=4)
        rFile.close()
        jFile.close()

    else:
        print('no files!!')

print('=============================================================================')