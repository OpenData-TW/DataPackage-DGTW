from bs4 import BeautifulSoup

with open('data.gov.tw.local.html', 'r', encoding='utf-8') as f:
    node_file = BeautifulSoup(f, 'lxml')

node_title = node_file.find_all('li', role = 'treeitem')

for k, i in enumerate(node_title):
    node_name = str(i.find('span', class_ = 'facet-name').text)
    node_count = str(i.find('span', class_ = 'facet-count').text)
    node_id = str(i.find('a', class_ = 'facet-item').get('data-qs')).replace('dtid:', '')
    print(node_name + ', ' + node_id)