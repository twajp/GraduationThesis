import sys
import csv
from datetime import datetime, timedelta


tslog_path = sys.argv[1]
tslog = []
with open(tslog_path) as f:
    for row in csv.reader(f):
        tslog.append(row)

aclog_path = sys.argv[2]
aclog = []
with open(aclog_path) as f:
    for row in csv.reader(f):
        aclog.append(row)

if len(sys.argv) > 3:
    aclog2 = []
    with open(sys.argv[3]) as f:
        for row in csv.reader(f):
            aclog2.append(row)
    aclog2.pop(0)
    aclog.extend(aclog2)

TSLog_with_ACLog = []
for i, line in enumerate(tslog):
    tslog_timestamp_str = line[1]
    tslog_timestamp = datetime.fromisoformat(tslog_timestamp_str)
    tslog_mode = line[5]
    tslog_signal = line[6]

    for x in range(1, len(aclog)):
        ac_timestamp = datetime.fromisoformat(aclog[x][0])
        if ac_timestamp-tslog_timestamp > timedelta(milliseconds=0):
            aclog_before_ts = aclog[x-1].copy()  # Deep copy
            aclog_after_ts = aclog[x].copy()
            aclog_before_ts[0:0] = [tslog_timestamp_str, tslog_mode, tslog_signal]
            aclog_after_ts[0:0] = [tslog_timestamp_str, tslog_mode, tslog_signal]
            # print(aclog_before_ts)
            print(aclog_after_ts)
            TSLog_with_ACLog.append(aclog_after_ts)
            break

print(tslog_path)
export_path = tslog_path.replace('/original/', '/post-processed/')
with open(export_path[:-4]+'_aclog.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(TSLog_with_ACLog)
