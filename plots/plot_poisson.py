import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

obs = [19,
       12,
       11,
       7,
       2,
       4,
       1,
       0,
       2,
       2,
       2,
       0,
       1,
       0,
       1,
       0,
       1,
       1,
       1,
       1,
       1,
       1,
       0,
       1,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       0,
       1]
pois = [

    1.229885872,
    3.587167126,
    6.97504719,
    10.17194382,
    11.86726779,
    11.53762146,
    9.614684551,
    7.010707485,
    4.543977073,
    2.650653293,
    1.405649473,
    0.683301827,
    0.306609794,
    0.127754081,
    0.049682143,
    0.018113281,
    0.006215342,
    0.002014231,
    0.000618404,
    0.000180368,
    5.01022E-05,
    1.32847E-05,
    3.3693E-06,
    8.18927E-07,
    1.91083E-07,
    4.28712E-08,
    9.2623E-09,
    1.92965E-09,
    3.88147E-10,
    7.5473E-11,
    1.42019E-11,
    2.58889E-12,
    4.57632E-13,
    7.85153E-14,
    1.30859E-14,
    2.1204E-15,
    3.34297E-16,
    5.13175E-17,
    7.6757E-18,
    1.11937E-18,
    1.5926E-19,
    2.21195E-20,
    3.00071E-21,
    3.97821E-22,
    5.15694E-23,
    6.53959E-24
]

fig, ax = plt.subplots(figsize=(8, 4))

x1 = [i + 0.25 for i in range(1, 47)]
x2 = [i - 0.25 for i in range(1, 47)]

p1 = plt.bar(x1, obs, color='#febf84', width=0.4)
p2 = plt.bar(x2, pois, color='#651a80', width=0.4)

ax.set(ylabel="Häufigkeit")
ax.set(xlabel="Streuweite")
ax.yaxis.set_major_locator(MultipleLocator(1))
ax.xaxis.set_major_locator(MultipleLocator(2))
ax.margins(0)
ax.legend((p1[0], p2[0]), ('Beobachtete Häufigkeit', 'Poisson Häufigkeit von \u03bb=5.83 '), loc=1)

plt.show()

fig.tight_layout()
fig.savefig('poisson.png')

