import datetime

import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
from collections import defaultdict
import db_mac



sql = """select object, img_url from od2 where object is not null and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time 
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
"/home/pi/Desktop/project/img/d_c__in_2020_01_13-16_34_46.png",]
falsepositves += false_pos2



# precision
luminance = defaultdict(float)
sql1 = """select precision, timestamp from od2 where timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and object is not null and img_url not in """ + str(tuple(falsepositves)) + """"""
result1 = db_mac.execute(sql1)
for row1 in result1:

    prec_list = row1[0].replace("[", "").replace("]", "").split(",")

    values = []
    for i in prec_list:
        values.append(float(i))
    if len(values) < 6:
        p = round(np.mean(values) * 100, 3)


        sql2 = """select luminance from brightness where  timestamp = '""" + str(row1[1]) + """'"""
        result2 = db_mac.execute(sql2)

        for row2 in result2:
            if len(result2) > 0:

                luminance[float(row2[0])] = p


fig, ax = plt.subplots(figsize=(10, 5))
ax.grid(True)

ax.margins(0)
ax.yaxis.set_major_locator(MultipleLocator(2.5))
ax.xaxis.set_major_locator(MultipleLocator(0.02))
ax.set_title('Ähnlichkeitswahrscheinlichkeit und Luminanz')
ax.set_xlabel("Luminanz")
ax.set_ylabel("Ähnlichkeitswahrscheinlichkeit in %")
ax.set_ylim(80,100)
ax.set_xlim(0,0.4)


ax.bar(luminance.keys(), luminance.values(), 0.008)

plt.show()
