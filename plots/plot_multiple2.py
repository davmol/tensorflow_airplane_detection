import datetime

import db_mac
import matplotlib.pyplot as plt

# daytimes 2020-01-07


t_min_2020_01_07 = datetime.datetime.strptime('2020-01-07 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_07 = datetime.datetime.strptime('2020-01-07 17:00', '%Y-%m-%d %H:%M')
t_min_2020_01_08 = datetime.datetime.strptime('2020-01-08 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_08 = datetime.datetime.strptime('2020-01-08 17:00', '%Y-%m-%d %H:%M')
t_min_2020_01_09 = datetime.datetime.strptime('2020-01-09 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_09 = datetime.datetime.strptime('2020-01-09 17:00', '%Y-%m-%d %H:%M')

sunrises = []
sunsets = []

print(sunrises, sunsets)

fig, ax = plt.subplots(3, 3, figsize=(15, 6))
# Remove horizontal space between axes
fig.subplots_adjust(wspace=0)
fig.subplots_adjust(hspace=0)

# humidity
hum = []
hum_t = []
sql = "select humidity, timestamp from od2 where timestamp >= '2020-01-07' and timestamp < '2020-01-10' and humidity is not null order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    hum.append(float(row[0]))
    hum_t.append(row[1])

ax[0, 0].set(ylabel='humidity')
ax[0, 0].plot(hum_t, hum)
ax[0, 0].set_ylim(min(hum), 102)
ax[0, 0].set_xlim(t_min_2020_01_07, t_max_2020_01_07)
ax[0, 0].spines['right'].set_visible(False)
ax[0, 0].spines['left'].set_visible(True)
ax[0, 0].yaxis.tick_left()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass plot, just so we don't keep repeating them
kwargs = dict(transform=ax[0, 0].transAxes, color='k', clip_on=False)
ax[0, 0].plot((1 - d, 1 + d), (-d, +d), **kwargs)
ax[0, 0].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

kwargs.update(transform=ax[0, 1].transAxes)  # switch to the bottom axes
ax[0, 1].plot((-d, +d), (1 - d, 1 + d), **kwargs)
ax[0, 1].plot((-d, +d), (-d, +d), **kwargs)

ax[0, 1].plot(hum_t, hum)
ax[0, 1].set_ylim(min(hum), 102)
ax[0, 1].set_xlim(t_min_2020_01_08, t_max_2020_01_08)
ax[0, 1].spines['right'].set_visible(False)
ax[0, 1].spines['left'].set_visible(False)
# ax[0,1].tick_params(labelright='off')
ax[0, 1].yaxis.tick_right()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass plot, just so we don't keep repeating them
kwargs = dict(transform=ax[0, 1].transAxes, color='k', clip_on=False)
ax[0, 1].plot((1 - d, 1 + d), (-d, +d), **kwargs)
ax[0, 1].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

kwargs.update(transform=ax[0, 2].transAxes)  # switch to the bottom axes
ax[0, 2].plot((-d, +d), (1 - d, 1 + d), **kwargs)
ax[0, 2].plot((-d, +d), (-d, +d), **kwargs)

ax[0, 2].plot(hum_t, hum)
ax[0, 2].set_ylim(min(hum), 102)
ax[0, 2].set_xlim(t_min_2020_01_09, t_max_2020_01_09)
ax[0, 2].spines['right'].set_visible(True)
ax[0, 2].spines['left'].set_visible(False)
# ax[0,2].tick_params(labelright='off')
ax[0, 2].yaxis.tick_right()

ax[0, 0].set(ylabel='humidity')

# clouds
clouds = []
clouds_t = []
sql = "select cloud_coverage, timestamp from od2 where timestamp > '2020-01-07' and timestamp < '2020-01-10' and cloud_coverage is not null order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    clouds.append(float(row[0]))
    clouds_t.append(row[1])
ax[1, 0].set(ylabel='cloud coverage')
ax[1, 0].plot(clouds_t, clouds)
ax[1, 0].set_ylim(min(clouds), 102)
ax[1, 0].set_xlim(t_min_2020_01_07, t_max_2020_01_07)
ax[1, 0].spines['right'].set_visible(False)
ax[1, 0].spines['left'].set_visible(True)
ax[1, 0].yaxis.tick_left()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass plot, just so we don't keep repeating them
kwargs = dict(transform=ax[1, 0].transAxes, color='k', clip_on=False)
ax[1, 0].plot((1 - d, 1 + d), (-d, +d), **kwargs)
ax[1, 0].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

kwargs.update(transform=ax[1, 1].transAxes)  # switch to the bottom axes
ax[1, 1].plot((-d, +d), (1 - d, 1 + d), **kwargs)
ax[1, 1].plot((-d, +d), (-d, +d), **kwargs)

ax[1, 1].plot(clouds_t, clouds)
ax[1, 1].set_ylim(min(clouds), 102)
ax[1, 1].set_xlim(t_min_2020_01_08, t_max_2020_01_08)
ax[1, 1].spines['right'].set_visible(False)
ax[1, 1].spines['left'].set_visible(False)
# ax[1,1].tick_params(labelright='off')
ax[1, 1].yaxis.tick_right()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass plot, just so we don't keep repeating them
kwargs = dict(transform=ax[1, 1].transAxes, color='k', clip_on=False)
ax[1, 1].plot((1 - d, 1 + d), (-d, +d), **kwargs)
ax[1, 1].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

kwargs.update(transform=ax[1, 2].transAxes)  # switch to the bottom axes
ax[1, 2].plot((-d, +d), (1 - d, 1 + d), **kwargs)
ax[1, 2].plot((-d, +d), (-d, +d), **kwargs)

ax[1, 2].plot(clouds_t, clouds)
ax[1, 2].set_ylim(min(clouds), 102)
ax[1, 2].set_xlim(t_min_2020_01_09, t_max_2020_01_09)
ax[1, 2].spines['right'].set_visible(True)
ax[1, 2].spines['left'].set_visible(False)
# ax[1,2].tick_params(labelright='off')
ax[1, 2].yaxis.tick_right()

# temp
temps = []
temps_t = []
sql = "select temperature, timestamp from od2 where timestamp > '2020-01-07' and timestamp < '2020-01-10' and cloud_coverage is not null order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    temps.append(float(row[0]))
    temps_t.append(row[1])
ax[2, 0].set(ylabel='temperature')
ax[2, 0].plot(temps_t, temps)
ax[2, 0].set_ylim(min(temps), max(temps))
ax[2, 0].set_xlim(t_min_2020_01_07, t_max_2020_01_07)
ax[2, 0].spines['right'].set_visible(False)
ax[2, 0].spines['left'].set_visible(True)
ax[2, 0].yaxis.tick_left()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass plot, just so we don't keep repeating them
kwargs = dict(transform=ax[2, 0].transAxes, color='k', clip_on=False)
ax[2, 0].plot((1 - d, 1 + d), (-d, +d), **kwargs)
ax[2, 0].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

kwargs.update(transform=ax[2, 1].transAxes)  # switch to the bottom axes
ax[2, 1].plot((-d, +d), (1 - d, 1 + d), **kwargs)
ax[2, 1].plot((-d, +d), (-d, +d), **kwargs)

ax[2, 1].plot(temps_t, temps)
ax[2, 1].set_ylim(min(temps), max(temps))
ax[2, 1].set_xlim(t_min_2020_01_08, t_max_2020_01_08)
ax[2, 1].spines['right'].set_visible(False)
ax[2, 1].spines['left'].set_visible(False)
# ax[2,1].tick_params(labelright='off')
ax[2, 1].yaxis.tick_right()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass plot, just so we don't keep repeating them
kwargs = dict(transform=ax[2, 1].transAxes, color='k', clip_on=False)
ax[2, 1].plot((1 - d, 1 + d), (-d, +d), **kwargs)
ax[2, 1].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

kwargs.update(transform=ax[2, 2].transAxes)  # switch to the bottom axes
ax[2, 2].plot((-d, +d), (1 - d, 1 + d), **kwargs)
ax[2, 2].plot((-d, +d), (-d, +d), **kwargs)

ax[2, 2].plot(temps_t, temps)
ax[2, 2].set_ylim(min(temps), max(temps))
ax[2, 2].set_xlim(t_min_2020_01_09, t_max_2020_01_09)
ax[2, 2].spines['right'].set_visible(True)
ax[2, 2].spines['left'].set_visible(False)
# ax[2,2].tick_params(labelright='off')
ax[2, 2].yaxis.tick_right()


def subplots(num, x, y, ylabel):
    ax[num, 0].set(ylabel=ylabel)
    ax[num, 0].plot(x, y)
    ax[num, 0].set_ylim(min(y), max(y))
    ax[num, 0].set_xlim(t_min_2020_01_07, t_max_2020_01_07)
    ax[num, 0].spines['right'].set_visible(False)
    ax[num, 0].spines['left'].set_visible(True)
    ax[num, 0].yaxis.tick_left()

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax[num, 0].transAxes, color='k', clip_on=False)
    ax[num, 0].plot((1 - d, 1 + d), (-d, +d), **kwargs)
    ax[num, 0].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

    kwargs.update(transform=ax[num, 1].transAxes)  # switch to the bottom axes
    ax[num, 1].plot((-d, +d), (1 - d, 1 + d), **kwargs)
    ax[num, 1].plot((-d, +d), (-d, +d), **kwargs)

    ax[num, 1].plot(x, y)
    ax[num, 1].set_ylim(min(y), max(y))
    ax[num, 1].set_xlim(t_min_2020_01_08, t_max_2020_01_08)
    ax[num, 1].spines['right'].set_visible(False)
    ax[num, 1].spines['left'].set_visible(False)
    # ax[num,1].tick_params(labelright='off')
    ax[num, 1].yaxis.tick_right()

    d = .015  # how big to make the diagonal lines in axes coordinates
    # arguments to pass plot, just so we don't keep repeating them
    kwargs = dict(transform=ax[num, 1].transAxes, color='k', clip_on=False)
    ax[num, 1].plot((1 - d, 1 + d), (-d, +d), **kwargs)
    ax[num, 1].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

    kwargs.update(transform=ax[num, 2].transAxes)  # switch to the bottom axes
    ax[num, 2].plot((-d, +d), (1 - d, 1 + d), **kwargs)
    ax[num, 2].plot((-d, +d), (-d, +d), **kwargs)

    ax[num, 2].plot(x, y)
    ax[num, 2].set_ylim(min(y), max(y))
    ax[num, 2].set_xlim(t_min_2020_01_09, t_max_2020_01_09)
    ax[num, 2].spines['right'].set_visible(True)
    ax[num, 2].spines['left'].set_visible(False)
    # ax[num,2].tick_params(labelright='off')
    ax[num, 2].yaxis.tick_right()


# hide the spines between ax and ax2
# axs1.spines['right'].set_visible(False)
# axs2.spines['left'].set_visible(False)
# axs1.yaxis.tick_left()
# axs1.tick_params(labelright='off')
# axs2.yaxis.tick_right()


#
#
# # clouds
# clouds = []
# clouds_t = []
# sql = "select cloud_coverage, timestamp from od2 where timestamp > '2020-01-07' and timestamp < '2020-01-08' and object is not null  and cloud_coverage is not null order by timestamp asc"
# result = db_mac.execute(sql)
# for row in result:
#     clouds.append(float(row[0]))
#     clouds_t.append(row[1])
#
# axs1[1].plot(clouds_t, clouds)
# #axs[1].set_yticks(np.arange(min(clouds), max(clouds)),5)
# axs1[1].set_ylim(min(clouds), max(clouds))
# axs1[0].set_xlim(sunrises[0],sunsets[0])
# axs2[0].set_xlim(sunrises[1],sunsets[1])
#
#
# # temp
# temp = []
# temp_t = []
# sql = "select temperature, timestamp from od2 where timestamp > '2020-01-07' and timestamp < '2020-01-08' and object is not null  and temperature is not null order by timestamp asc"
# result = db_mac.execute(sql)
# for row in result:
#     temp.append(float(row[0]))
#     temp_t.append(row[1])
#
# axs1[2].plot(temp_t, temp)
# #axs[2].set_yticks(np.arange(min(temp), max(temp)),1)
# axs1[2].set_ylim(min(temp), max(temp))
# axs1[0].set_xlim(sunrises[0],sunsets[0])
# axs2[0].set_xlim(sunrises[1],sunsets[1])
#


# axs.grid(True)
fig.autofmt_xdate()
# fig.tight_layout()


plt.show()
