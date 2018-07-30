# Cut test
# data_test.txt
#

import jieba
jieba.set_dictionary('dict.zh_tw.txt')
jieba.load_userdict('dict_revised_3.txt')
jieba.load_userdict('dataset.txt') 
jieba.load_userdict('geo_name.txt') 

with open('data_title.txt', 'r', encoding='utf-8') as f:
	w = open('data_title_cut.txt', 'w', encoding='utf-8')
	for i in f.readlines():
		seg_list = jieba.cut(i, cut_all=False)
		w.write(i)
		w.write("/ ".join(seg_list))
	w.close()

