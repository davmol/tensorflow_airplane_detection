import datetime
import operator
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
import db_mac
from _collections import OrderedDict


# precision
airlines_score = dict()

sql1 = "select aircraft, count(*) from od2 where bound like 'in' and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and aircraft is not null group by 1 order by 2 desc limit 15"
result1 = db_mac.execute(sql1)

aircrafts = set()


for row1 in result1:

    if row1[0] == "A20N":
        aircrafts.add("A320")

    elif row1[0] == "A21N":
        aircrafts.add("A321")

    elif row1[0] == "B738" or row1[0] == "B739":
        aircrafts.add("B737")

    else:
        aircrafts.add(row1[0])


print(aircrafts)
for a in aircrafts:


    sql2 = """select precision from od2 where object is not null and aircraft like '"""+ str(a) +"""' and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time """
    result2 = db_mac.execute(sql2)
    values = []
    for row2 in result2:
        if len(result2) > 0:
            prec_list = row2[0].replace("[", "").replace("]", "").split(",")


            for i in prec_list:
                values.append(float(i))

            p = round(np.mean(values) * 100, 2)

            airlines_score[a] = p


sorted_aircraft_score = sorted(airlines_score.items(), key=operator.itemgetter(1))
print(sorted_aircraft_score)
prec_aircraft = defaultdict(float)
for a in sorted_aircraft_score:

    count_all = 0
    all_det = 0
    sql1 = """select count(*) from od2 where bound like 'in' and  aircraft like '""" + str(a[0]) +"""' and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time"""
    result1 = db_mac.execute(sql1)
    for row1 in result1:
        print(row1[0])
        count_all = row1[0]


    sql2 = """select count(*) from od2 where bound like 'in' and object is not null and  aircraft like '""" + str(a[0]) + """' and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time"""
    result2 = db_mac.execute(sql2)
    for row2 in result2:
        print(row2[0])
        all_det = row2[0]


    prec_aircraft[a[0]] = round(all_det / count_all * 100, 2)


print(prec_aircraft)


N = len(sorted_aircraft_score)

fig, ax = plt.subplots(figsize=(10, 4))

ind = np.arange(N)  # the x locations for the groups
width = 0.2  # the width of the bars
p1 = ax.bar(ind, [i[1] for i in sorted_aircraft_score], width, color="#2980b9")



ax.set_title('Erkennungsrate Flugzeugtypen und Ähnlichkeitswahrscheinlichkeit')


ax.set_xticks(ind + width / 2)
ax.set_xticklabels([i[0] for i in sorted_aircraft_score], rotation=90)
ax.set_ylim(88,100)

ax.set_ylabel('Ähnlichkeitswahrscheinlichkeit in %', color="#2980b9")
#ax.autoscale_view()

ax2 = ax.twinx()

p2 = ax2.bar(ind + width, prec_aircraft.values(), width, color="#e67e22")

ax2.set_ylabel('Erkennung der Fluggesellschaft in %', color="#e67e22")
ax2.set_xticks(ind + width / 2)
#ax2.set_xticklabels([i[0] for i in prec_airline], rotation=90)
ax2.set_ylim(0,100)




plt.tight_layout()
plt.show()
