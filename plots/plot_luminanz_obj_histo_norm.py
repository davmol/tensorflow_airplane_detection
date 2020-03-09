from collections import defaultdict

import db_mac
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator

sql = """select object, img_url from od2 where object is not null and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and weather_status like 'Clouds'
    """
falses = defaultdict(list)
result = db_mac.execute(sql)

for row in result:
    if len(row[0].split(",")) > 5:
        falses["falses"].append(row[1])

falsepositves = []
for v in falses.values():
    falsepositves = v

false_pos2 = ["/home/pi/Desktop/project/img/d_c__in_2020_01_08-08_04_53.png",
              "/home/pi/Desktop/project/img/d_c__in_2020_01_09-17_38_02.png",
              "/home/pi/Desktop/project/img/d_c__in_2020_01_09-17_40_03.png",
              "/home/pi/Desktop/project/img/d_c__in_2020_01_09-17_42_49.png",
              "/home/pi/Desktop/project/img/d_c__in_2020_01_13-16_27_44.png",
              "/home/pi/Desktop/project/img/d_c__in_2020_01_13-16_36_43.png",
              "/home/pi/Desktop/project/img/d_c__in_2020_01_09-17_35_53.png",
              "/home/pi/Desktop/project/img/d_c__in_2020_01_13-16_34_46.png"]
falsepositves = falsepositves + false_pos2

luminanz_yes = defaultdict(int)
luminanz_no = defaultdict(int)
sql1 = "select timestamp from od2 where   timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and object is not null and img_url not in """ + str(
    tuple(falsepositves)) + """"""

result1 = db_mac.execute(sql1)
for row1 in result1:

    sql2 = """select luminance from brightness where  timestamp = '""" + str(row1[0]) + """' """
    result2 = db_mac.execute(sql2)

    for row2 in result2:
        luminanz_yes[float(row2[0])] += 1

sql1 = "select timestamp from od2 where   timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and object is null and img_url not in """ + str(
    tuple(falsepositves)) + """"""

result1 = db_mac.execute(sql1)
for row1 in result1:

    sql2 = """select luminance from brightness where  timestamp = '""" + str(row1[0]) + """' """
    result2 = db_mac.execute(sql2)

    for row2 in result2:
        luminanz_no[float(row2[0])] += 1

print(sorted(luminanz_yes.items(), key=lambda i: i[0]))
print(sorted(luminanz_no.items(), key=lambda i: i[0]))

percentage = defaultdict(int)
for key, i in luminanz_yes.items():
    if i != 0 and luminanz_no[key] and luminanz_no[key] != 0:

        perc = i / (i + luminanz_no[key]) * 100
        percentage[key] = perc
    else:
        percentage[key] = 0

print(percentage)
fig, ax = plt.subplots(figsize=(10, 4))

N = len(percentage.keys())
ind = np.arange(N)  # the x locations for the groups
width = 0.008  # the width of the bars

p1 = ax.bar(percentage.keys(), percentage.values(), width, color="#85c1e9")
ax.set_ylim(0, 100)
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_major_locator(MultipleLocator(0.02))
ax.set_title('Erkennungen nach Luminanz')
ax.set_xlabel("Luminanz")
ax.set_ylabel("Anzahl in %")
# ax.set_xticks(ind + width / 2)
# ax.set_xticklabels([""] +  ["< 61"]  + [str(i[0]) for i in percentage])

ax.autoscale_view()
plt.tight_layout()
plt.show()
