from collections import OrderedDict
from collections import defaultdict

import db_mac
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.pyplot import MultipleLocator

falses = defaultdict(list)
sql = """select object, img_url from od2 where object is not null and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and weather_status like 'Clouds'
    """

result = db_mac.execute(sql)

for row in result:
    if len(row[0].split(",")) > 5:
        falses["falses"].append(row[1])

falsepositves = []
for v in falses.values():
    falsepositves = v
print(len(falsepositves))

weather = defaultdict(tuple)

sql = """select distinct weather_status_detail from od2 where timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time and  img_url not in """ + str(
    tuple(falsepositves)) + """
    """
result = db_mac.execute(sql)
for row in result:
    if row[0] is not None:
        weather[row[0]] = (0, 0)
    else:
        weather["Null"] = (0, 0)

print(weather)
for w in weather.keys():
    if w == "Null":
        sql = """with nocount as (select count(*) as nope from od2 where bound like 'in' and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time  and object is null and weather_status_detail is null),
        yescount as (select count(*) as yes from od2 where bound like 'in' and img_url not in """ + str(
            tuple(falsepositves)) + """ and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time  and object is not null and weather_status_detail is null)
        select nocount.nope, yescount.yes from nocount, yescount
        
        
        """
    else:
        sql = """with nocount as (select count(*) as nope from od2 where bound like 'in' and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time  and object is null and weather_status_detail like '""" + w + """'),
                yescount as (select count(*) as yes from od2 where bound like 'in' and img_url not in """ + str(
            tuple(
                falsepositves)) + """ and timestamp::time > '07:59:00'::time and timestamp::time <= '16:40:00'::time  and object is not null and weather_status_detail like '""" + w + """')
                select nocount.nope, yescount.yes from nocount, yescount


                """

    result = db_mac.execute(sql)
    for row in result:
        weather[w] = (row[0], row[1])

weather_ordered = OrderedDict()
weather_ordered["few clouds"] = weather["few clouds"]
weather_ordered["scattered clouds"] = weather["scattered clouds"]
weather_ordered["broken clouds"] = weather["broken clouds"]
weather_ordered["light intensity drizzle"] = weather["light intensity drizzle"]
weather_ordered["light intensity drizzle rain"] = weather["light intensity drizzle rain"]
weather_ordered["light rain"] = weather["light rain"]
weather_ordered["moderate rain"] = weather["moderate rain"]
weather_ordered["mist"] = weather["mist"]
weather_ordered["Null"] = weather["Null"]

print(weather_ordered)

N = len(weather_ordered.keys())

fig, ax = plt.subplots(figsize=(5, 5))

ind = np.arange(N)  # the x locations for the groups
width = 0.3  # the width of the bars

p1 = ax.bar(ind, [i[1] for i in weather_ordered.values()], width, color="#117a65")
p2 = ax.bar(ind + width, [i[0] for i in weather_ordered.values()], width, color="#d7456c")

ax.yaxis.set_major_locator(MultipleLocator(10))
ax.set_title('Erkennungen nach detailiertem Wetterstatus')
ax.set_xlabel("detailierter Wetterstatus")
ax.set_ylabel("Anzahl")
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(weather_ordered.keys(), rotation=90)

ax.legend((p1[0], p2[0]), ('erkannt', 'nicht erkannt'))
ax.autoscale_view()

plt.show()
