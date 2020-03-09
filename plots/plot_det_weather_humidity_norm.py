from _collections import defaultdict

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

for key, i in yes_step.items():
    if i != 0:
        perc = i / (i + no_step[key]) * 100
        percentage[key] = perc
    else:
        percentage[key] = 0

percentage = sorted(percentage.items(), key=lambda i: i[0])

print(percentage)
N = len(percentage) + 1

fig, ax = plt.subplots(figsize=(10, 4))

ind = np.arange(N)  # the x locations for the groups
width = 0.3  # the width of the bars

p1 = ax.bar(ind, [0] + [i[1] for i in percentage], width, color="#5499c7")

ax.yaxis.set_major_locator(MultipleLocator(5))
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.set_title('Erkennungen nach rel. Luftfeuchtigkeit')
ax.set_xlabel("rel. Luftfeuchtigkeit in %")
ax.set_ylabel("Objekterkennungsrate in %")
# ax.set_xticks(ind + width / 2)
ax.set_xticklabels([""] + ["< 61"] + [str(i[0]) for i in percentage])

ax.autoscale_view()
plt.tight_layout()
plt.show()
