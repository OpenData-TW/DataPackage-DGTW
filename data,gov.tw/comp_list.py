# compare CSV list
#

file1 = 'Datasets\\csv.lst'             # from front page
file2 = 'Datasets\\csv2.lst'            # from search page
outfile = 'Datasets\\csv3.lst'          # diff

with open(file1, 'r', encoding='utf-8') as f1:
    list1 = f1.readlines()

with open(file2, 'r', encoding='utf-8') as f2:
    list2 = f2.readlines()

with open(outfile, 'w', encoding='utf-8') as f3:
    j = 0
    for i in list1:
        while i > list2[j]:
            dump_text = list2[j].replace('\n', '') + ' *\n'
            f3.write(dump_text)
            j = j + 1

        if i == list2[j]:
            f3.write(i)
            j = j + 1
        else:
            f3.write('-\n')


