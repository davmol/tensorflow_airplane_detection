import datetime

import db_mac
import matplotlib.pyplot as plt
from brokenaxes import brokenaxes

t_min_2020_01_07 = datetime.datetime.strptime('2020-01-07 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_07 = datetime.datetime.strptime('2020-01-07 17:00', '%Y-%m-%d %H:%M')
t_min_2020_01_08 = datetime.datetime.strptime('2020-01-08 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_08 = datetime.datetime.strptime('2020-01-08 17:00', '%Y-%m-%d %H:%M')

fig = plt.figure(figsize=(5, 2))

# humidity
hum = []
hum_t = []
sql = "select humidity, timestamp from od2 where timestamp > '2020-01-07' and timestamp < '2020-01-09' and humidity is not null order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    hum.append(float(row[0]))
    hum_t.append(row[1])

bax = brokenaxes(xlims=((t_min_2020_01_07, t_max_2020_01_07), (t_min_2020_01_08, t_max_2020_01_08)), hspace=.05)

bax.plot(hum, hum_t)

# bax.legend(loc=3)
# bax.set_xlabel('time')
# bax.set_ylabel('value')


fig.autofmt_xdate()
# fig.tight_layout()


plt.show()
