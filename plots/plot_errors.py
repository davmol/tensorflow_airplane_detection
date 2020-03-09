from datetime import datetime

import db_mac
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

sorted_errors = []
errors = []
sql = "select * from error_log where timestamp >= '2020-01-07' order by timestamp asc"
result = db_mac.execute(sql)
for row in result:

    errors.append(row)
print(errors[0])


for i, error in enumerate(errors):
    try:
        if datetime.timestamp(errors[i + 1][1]) - datetime.timestamp(error[1]) > 60:
            sorted_errors.append(error)
    except:
        pass


print(sorted_errors)


print(len(errors), len(sorted_errors))

count_2 = 0
error_msg = []
timestamps = []
for t in sorted_errors:
    if "frame_expanded" in t[0]:
        error_msg.append(1)
    elif "20th" in t[0]:
        error_msg.append(2)
        count_2 += 1
    elif "ret == False" in t[0]:
        error_msg.append(3)
    elif "frame is None" in t[0]:
        error_msg.append(4)
    else:
        error_msg.append(0)
    timestamps.append(t[1])

print("count2", count_2)


#r'$\Delta_i$'

fig, ax = plt.subplots(figsize=(10, 4))
ax.scatter(timestamps, error_msg, 65, alpha=0.5, color="#e74c3c")
ax.set_xlabel("Beobachtungszeitraum")
ax.set_ylabel("Fehlertyp")
ax.set_title('Fehlertypen Übersicht')

ax.set_ylim(1, 4)
ax.set_xlim((min(timestamps), max(timestamps)))
ax.yaxis.set_major_locator(MultipleLocator(1))

ax.xaxis.set_major_locator(MultipleLocator(0.5))
ax.grid(True)
fig.autofmt_xdate()
fig.tight_layout()

# plt.show()
plt.savefig("errors.png")

#
# with open('errors.csv', 'w', newline='') as csvfile:
#     fieldnames = ['timestamp', 'error_type']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     writer.writeheader()
#     for i in range(0,len(error_msg)):
#         writer.writerow({'timestamp': timestamps[i].strftime('%x %X'), 'error_type': error_msg[i]})
#
