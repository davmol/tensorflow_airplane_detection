import db_mac
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator)

sql = """select 
sqrt(power((ST_X(d.geom) - 382983),2) + power((ST_Y(d.geom)  - 5824610),2)) as distance, d.altitude_cor*0.3048
 from dump d , bufferzone b
 where
  st_within(d.geom, b.geom)
 --and d.vert_rate > 0 ---start
 and d.vert_rate <= 0 -- land
 and d.altitude_cor*0.3048 <=800
 --and d.track  > 70 and d.track < 90 -- start
 and d.track  > 250 and d.track < 270 -- land
 and b.name like 'TXL'
 and sqrt(power((ST_X(d.geom) - 382983),2) + power((ST_Y(d.geom)  - 5824610),2)) <= 11000
 --and extract(day from timestamp) = 29
 """

data = np.array(list(db_mac.execute(sql))).T
distance = [round(i) for i in data[0, :]]
alt1 = [round(i) for i in data[1, :]]

sql = """select 
sqrt(power((ST_X(d.geom) - 382983),2) + power((ST_Y(d.geom)  - 5824610),2)) as distance, d.altitude*0.3048
 from dump d , bufferzone b
 where
  st_within(d.geom, b.geom)
 --and d.vert_rate > 0 ---start
 and d.vert_rate <= 0 -- land
 and d.altitude*0.3048 <=800
 --and d.track  > 70 and d.track < 90 -- start
 and d.track  > 250 and d.track < 270 -- land
 and b.name like 'TXL'
 and sqrt(power((ST_X(d.geom) - 382983),2) + power((ST_Y(d.geom)  - 5824610),2)) <= 11000
 --and extract(day from timestamp) = 29
 """

data = np.array(list(db_mac.execute(sql))).T
distance = [round(i) for i in data[0, :]]
alt = [round(i) for i in data[1, :]]

sql = """select  det_dist_surf + 5200, altitude_cor from od2 where bound like 'in'
 """

data = np.array(list(db_mac.execute(sql))).T
det_dist = [round(i) for i in data[0, :]]
alt2 = [round(i) for i in data[1, :]]

sql = """select  det_dist_surf + 5200, altitude_cor from od2 where bound like 'in' and object is not null
 """

data = np.array(list(db_mac.execute(sql))).T
det_dist_obj = [round(i) for i in data[0, :]]
alt3 = [round(i) for i in data[1, :]]

fig, ax = plt.subplots(figsize=(10, 5))
ax.grid(True)
ax.set_title('Flughöhen im Geofence')
ax.margins(0)
ax.axvline(x=4191, color='red')
ax.set_ylim(min(alt1), 1000)
ax.set_xlim(0, 11000)
ax.yaxis.set_major_locator(MultipleLocator(100))
ax.xaxis.set_major_locator(MultipleLocator(1000))
ax.set(ylabel="Höhe in Meter")
ax.set(xlabel="Distanz zum Flughafen-Zentroid (E:382983 N:5824610, WGS84 UTM-33N) in Meter")
ax.scatter(distance, alt, 0.01, "k", alpha=0.5)
ax.scatter(distance, alt1, 0.01, "b", alpha=0.5)
ax.scatter(det_dist, alt2, 0.8, "g", alpha=0.5)
ax.scatter(det_dist_obj, alt3, 0.8, "r", alpha=0.5)
plt.tight_layout()
plt.show()
