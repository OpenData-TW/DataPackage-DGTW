# encoding: utf-8
#
# 2017.10.10 v0.1
# GET_RES : from dp[r].json - create folder + download resources
#

import requests
import json
from os import walk

baseURL = 'e:\\DevSource\\Github\\DataPackage-DGTW\\Temp\\'

# get all [r].json in the directory
fullList = []
dirList = []
for (dirpath, dirnames, filenames) in walk(baseURL):
    fullList.extend(filenames)
    break

# get all files
for i in fullList :
    if '[r]' in i : 
        dirList.append(i)

rData = {}
rNum = 0

# Process for each file
# 1. make folder
# 2. copy files
# 3. get resource types/names/number
# 4. download resource file, rename to :
#      1. 資源描述.file_type
#      2. if all resources got same 資源描述 : title.file_type
for i in dirList :
    with open(baseURL + i, encoding = 'utf-8') as data_file:
        rData = json.load(data_file)
        print('node : ', rData['node'])
        rNum = int((len(rData) - 1) / 5)
        j = 0
        resName = rData['res_name_' + str(j)].replace('csv', '').replace('xml', '').replace('json', '')
        print(j, ' : ', resName)
        for j in range(1, rNum) :
            resName = rData['res_name_' + str(j)].replace('csv', '').replace('xml', '').replace('json', '')
            if resName == rData['res_name_' + str(j-1)].replace('csv', '').replace('xml', '').replace('json', '') :
                continue
            print(j, ' : ', resName)
    print(rNum)

    print("--------------------------------------------------------------")


