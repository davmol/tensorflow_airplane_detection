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


ind = np.arange(8)
fig, ax = plt.subplots(figsize=(10, 4))

width = 0.2  # the width of the bars

new_yes = []
for c, i in enumerate(values_in):
    if i != 0 and values_out[c] != 0:
        r = i/(values_out[c]+ i) * 100
        new_yes.append(r)
    else:
        new_yes.append(0)



ax.set_title('Prozentueller Anteil landender Flugzeuge')
ax.set_ylabel("Anzahl in %")
ax.set_xlabel("Beobachtungszeitraum")
#ax.set_xticks(ind + width / 2)
ax.set_xticklabels(["","2020-01-07","2020-01-08","2020-01-09","2020-01-10","2020-01-11","2020-01-12","2020-01-13","2020-01-14"])

p1 = ax.bar(ind, new_yes, width, color="#febf84")
ax.autoscale_view()
plt.tight_layout()
plt.show()

