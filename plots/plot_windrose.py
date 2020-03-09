import db_mac
import matplotlib.cm as cm
import numpy as np
from matplotlib import pyplot as plt
from windrose import WindroseAxes

#https://windrose.readthedocs.io/en/latest/usage.html#script-example


units = "m/s"

def speed_labels(spd_bins, units):
  labels = []
  for left, right in zip (spd_bins[:-1], spd_bins[1:]):
    if left == spd_bins[1:3]:
      labels.append('calm'.format(right))
    elif np.isinf(right):
      labels.append('>{} {}'.format(left, units))
    else:
      labels.append('{} - {} {}'.format(left, right, units))
  labels.append(">12")
  print(labels)
  return labels


# Create wind speed and direction variables

ws = []
wd = []

sql = "Select wind_speed, wind_direction from od2"
result = db_mac.execute(sql)


for row in result:
    if row[0] is not None and row[1] is not None:
        ws.append(float(row[0]))
        wd.append(float(row[1]))


#ws = np.random.random(500) * 6
#wd = np.random.random(500) * 360

#bins_range = np.arange(1,6,1)
spd_bins = [0, 2, 4, 6, 8, 10, 12] #, np.inf]
# spd_labels = speed_labels(spd_bins, units='m/s')

fig = plt.figure(figsize=(10, 10))

ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed=True, opening=0.8, bins=spd_bins, edgecolor='white', cmap = cm.magma_r)
ax.set_yticks(np.arange(5, 30, step=5))
ax.set_yticklabels([str(i) + " %" for i in np.arange(5, 30, step=5)])
#ax.set_legend(labels = [label + " m/s" for label in ax.get_label()], title="Windrose", loc="upper left")

#ax.set_legend(loc=(-0.12, 2), labels=spd_labels)
# ax.set_legend()
ax.set_title("Windrosenplot Windrichtung & Windstärke")

# für Grad richtungen

degrees = ["90°", "45°","0°","315°","270°","225°","180°","135°"]
ax.set_xticklabels(labels=degrees)

# plt.show()
plt.savefig('WindRose.png')
