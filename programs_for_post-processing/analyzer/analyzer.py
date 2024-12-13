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
    '1': {'both': [0, 0, 0, 0],
          'right': [0, 0, 0, 0],
          'left': [0, 0, 0, 0]},
    '2': {'both': [0, 0, 0, 0],
          'right': [0, 0, 0, 0],
          'left': [0, 0, 0, 0]},
    '3': {'both': [0, 0, 0, 0],
          'right': [0, 0, 0, 0],
          'left': [0, 0, 0, 0]},
    '5': {'both': [0, 0, 0, 0],
          'right': [0, 0, 0, 0],
          'left': [0, 0, 0, 0]},
}

for i in range(0, len(imported_data)):
    if imported_data[i][7] == '1':
        sum['1']['both'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
        sum['1']['both'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
        sum['1']['both'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
        sum['1']['both'][3] += 1  # データ数
        if imported_data[i][10][0] == 'r':
            sum['1']['right'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
            sum['1']['right'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
            sum['1']['right'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
            sum['1']['right'][3] += 1  # データ数
        elif imported_data[i][10][0] == 'l':
            sum['1']['left'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
            sum['1']['left'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
            sum['1']['left'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
            sum['1']['left'][3] += 1  # データ数
    elif imported_data[i][7] == '2':
        sum['2']['both'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
        sum['2']['both'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
        sum['2']['both'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
        sum['2']['both'][3] += 1  # データ数
        if imported_data[i][10][0] == 'r':
            sum['2']['right'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
            sum['2']['right'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
            sum['2']['right'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
            sum['2']['right'][3] += 1  # データ数
        elif imported_data[i][10][0] == 'l':
            sum['2']['left'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
            sum['2']['left'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
            sum['2']['left'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
            sum['2']['left'][3] += 1  # データ数
    elif imported_data[i][7] == '3':
        sum['3']['both'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
        sum['3']['both'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
        sum['3']['both'][2] += (2/3)*3 - float(imported_data[i][4]) - float(imported_data[i][5])  # 車線変更終了からウインカーが「消える」まで
        sum['3']['both'][3] += 1  # データ数
        if imported_data[i][10][0] == 'r':
            sum['3']['right'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
            sum['3']['right'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
            sum['3']['right'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
            sum['3']['right'][3] += 1  # データ数
        elif imported_data[i][10][0] == 'l':
            sum['3']['left'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
            sum['3']['left'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
            sum['3']['left'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
            sum['3']['left'][3] += 1  # データ数
    elif imported_data[i][7] == '5':
        sum['5']['both'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
        sum['5']['both'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
        sum['5']['both'][2] += (2/3)*5 - float(imported_data[i][4]) - float(imported_data[i][5])  # 車線変更終了からウインカーが「消える」まで
        sum['5']['both'][3] += 1  # データ数
        if imported_data[i][10][0] == 'r':
            sum['5']['right'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
            sum['5']['right'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
            sum['5']['right'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
            sum['5']['right'][3] += 1  # データ数
        elif imported_data[i][10][0] == 'l':
            sum['5']['left'][0] += float(imported_data[i][4])  # ウインカーを付けてから車線変更するまで
            sum['5']['left'][1] += float(imported_data[i][5])  # 車線変更開始～終了まで
            sum['5']['left'][2] += float(imported_data[i][6])  # 車線変更終了からウインカーを消すまで
            sum['5']['left'][3] += 1  # データ数

average = {
    '1': {'both': [sum['1']['both'][0]/sum['1']['both'][3], sum['1']['both'][1]/sum['1']['both'][3], sum['1']['both'][2]/sum['1']['both'][3]],
          'right': [sum['1']['right'][0]/sum['1']['right'][3], sum['1']['right'][1]/sum['1']['right'][3], sum['1']['right'][2]/sum['1']['right'][3]],
          'left': [sum['1']['left'][0]/sum['1']['left'][3], sum['1']['left'][1]/sum['1']['left'][3], sum['1']['left'][2]/sum['1']['left'][3]]},
    '2': {'both': [sum['2']['both'][0]/sum['2']['both'][3], sum['2']['both'][1]/sum['2']['both'][3], sum['2']['both'][2]/sum['2']['both'][3]],
          'right': [sum['2']['right'][0]/sum['2']['right'][3], sum['2']['right'][1]/sum['2']['right'][3], sum['2']['right'][2]/sum['2']['right'][3]],
          'left': [sum['2']['left'][0]/sum['2']['left'][3], sum['2']['left'][1]/sum['2']['left'][3], sum['2']['left'][2]/sum['2']['left'][3]]},
    '3': {'both': [sum['3']['both'][0]/sum['3']['both'][3], sum['3']['both'][1]/sum['3']['both'][3], sum['3']['both'][2]/sum['3']['both'][3]],
          'right': [sum['3']['right'][0]/sum['3']['right'][3], sum['3']['right'][1]/sum['3']['right'][3], sum['3']['right'][2]/sum['3']['right'][3]],
          'left': [sum['3']['left'][0]/sum['3']['left'][3], sum['3']['left'][1]/sum['3']['left'][3], sum['3']['left'][2]/sum['3']['left'][3]]},
    '5': {'both': [sum['5']['both'][0]/sum['5']['both'][3], sum['5']['both'][1]/sum['5']['both'][3], sum['5']['both'][2]/sum['5']['both'][3]],
          'right': [sum['5']['right'][0]/sum['5']['right'][3], sum['5']['right'][1]/sum['5']['right'][3], sum['5']['right'][2]/sum['5']['right'][3]],
          'left': [sum['5']['left'][0]/sum['5']['left'][3], sum['5']['left'][1]/sum['5']['left'][3], sum['5']['left'][2]/sum['5']['left'][3]]},
}
pprint(average)
with open('../../data/post-processed/Analysis_1_both.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['1']['both'])
with open('../../data/post-processed/Analysis_1_right.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['1']['right'])
with open('../../data/post-processed/Analysis_1_left.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['1']['left'])

with open('../../data/post-processed/Analysis_2_both.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['2']['both'])
with open('../../data/post-processed/Analysis_2_right.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['2']['right'])
with open('../../data/post-processed/Analysis_2_left.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['2']['left'])

with open('../../data/post-processed/Analysis_3_both.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['3']['both'])
with open('../../data/post-processed/Analysis_3_right.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['3']['right'])
with open('../../data/post-processed/Analysis_3_left.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['3']['left'])

with open('../../data/post-processed/Analysis_5_both.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['5']['both'])
with open('../../data/post-processed/Analysis_5_right.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['5']['right'])
with open('../../data/post-processed/Analysis_5_left.csv', 'a', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(average['5']['left'])
