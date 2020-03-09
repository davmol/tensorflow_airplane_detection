from collections import OrderedDict
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

luminanz_yes = defaultdict(int)
sql1 = "select timestamp from od2 where   timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and object is not null and img_url not in """ + str(
    tuple(falsepositves)) + """"""

result1 = db_mac.execute(sql1)
for row1 in result1:

    sql2 = """select luminance, timestamp from brightness where  timestamp = '""" + str(row1[0]) + """' """
    result2 = db_mac.execute(sql2)

    for row2 in result2:
        luminanz_yes[float(row2[0])] += 1

luminanz_no = defaultdict(int)
sql1 = "select timestamp from od2 where  timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and object is null and img_url not in """ + str(
    tuple(falsepositves)) + """"""

result1 = db_mac.execute(sql1)
for row1 in result1:

    sql2 = """select luminance, timestamp from brightness where  timestamp = '""" + str(row1[0]) + """' """
    result2 = db_mac.execute(sql2)

    for row2 in result2:
        luminanz_no[float(row2[0])] += 1

values_ordered = OrderedDict()

for i in range(0, 42, 1):
    i = i / 100
    values_ordered[i] = (0, 0)

print(values_ordered)

for k, v in sorted(luminanz_yes.items()):
    if not luminanz_no[k]:
        values_ordered[k] = (v, 0)

    else:
        values_ordered[k] = (v, luminanz_no[k])

for k, v in sorted(luminanz_no.items()):
    if not luminanz_yes[k]:
        values_ordered[k] = (0, v)

    else:
        values_ordered[k] = (luminanz_yes[k], v)

print(values_ordered.values())
print([i[0] for i in values_ordered.values()])

fig, ax = plt.subplots(figsize=(10, 4))

ind = np.arange(len(values_ordered))  # the x locations for the groups
width = 0.4  # the width of the bars

p1 = ax.bar(ind, [i[0] for i in values_ordered.values()], width, color="#117a65")
p2 = ax.bar(ind + width, [i[1] for i in values_ordered.values()], width, color="#d7456c")
ax.yaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.set_title('Erkennungen nach Luminanz')
ax.set_xlabel("Luminanz")
ax.set_ylabel("Anzahl")
ax.set_xticks(ind + width / 2)

ax.legend((p1[0], p2[0]), ('erkannt', 'nicht erkannt'))

ax.set_xticklabels([str(i) for i in values_ordered.keys()], rotation=90)

ax.autoscale_view()
plt.tight_layout()
plt.show()
