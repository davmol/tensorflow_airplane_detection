import matplotlib.pyplot as plt
import numpy as np
from _collections import defaultdict
import db_mac
import datetime
from matplotlib.pyplot import MultipleLocator

sql = """select object, img_url from od2 where object is not null
    """
falses = defaultdict(list)
result = db_mac.execute(sql)

for row in result:
    if len(row[0].split(",")) > 5:
        falses["falses"].append(row[1])

falsepositves = []
for v in falses.values():
    falsepositves = v
print(falsepositves)


scores = defaultdict(list)
sql1 = """select precision, timestamp from od2 where timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and precision is not null  and img_url not in """ + str(tuple(falsepositves))  + """ order by timestamp asc ;"""
result1 = db_mac.execute(sql1)
for row1 in result1:
    prec_list = row1[0].replace("[", "").replace("]", "").split(",")
    values = []
    for i in prec_list:
        values.append(float(i))
    if len(values) < 6:


        scores[row1[1].strftime("%Y-%m-%d")].append(round(np.mean(values) * 100, 2))




sql = """with nn as (select DISTINCT(DATE(timestamp)) as date1, 
       count(*) as count1

from od2 where object is not null and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time  and img_url not in """ + str(
    tuple(falsepositves)) + """
group by 1
order by 1 asc),

nn2 as 
(select DISTINCT(DATE(timestamp)) as date2, 
       count(*) as count2
from od2 
where  bound like 'in'  and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time  and img_url not in """ + str(
    tuple(falsepositves)) + """
group by 1
order by 1 asc )

select nn.date1, nn.count1, nn2.count2  from nn join nn2 on nn.date1 = nn2.date2
    """

result = db_mac.execute(sql)
data = np.array(list(db_mac.execute(sql))).T
date = [i for i in data[0, :]]
obj = [i for i in data[1, :]]
prc = []
for c, i in enumerate(obj):
    prc.append(i / data[2, :][c] * 100)


score = [(np.mean(i)) for i in scores.values()]
lbl =  [str(i) for i in scores.keys()]
print(lbl)

print(prc, score)
fig, ax = plt.subplots(figsize=(10, 4))

ind = np.arange(len(scores.keys()))  # the x locations for the groups

p1 = ax.scatter(prc, score, 40, color="#2c3e50")



ax.set_title('Ähnlichkeitswahrscheinlichkeit')
ax.set_xlabel("Anteil an erkannten Objekten pro Tag in %")
ax.set_ylabel("Ähnlichkeitswahrscheinlichkeit in %")
#ax.set_ylim(95,100)
#ax.set_xticks(ind + width / 2)
ax.yaxis.set_major_locator(MultipleLocator(0.5))
ax.xaxis.set_major_locator(MultipleLocator(5))
#ax.set_xticklabels([""]+ [str(i) for i in scores.keys()])
ax.grid(True)


for i, txt in enumerate(lbl):
    ax.text(prc[i] + .03, score[i] + .03, txt, fontsize=9)


ax.autoscale_view()
plt.tight_layout()
plt.show()
