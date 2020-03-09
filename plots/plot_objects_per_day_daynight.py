import matplotlib.pyplot as plt
from matplotlib.pyplot import  MultipleLocator
import numpy as np
from _collections import defaultdict
import db_mac

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



sql = """with nn as (select DISTINCT(DATE(timestamp)) as date1, 
       count(*) as count1
	  
from od2 where object is not null and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time  and img_url not in """ + str(tuple(falsepositves))  + """
group by 1
order by 1 asc),

nn2 as 
(select DISTINCT(DATE(timestamp)) as date2, 
       count(*) as count2
from od2 
where  bound like 'in'  and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time  and img_url not in """ + str(tuple(falsepositves))  + """
group by 1
order by 1 asc )

select nn.date1, nn.count1, nn2.count2  from nn join nn2 on nn.date1 = nn2.date2
    """

result = db_mac.execute(sql)
data = np.array(list(db_mac.execute(sql))).T
date = [i for i in data[0, :]]
obj = [round(i) for i in data[1, :]]
all = [round(i) for i in data[2, :]]


N = 8
fig, ax = plt.subplots(figsize=(10, 4))

ind = np.arange(N)  # the x locations for the groups
width = 0.2  # the width of the bars
p1 = ax.bar(ind, obj, width, color="#febf84")

p2 = ax.bar(ind + width, all, width, color="#651a80")

ax.set_title('Objekterkennungen zwischen den Blauen Stunden')
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(date)
ax.yaxis.set_major_locator(MultipleLocator(10))

ax.set_xlabel("Tage")
ax.set_ylabel("Anzahl")
ax.legend((p1[0], p2[0]), ('erkannt', 'Gesamt Anzahl Landungen'))
ax.autoscale_view()
plt.tight_layout()
plt.show()
