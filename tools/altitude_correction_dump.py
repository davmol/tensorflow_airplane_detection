import multiprocessing as mp
import time
from collections import defaultdict

import db_mac2

t = time.time()
values = defaultdict(tuple)
c = db_mac2.DB_Conn()

sql = """select timestamp, altitude, temperature, pressure from dump;"""

result = c.execute(sql)

hours, rem = divmod(time.time() - t, 3600)
minutes, seconds = divmod(rem, 60)
print("step1 {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))


def update(x):
    conn = db_mac2.DB_Conn()
    for row in result[x[0]:x[1]]:
        timestamp = row[0]
        alt = float(row[1])
        temp = float(row[2])
        press = float(row[3])

        T0 = temp
        P = press
        P0 = 1013.25
        h = (273.15 + T0) / 0.0065 * (1 - (P / P0) ** (1 / 5.255))

        newh = alt - round(round(h) * 0.3048)

        sql2 = """UPDATE dump SET altitude_cor = """ + str(newh) + """where timestamp = '""" + str(timestamp) + """';"""

        conn.execute(sql2)


step1 = int(len(result) / 4)
step2 = 2 * step1
step3 = 3 * step1
step4 = len(result)
steps = [[0, step1], [step1, step2], [step2, step3, ], [step3, step4, ]]

pool = mp.Pool(mp.cpu_count())
pool.map(update, steps)

hours, rem = divmod(time.time() - t, 3600)
minutes, seconds = divmod(rem, 60)
print("step2 {:0>2}:{:0>2}:{:05.2f}".format(int(hours), int(minutes), seconds))
