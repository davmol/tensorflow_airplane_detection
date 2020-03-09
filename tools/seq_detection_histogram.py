import math
from collections import defaultdict

import db_mac
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)
from scipy import stats

series = []
sql = "select object , timestamp from od2 where bound = 'in' order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    if row[0] is None:
        series.append(-1)
    else:
        series.append(1)

sql = "select count(object)  from od2 where bound = 'in' and object is not null"
result = db_mac.execute(sql)
for row in result:
    count = row[0]




print(series)

trues = defaultdict(int)

seq = []
for i in series:

    if i > 0:
        seq.append(i)

    else:
        if len(seq) != 0:
            trues[len(seq)] += 1
        seq = []
if len(seq) != 0:
    trues[len(seq)] += 1


print(trues)

x = trues.keys()
y = trues.values()

print(sum(y))

# https://www.empirical-methods.hslu.ch/entscheidbaum/zusammenhaenge/logistische-regression/
# https://www.youtube.com/watch?v=zM4VZR0px8E


fig, ax = plt.subplots(figsize=(12, 7))
# Remove horizontal space between axes

ax.bar(x, y, )

ax.set(xlabel="Anzahl aufeinander folgender Erkennungen")
ax.set(ylabel="Anzahl")
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_major_locator(MultipleLocator(1))

ax.margins(0)

plt.style.use('seaborn-dark-palette')
# plt.show()
fig.tight_layout()
# plt.savefig('fps_tf_1.png')


plt.show()

#### poissont
ps = []
x = list(x)
for i, v in enumerate(y):
    fak = math.factorial(x[i])
    lmbdpow = v ** x[i]
    p = (lmbdpow / fak) * (math.e ** - v)
    ps.append(p)

fig, ax = plt.subplots(figsize=(12, 7))
# Remove horizontal space between axes

ax.bar(x, ps, )

ax.set(xlabel="Anzahl aufeinander folgender Erkennungen")
ax.set(ylabel="Anzahl")
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_major_locator(MultipleLocator(1))

# ax.margins(0)

plt.style.use('seaborn-dark-palette')
# plt.show()
fig.tight_layout()
# plt.savefig('fps_tf_1.png')

plt.show()

print(count)
mu = count / max(x)
print(max(list(x)))
x = range(0, max(list(x)))
prob = stats.poisson.pmf(x, mu) * 100
counts = stats.poisson.rvs(mu, size=100)
bins = range(0, max(counts) + 2)
plt.bar(x, prob)

plt.show()
