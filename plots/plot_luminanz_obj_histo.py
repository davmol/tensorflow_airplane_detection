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
falsepositves += false_pos2

luminanz = defaultdict(int)
sql1 = "select timestamp from od2 where   timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and object is not null and img_url not in """ + str(
    tuple(falsepositves)) + """"""

result1 = db_mac.execute(sql1)
for row1 in result1:

    sql2 = """select luminance, timestamp from brightness where  timestamp = '""" + str(row1[0]) + """' """
    result2 = db_mac.execute(sql2)

    for row2 in result2:
        luminanz[float(row2[0])] += 1

fig, ax = plt.subplots(figsize=(10, 4))

N = len(luminanz.keys())
ind = np.arange(N)  # the x locations for the groups
width = 0.008  # the width of the bars

p1 = ax.bar(luminanz.keys(), luminanz.values(), width, color="#85c1e9")

ax.yaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_major_locator(MultipleLocator(0.02))
ax.set_title('Verteilungen der Objekterkennungen zur Luminanz')
ax.set_xlabel("Luminanz")
ax.set_ylabel("Anzahl")
# ax.set_xticks(ind + width / 2)
# ax.set_xticklabels([""] +  ["< 61"]  + [str(i[0]) for i in percentage])

ax.autoscale_view()
plt.tight_layout()
plt.show()
