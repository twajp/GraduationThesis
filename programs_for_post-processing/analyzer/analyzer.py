import sys
import csv
from pprint import pprint


# Result_Time_Simple.csv
import_path = sys.argv[1]
imported_data = []
with open(import_path) as f:
    for row in csv.reader(f):
        imported_data.append(row)


sum = {
    '1': [0, 0, 0, 0],
    '2': [0, 0, 0, 0],
    '3': [0, 0, 0, 0],
    '5': [0, 0, 0, 0],
}

for i in range(0, len(imported_data)):
    if imported_data[i][7] == '1':
        sum['1'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
        sum['1'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
        sum['1'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
        sum['1'][3] += 1  # データ数
    elif imported_data[i][7] == '2':
        sum['2'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
        sum['2'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
        sum['2'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
        sum['2'][3] += 1  # データ数
    elif imported_data[i][7] == '3':
        sum['3'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
        sum['3'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
        sum['3'][2] += (2/3)*3 - float(imported_data[i][4]) - float(imported_data[i][5])  # 車線変更終了からウインカーが「消える」まで
        sum['3'][3] += 1  # データ数
    elif imported_data[i][7] == '5':
        sum['5'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
        sum['5'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
        sum['5'][2] += (2/3)*5 - float(imported_data[i][4]) - float(imported_data[i][5])  # 車線変更終了からウインカーが「消える」まで
        sum['5'][3] += 1  # データ数

average = {
    '1': [sum['1'][0]/sum['1'][3], sum['1'][1]/sum['1'][3], sum['1'][2]/sum['1'][3]],
    '2': [sum['2'][0]/sum['2'][3], sum['2'][1]/sum['2'][3], sum['2'][2]/sum['2'][3]],
    '3': [sum['3'][0]/sum['3'][3], sum['3'][1]/sum['3'][3], sum['3'][2]/sum['3'][3]],
    '5': [sum['5'][0]/sum['5'][3], sum['5'][1]/sum['5'][3], sum['5'][2]/sum['5'][3]],
}
pprint(average)
print(average['1'])
with open('../../data/post-processed/Analysis_1.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['1'])
with open('../../data/post-processed/Analysis_2.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['2'])
with open('../../data/post-processed/Analysis_3.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['3'])
with open('../../data/post-processed/Analysis_5.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['5'])
