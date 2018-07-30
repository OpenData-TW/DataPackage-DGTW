#
# get data list CSV from data.gov.tw
# CSV - https://data.gov.tw/datasets/export/csv
# CSV - https://data.gov.tw/datasets/export/csv?type=dataset&order=last_update_time&qs=&uid=
#

import requests
import datetime

csv_url = "https://data.gov.tw/datasets/export/csv"
list_url = "https://data.gov.tw/datasets/export/csv?type=dataset"

now_date = datetime.datetime.now()
today_date = now_date.strftime("%Y%m%d")
csv_file = 'datagovtw_dataset_' + today_date + '.csv'

csv_node = requests.get(list_url)

with open('\\Datasets\\' + csv_file, 'wb') as cf:
    for csv_data in csv_node.iter_content():
        cf.write(csv_data)



