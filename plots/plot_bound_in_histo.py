import db_mac
import matplotlib.pyplot as plt
import numpy as np

sql = """select date_trunc('hour', timestamp),  count(1) from od2 where bound like 'in' group by 1 order by 1"""
result = db_mac.execute(sql)

print(result)

data = np.array(list(db_mac.execute(sql))).T
timestamp = data[0, :]
count = data[1, :]

print(timestamp)
print(count)

bar_width = 0.03
fig, ax = plt.subplots(figsize=(20, 14))

ax.set(ylabel="")
ax.set(xlabel="")
ax.bar(timestamp, count, width=bar_width)

ax.grid(True)
# fig.autofmt_xdate()
# fig.tight_layout()

plt.show()
