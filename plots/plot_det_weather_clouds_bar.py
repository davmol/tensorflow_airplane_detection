import matplotlib.pyplot as plt
from matplotlib.pyplot import MultipleLocator
import numpy as np
from _collections import defaultdict

import db_mac

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
yes_step["0"] += 0
no_step["0"] += 0

for s in range(0, 100, 10):
    yes_step[str(s + 1) + " - " + str(s + 10)] += 0
    no_step[str(s + 1) + " - " + str(s + 10)] += 0

percentage = defaultdict(int)

sql = """
select cloud_coverage,
       count(*) as cnt
       from od2 where bound like 'in' and img_url not in """ + str(tuple(falsepositves))  + """ and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and object is not null
group by 1 
order by 2;
    """

result = db_mac.execute(sql)
for row in result:
    if type(row[0]) == int:
        for s in range(0, 100, 10):
            if row[0] > s and row[0] <= s + 10:
                yes_step[str(s + 1) + " - " + str(s + 10)] += row[1]
        else:
            yes_step["Null"] = row[1]

print(yes_step)


sql = """select cloud_coverage,
       count(*) as cnt
       from od2 where bound like 'in' and img_url not in """ + str(tuple(falsepositves))  + """ and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and object is  null
group by 1 
order by 2;
    """


result = db_mac.execute(sql)
for row in result:
    if type(row[0]) == int:
        for s in range(0, 100, 10):
            if row[0] > s and row[0] <= s + 10:
                no_step[str(s + 1) + " - " + str(s + 10)] += row[1]
    else:
        no_step["Null"] = row[1]





yes = sorted(yes_step.items(), key = lambda i: i[0])
no = sorted(no_step.items(), key = lambda i: i[0])

print(yes)
print(no)
fig, ax = plt.subplots(figsize=(10, 4))

ind = np.arange(len(yes))  # the x locations for the groups
width = 0.3  # the width of the bars

p1 = ax.bar(ind, [i[1] for i in yes], width, color="#117a65")
p2 = ax.bar(ind + width, [i[1] for i in no], width, color="#d7456c")
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_major_locator(MultipleLocator(1))
ax.set_title('Erkennungen nach Wolkenbedeckung')
ax.set_xlabel("Wolkenbedeckung in %")
ax.set_ylabel("Anzahl")
ax.set_xticks(ind + width / 2)

ax.legend((p1[0], p2[0]), ('erkannt', 'nicht erkannt' ))

ax.set_xticklabels([str(i[0]) for i in yes])

ax.autoscale_view()
plt.tight_layout()
plt.show()
