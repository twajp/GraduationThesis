import re
import sys
import csv
from datetime import datetime, timedelta


exdata_path = sys.argv[1]
exdata = []
with open(exdata_path) as f:
    for row in csv.reader(f):
        exdata.append(row)

tslog_path = sys.argv[2]
tslog = []
with open(tslog_path) as f:
    for row in csv.reader(f):
        tslog.append(row)

aclog_path = sys.argv[3]
aclog = []
with open(aclog_path) as f:
    for row in csv.reader(f):
        aclog.append(row)

if len(sys.argv) > 4:
    aclog2 = []
    with open(sys.argv[4]) as f:
        for row in csv.reader(f):
            aclog2.append(row)
    aclog2.pop(0)
    aclog.extend(aclog2)

result = []
print(tslog_path)

for i in range(1, len(exdata)):
    if not exdata[i]:
        continue
    if exdata[i][0] == '':
        continue

    # 車線変更開始と終了時刻を記録
    lc_start = datetime.fromisoformat(exdata[i][0])
    lc_end = datetime.fromisoformat(exdata[i][16])

    # tslogを一行ずつ取り出し、
    for j, line in enumerate(tslog):  # この辺のコードがおかしそう11/26 ウインカーを出す前に車線変更をした場合の検討が足りない？
        ts_timestamp = datetime.fromisoformat(line[1])
        ts = line[6]
        ts_mode = line[5]

        if lc_start-ts_timestamp > timedelta(milliseconds=0) and (ts_mode == '1' or ts_mode == '2'):  # 方向指示器の操作時～車線変更するまでが正の値の時 and 1 or 2
            if exdata[i][14] == 'right start' and ts == 'right on':
                ts_start = ts_timestamp
                ts_index = j
                next_ts_index = j+1
                exdata_index = i
            elif exdata[i][14] == 'left start' and ts == 'left on':
                ts_start = ts_timestamp
                ts_index = j
                next_ts_index = j+1
        elif lc_start-ts_timestamp > timedelta(milliseconds=0) and (ts_mode == '3' or ts_mode == '5'):  # 方向指示器の操作時～車線変更するまでが正の値の時 and 3 or 5
            if exdata[i][14] == 'right start' and ts == 'right on':
                ts_start = ts_timestamp
                ts_index = j
                next_ts_index = j+1
            elif exdata[i][14] == 'left start' and ts == 'left on':
                ts_start = ts_timestamp
                ts_index = j
                next_ts_index = j+1
        else:  # 方向指示器の操作時～車線変更するまでが同じか、負の値
            break
            # if ts[-1] == 'f':  # off
            #     ts_end = ts_timestamp
            #     break
    if tslog[next_ts_index][1][-1] == 'n':
        print('hello')
    ts_end = datetime.fromisoformat(tslog[next_ts_index][1])  # 何のコード？

    result.append([ts_start.time(), lc_start.time(), lc_end.time(), ts_end.time(), (lc_start-ts_start).total_seconds(), (lc_end-lc_start).total_seconds(), (ts_end-lc_end).total_seconds(), tslog[ts_index][5], tslog[ts_index][6], tslog[next_ts_index][6], exdata[i][14], exdata[i][30]])
    print(*result[-1])
    # print(aclog)

    for x in range(1, len(aclog)):
        ac_timestamp = datetime.fromisoformat(aclog[x][0])
        if ts_start-ac_timestamp > timedelta(milliseconds=0):
            ts_start_aclog1 = aclog[x]
            # ts_start_aclog2 = aclog[x+1]
        elif ts_end-ac_timestamp > timedelta(milliseconds=0):
            ts_end_aclog1 = aclog[x]
            # ts_end_aclog2 = aclog[x+1]

    # print(ts_start_aclog1)
    # print(ts_end_aclog1)

    exdata[i].insert(0, '')
    exdata[i][0:0] = ts_start_aclog1
    exdata[i].append('')
    exdata[i].extend(ts_end_aclog1)
    exdata[i].extend(['', (lc_start-ts_start).total_seconds(), (lc_end-lc_start).total_seconds(), (ts_end-lc_end).total_seconds(), tslog[j][5]])

# ts_start, lc_start,

exdata[0].insert(0, '')
exdata[0][0:0] = aclog[0][0:13]
exdata[0].append('')
exdata[0].extend(aclog[0][0:13])
exdata[0].extend(['', 'lc_start-ts_start', 'lc_end-lc_start', 'ts_end-lc_end', 'tslog[next_ts_index][5]'])
with open(exdata_path[:-4]+'_aclog.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(exdata)

with open(re.sub(r'ExData_.*?_', 'Result_Time_Simple_', exdata_path), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(result)
