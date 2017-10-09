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

for i in fullList :
    if '[r]' in i :
        dirList.append(i)

rData = {}
for i in dirList :
    with open(baseURL + i, encoding = 'utf-8') as data_file:
        rData = json.load(data_file)
        rNum = int((len(rData) - 1) / 4)
        for j in range(0, rNum) :
            print(rNum)

    print("--------------------------------------------------------------")


