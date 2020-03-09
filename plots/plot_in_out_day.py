import db_mac
import numpy as np
import datetime
import matplotlib.pyplot as plt
import db_mac

# series = read_csv('daily-minimum-temperatures.csv', header=0, index_col=0, parse_dates=True, squeeze=True)


timestamps = []
values_in= [140,157,160,195,142,162,177,47]
values_out = [83,93,81,85,80,68,72,23]
xlabels = [datetime.datetime.strptime(i, '%Y-%m-%d') for i in ["2020-01-07","2020-01-08","2020-01-09","2020-01-10","2020-01-11","2020-01-12","2020-01-13","2020-01-14"]]


ind = np.arange(len(values_in))
fig, ax = plt.subplots(figsize=(10, 4))

width = 0.2  # the width of the bars
p1 = ax.bar(ind, values_in, width, color="#febf84")
p2 = ax.bar(ind + width, values_out, width, color="#d7456c")

ax.set_title('Übersicht Anzahl landender und startender Flugzeuge')
ax.set_ylabel("Anzahl/Tag")
ax.set_xlabel("Beobachtungszeitraum")
ax.set_xticks(ind + width / 2)
ax.set_xticklabels(["2020-01-07","2020-01-08","2020-01-09","2020-01-10","2020-01-11","2020-01-12","2020-01-13","2020-01-14"])

ax.legend((p1[0], p2[0]), ('landend', 'startend' ))
ax.autoscale_view()
plt.tight_layout()
plt.show()
