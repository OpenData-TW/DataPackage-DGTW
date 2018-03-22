import requests
from bs4 import BeautifulSoup

node_url = 'http://data.ntpc.gov.tw/od/search'
node_next = 'http://data.ntpc.gov.tw/getSearchPageData'

param = {'clickPage': 3}
para_headers = {
    'Accept-Encoding': 'gzip, deflate',
    'Cookie': 'JSESSIONID=AD282B646C8CC1BE046CD45CA7C300D8; TS01b5ddc3=0105e3da54c866a977e9fd63c1400d65e63cd6a91dd16ab8e0b71afd695d6251430d97bbd95081bd93a85b8f009dfb27cbdc038eb7318844031ad619d684970940089e1512; BIGipServerPool_IMC-MIS-OD2AP_80=rd4o00000000000000000000ffffac127c37o80',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'data.ntpc.gov.tw',
    'Referer': 'http://data.ntpc.gov.tw/od/search',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0'
}
r = requests.post(node_next, data = param, headers = para_headers)
b = BeautifulSoup(r.content.decode('utf-8'), 'lxml')

print(b)
