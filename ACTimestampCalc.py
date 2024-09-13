import sys
import csv
from datetime import datetime, timedelta


aclog_path = sys.argv[1]
aclog = []
with open(aclog_path) as f:
    for row in csv.reader(f):
        aclog.append(row)

zeroTimestamp = datetime.fromisoformat(aclog[1][0]) - timedelta(milliseconds=int(aclog[1][2]))
# print(zeroTimestamp.isoformat())


aclaptime_path = sys.argv[2]
aclaptime = []
with open(aclaptime_path) as f:
    for row in csv.reader(f):
        aclaptime.append(row)

aclaptime[0].insert(0, 'timestamp')
aclaptime[0].insert(16, '')
aclaptime[0][16:16] = aclaptime[0]
for i in range(1, len(aclaptime)):
    if not aclaptime[i]:
        continue
    # if not aclaptime[i][0]:
    #     continue
    if aclaptime[i][0] == '':
        continue
    timestamp_start = zeroTimestamp+timedelta(milliseconds=int(aclaptime[i][1]))
    timestamp_end = zeroTimestamp+timedelta(milliseconds=int(aclaptime[i][16]))
    # print(aclaptime[i][1], timestamp.isoformat())
    aclaptime[i].insert(0, timestamp_start.isoformat())
    aclaptime[i].insert(16, timestamp_end.isoformat())

# print(aclaptime)

with open(aclaptime_path[:-4]+'_timestamp.csv', 'w', newline="") as f:
    writer = csv.writer(f)
    writer.writerows(aclaptime)
