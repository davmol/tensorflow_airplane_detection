import db_mac
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import (MultipleLocator)

sql = """select 
sqrt(power((ST_X(d.geom) - 382983),2) + power((ST_Y(d.geom)  - 5824610),2)) as distance, d.speed*0.514444
 from dump d , bufferzone b
 where
  st_within(d.geom, b.geom)
 and d.vert_rate > 0 ---start
 --and d.vert_rate <= 0 -- land
 and d.track  > 70 and d.track < 90 -- start
 --and d.track  > 250 and d.track < 270 -- land
 and b.name like 'TXL'
and d.speed <= 300
and sqrt(power((ST_X(d.geom) - 382983),2) + power((ST_Y(d.geom)  - 5824610),2)) <= 11000

 """

data = np.array(list(db_mac.execute(sql))).T
distance = [round(i) for i in data[0, :]]
speed = [round(i) for i in data[1, :]]

fig, ax = plt.subplots(figsize=(10, 4))
ax.grid(True)
ax.set_title('Fluggeschwindigkeiten im Geofence mit postiver Vertikalrate')
ax.margins(0)
# ax.axvline(x=4191,color='red')
ax.set_xlim(0, 11000)
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_major_locator(MultipleLocator(1000))
ax.set(ylabel="Geschwindigkeit in Meter/Sekunde")
ax.set(xlabel="Distanz zum Zentroid (E:382983 N:5824610 (UTM-33N WGS84) in Meter")
ax.scatter(distance, speed, 0.01)
plt.tight_layout()
plt.show()
