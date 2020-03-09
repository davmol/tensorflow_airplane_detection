import db_mac
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator)

sql = """select  det_dist_surf + 4191, altitude from od2 where bound like 'in'
 """

data = np.array(list(db_mac.execute(sql))).T
det_dist = [round(i) for i in data[0, :]]
alt = [round(i) for i in data[1, :]]

fig, ax = plt.subplots(figsize=(10, 4))
ax.grid(True)
ax.set_title('Detektionsentfernung im Geofence')
ax.margins(0)
ax.axvline(x=4191, color='red')
ax.set_ylim(min(alt), 1000)
ax.set_xlim(0, 11000)
ax.yaxis.set_major_locator(MultipleLocator(100))
ax.xaxis.set_major_locator(MultipleLocator(1000))
ax.set(ylabel="Höhe in Meter")
ax.set(xlabel="Distanz zum Zentroid (E:382983 N:5824610 (UTM-33N WGS84) in Meter")
ax.scatter(det_dist, alt, 0.1)

plt.show()

# 1
# 20
# 21
# 27
# 28
# 29
# 30
