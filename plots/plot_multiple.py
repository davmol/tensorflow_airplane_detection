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

fig, (axs1, axs2, axs3) = plt.subplots(2, 3, sharey=True, figsize=(10, 3))
# Remove horizontal space between axes
fig.subplots_adjust(wspace=10)
fig.subplots_adjust(hspace=10)

# humidity
hum = []
hum_t = []
sql = "select humidity, timestamp from od2 where timestamp >= '2020-01-07' and timestamp < '2020-01-010' and humidity is not null order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    hum.append(float(row[0]))
    hum_t.append(row[1])

axs1.plot(hum_t, hum)
axs1.set_ylim(min(hum), 102)
axs1.set_xlim(t_min_2020_01_07, t_max_2020_01_07)
axs1.spines['right'].set_visible(False)
axs1.spines['left'].set_visible(True)
axs1.yaxis.tick_left()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass plot, just so we don't keep repeating them
kwargs = dict(transform=axs1.transAxes, color='k', clip_on=False)
axs1.plot((1 - d, 1 + d), (-d, +d), **kwargs)
axs1.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

kwargs.update(transform=axs2.transAxes)  # switch to the bottom axes
axs2.plot((-d, +d), (1 - d, 1 + d), **kwargs)
axs2.plot((-d, +d), (-d, +d), **kwargs)

axs2.plot(hum_t, hum)
axs2.set_ylim(min(hum), 102)
axs2.set_xlim(t_min_2020_01_08, t_max_2020_01_08)
axs2.spines['right'].set_visible(False)
axs2.spines['left'].set_visible(False)
# axs2.tick_params(labelright='off')
axs2.yaxis.tick_right()

d = .015  # how big to make the diagonal lines in axes coordinates
# arguments to pass plot, just so we don't keep repeating them
kwargs = dict(transform=axs2.transAxes, color='k', clip_on=False)
axs2.plot((1 - d, 1 + d), (-d, +d), **kwargs)
axs2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)

kwargs.update(transform=axs3.transAxes)  # switch to the bottom axes
axs3.plot((-d, +d), (1 - d, 1 + d), **kwargs)
axs3.plot((-d, +d), (-d, +d), **kwargs)

axs3.plot(hum_t, hum)
axs3.set_ylim(min(hum), 102)
axs3.set_xlim(t_min_2020_01_09, t_max_2020_01_09)
axs3.spines['right'].set_visible(True)
axs3.spines['left'].set_visible(False)
# axs3.tick_params(labelright='off')
axs3.yaxis.tick_right()

#
# # clouds
# clouds = []
# clouds_t = []
# sql = "select cloud_coverage, timestamp from od2 where timestamp > '2020-01-07' and timestamp < '2020-01-09' and cloud_coverage is not null order by timestamp asc"
# result = db_mac.execute(sql)
# for row in result:
#     clouds.append(float(row[0]))
#     clouds_t.append(row[1])
#
# axs1[1].plot(clouds_t, clouds)
# axs2[1].plot(clouds_t, clouds)
#
#
# #axs[1].set_yticks(np.arange(min(clouds), max(clouds)),5)
# axs1[1].set_ylim(min(clouds), max(clouds))
# axs2[1].set_ylim(min(clouds), max(clouds))
#
# axs1[1].set_xlim(t_min_2020_01_07,t_max_2020_01_07)
# axs2[1].set_xlim(t_min_2020_01_08,t_max_2020_01_08)
#
#
#
# # hide the spines between ax and ax2
# axs1[1].spines['right'].set_visible(False)
# axs1[1].yaxis.tick_left()
# #axs1.tick_params(labelright='off')
#
# axs2[1].spines['left'].set_visible(False)
# axs2[1].tick_params(labelright='off')
# axs2[1].yaxis.tick_right()
#
#
# g = 1
# d = .015 # how big to make the diagonal lines in axes coordinates
# # arguments to pass plot, just so we don't keep repeating them
# kwargs = dict(transform=axs1[1].transAxes, color='k', clip_on=False)
# axs1[1].plot((g-d,g+d), (-d,+d), **kwargs)
# axs1[1].plot((g-d,g+d),(g-d,g+d), **kwargs)
#
# kwargs.update(transform=axs2[1].transAxes)  # switch to the bottom axes
# axs2[1].plot((-d,+d), (g-d,g+d), **kwargs)
# axs2[1].plot((-d,+d), (-d,+d), **kwargs)


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
