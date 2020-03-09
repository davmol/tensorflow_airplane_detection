import datetime
import multiprocessing as mp
import time
from collections import defaultdict

import db_mac2
import requests

t = time.time()

station = [10382, "DE", "Berlin / Tegel", 52.5667, 13.3167, 37, "EDDT", 10382, "TXL", "Europe/Berlin"]

dates = [("2020-01-07", "2020-01-15")]
insert_dict = defaultdict(tuple)

hist_weather_list = []

for d in dates:
    end = d[1]
    start = d[0]
    print(start, end)
    url = "https://api.meteostat.net/v1/history/hourly?station={station}&start={start}&end={end}&time_zone={timezone}&&time_format=Y-m-d%20H:i&key=wzwi2YR5".format(
        station=station[0], start=start, end=end, timezone=station[-1])

    response = requests.get(url)
    weather = response.json()
    print(weather)
    for i in weather["data"]:
        hist_weather_list.append(i)

c1 = db_mac2.DB_Conn()
sql = "select timestamp, altitude from od2 order by timestamp asc where bound = 'in'"
result = c1.execute(sql)

hours, rem = divmod(time.time() - t, 3600)
minutes, seconds = divmod(rem, 60)
print("step1 {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))


def find_parameters(x):
    conn = db_mac2.DB_Conn()
    for row in result[x[0]:x[1]]:
        try:
            ts_dump = datetime.datetime.timestamp(row[0])
            for i, hour in enumerate(hist_weather_list):
                ts1 = datetime.datetime.timestamp(datetime.datetime.strptime(hour["time"], '%Y-%m-%d %H:%M:%S'))

                ts2 = datetime.datetime.timestamp(
                    datetime.datetime.strptime(hist_weather_list[i + 1]["time"], '%Y-%m-%d %H:%M:%S'))

                if ts1 <= ts_dump and ts_dump < ts2:
                    T0 = hour["temperature"]
                    P = hour["pressure"]
                    P0 = 1013.25
                    h = (273.15 + T0) / 0.0065 * (1 - (P / P0) ** (1 / 5.255))

                    newh = row[1] - h

                    sql2 = """UPDATE od2 SET altitude_cor = """ + str(newh) + """ where timestamp = '""" + str(
                        row[0]) + """';"""

                    conn.execute(sql2)

        except:
            pass


step1 = int(len(result) / 4)
step2 = 2 * step1
step3 = 3 * step1
step4 = len(result)
steps = [[0, step1], [step1, step2], [step2, step3, ], [step3, step4, ]]

pool = mp.Pool(mp.cpu_count())
pool.map(find_parameters, steps)

hours, rem = divmod(time.time() - t, 3600)
minutes, seconds = divmod(rem, 60)
print("step2 {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
