import csv

with open('yilan.2018.03.20.csv', 'r', newline='', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
    for k, row in enumerate(csv_reader):
        if len(row) > 5:
            new_cont = ', '.join(row[4:])
            print(str(k+1) + ' :: ' + new_cont)
