from collections import OrderedDict
from collections import defaultdict

import db_mac
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator

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
              "/home/pi/Desktop/project/img/d_c__in_2020_01_13-16_34_46.png"]
falsepositves += false_pos2

yes_step = defaultdict(int)
no_step = defaultdict(int)
percentage = defaultdict(int)

sql = """
select humidity,
       count(*) as cnt
       from od2 where humidity is not null and bound like 'in' and img_url not in """ + str(tuple(falsepositves)) + """ and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and object is not null
group by 1 
order by 2;
    """

result = db_mac.execute(sql)
for row in result:
    for s in range(60, 100, 5):
        if row[0] > s and row[0] <= s + 5:
            yes_step[str(s + 1) + " - " + str(s + 5)] += row[1]

sql = """select humidity,
       count(*) as cnt
       from od2 where humidity is not null and bound like 'in' and img_url not in """ + str(tuple(falsepositves)) + """ and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and object is  null
group by 1 
order by 2;
    """

result = db_mac.execute(sql)
for row in result:
    for s in range(60, 100, 5):
        if row[0] > s and row[0] <= s + 5:
            no_step[str(s + 1) + " - " + str(s + 5)] += row[1]

values_ordered = OrderedDict()
for k in sorted(no_step.keys()):
    tup = (yes_step[k], no_step[k])
    values_ordered[k] = tup

print(values_ordered)

fig, ax = plt.subplots(figsize=(10, 4))

ind = np.arange(len(no_step) + 1)  # the x locations for the groups
width = 0.3  # the width of the bars

p1 = ax.bar(ind, [0] + [i[0] for i in values_ordered.values()], width, color="#117a65")
p2 = ax.bar(ind + width, [0] + [i[1] for i in values_ordered.values()], width, color="#d7456c")
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.set_title('Erkennungen nach rel. Luftfeuchtigkeit')
ax.set_xlabel("Wolkenbedeckung in %")
ax.set_ylabel("Anzahl")
ax.set_xticks(ind + width / 2)

ax.legend((p1[0], p2[0]), ('erkannt', 'nicht erkannt'))

ax.set_xticklabels(["< 61"] + [str(i) for i in values_ordered.keys()])

ax.autoscale_view()
plt.tight_layout()
plt.show()
