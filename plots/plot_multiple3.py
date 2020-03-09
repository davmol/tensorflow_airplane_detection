import datetime

import db_mac
import matplotlib.pyplot as plt
import numpy as np

# daytimes 2020-01-07


t_min_2020_01_07 = datetime.datetime.strptime('2020-01-07 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_07 = datetime.datetime.strptime('2020-01-07 17:00', '%Y-%m-%d %H:%M')
t_min_2020_01_08 = datetime.datetime.strptime('2020-01-08 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_08 = datetime.datetime.strptime('2020-01-08 17:00', '%Y-%m-%d %H:%M')
t_min_2020_01_09 = datetime.datetime.strptime('2020-01-09 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_09 = datetime.datetime.strptime('2020-01-09 17:00', '%Y-%m-%d %H:%M')

nine_hours_from_now = datetime.datetime.strptime('2020-01-09', '%Y-%m-%d') + datetime.timedelta(hours=6)

sql = """select date_trunc('hour', timestamp),  count(1) from od2 where bound like 'in' group by 1 order by 1"""
result = db_mac.execute(sql)
print(result)

data = np.array(list(db_mac.execute(sql))).T
flights_t = data[0, :]
flights_count_buckets = data[1, :]

# humidity
prec = []
prec_t = []
sql = "select precision, timestamp from od2 where  precision is not null order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    prec_list = row[0].replace("[", "").replace("]", "").split(",")
    print(prec_list)
    values = []
    for i in prec_list:
        values.append(float(i))
    if len(values) < 6:
        p = round(np.mean(values), 2) * len(values)
        prec.append(p)
        prec_t.append(row[1])


# humidity
hum = []
hum_t = []
sql = "select humidity, timestamp from od2 where  humidity is not null order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    hum.append(float(row[0]))
    hum_t.append(row[1])

# clouds
clouds = []
clouds_t = []
sql = "select cloud_coverage, timestamp from od2  where cloud_coverage is not null order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    clouds.append(float(row[0]))
    clouds_t.append(row[1])

# temp
# temps = []
# temps_t = []
# sql = "select temperature, timestamp from od2  where cloud_coverage is not null order by timestamp asc"
# result = db_mac.execute(sql)
# for row in result:
#    temps.append(float(row[0]))
#    temps_t.append(row[1])
#    temps.append(float(row[0]))


# weather_status
weather = ["Mist", "Rain", "Drizzle", "Clouds", "Clear"]
weather_status = []
weather_status_t = []
sql = "select weather_status, timestamp from od2 where weather_status is not null order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    if row[0] == "Clear":
        weather_status.append(5)
    if row[0] == "Clouds":
        weather_status.append(4)
    if row[0] == "Drizzle":
        weather_status.append(3)
    if row[0] == "Rain":
        weather_status.append(2)
    if row[0] == "Mist":
        weather_status.append(1)

    weather_status_t.append(row[1])

# Erkennungsrate
object = []
object_t = []
sql = "select object , timestamp from od2 where bound like 'in'  order by timestamp asc"
result = db_mac.execute(sql)
for row in result:

    if row[0] is not None:
        dets = len(row[0].split(","))
        print(dets)
        if dets < 6:
            object.append(dets)
            object_t.append(row[1])
        else:
            object.append(0)
            object_t.append(row[1])
    else:
        object.append(-1)
        object_t.append(row[1])



# luminance
brightness = []
brightness_t = []
sql = "select luminance , timestamp from brightness  order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    brightness.append(float(row[0]))
    brightness_t.append(row[1])

# intensity
intensity = []
intensity_t = []
sql = "select intensity , timestamp from brightness  order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    intensity.append(float(row[0]))
    intensity_t.append(row[1])

# virdis
cmap = [
    "#440154FF",
    "#481567FF",
    "#482677FF",
    "#453781FF",
    "#404788FF",
    "#39568CFF",
    "#33638DFF",
    "#2D708EFF",
    "#287D8EFF",
    "#238A8DFF",
    "#1F968BFF",
    "#20A387FF",
    "#29AF7FFF",
    "#3CBB75FF",
    "#55C667FF",
    "#73D055FF",
    "#95D840FF",
    "#B8DE29FF",
    "#DCE319FF",
    "#FDE725FF"
]

#colorbrew div 11
cmap = [

    "#a6cee3",
    "#1f78b4",
    "#b2df8a",
    "#33a02c",
    "#fb9a99",
    "#e31a1c",
    "#fdbf6f",
    "#ff7f00",
    "#cab2d6",
    "#67001f",
    "#053061"
]

data = [[flights_t, flights_count_buckets, "Häufigkeit", cmap[0]],
        # [temps_t, temps, "Temperatur", cmap[0]],
        [hum_t, hum, "rel. Luftfeuchtigkeit", cmap[2]],
        [clouds_t, clouds, "Wolkenbedeckung", cmap[4]],
        [brightness_t, brightness, "Luminanz", cmap[6]],
        [weather_status_t, weather_status, "Wetter", cmap[8]],
        [object_t, object, "Erkennungsrate", cmap[10]],
        [prec_t, prec, "Ähnlichkeitswahrscheinlichkeit", cmap[1]]]

bar_width = 0.002
bar_width2 = 0.01
line_width = 0.2
def subplots(data):
    # nine_hours_from_now = datetime.datetime.strptime('2020-01-09', '%Y-%m-%d') + datetime.timedelta(hours=6)
    dates = set()
    for d in intensity_t:
        dates.add(d.date())

    dates = (sorted(list(dates)))
    datetimes = [datetime.datetime.combine(d, datetime.datetime.min.time()) for d in dates]
    print(datetimes)

    fig, ax = plt.subplots(len(data), 8, figsize=(45, 15))
    # Remove horizontal space between axes
    fig.subplots_adjust(wspace=0.1)
    fig.subplots_adjust(hspace=0.1)
    plt.xlabel("Tagesstunden", x=.5)


    for num, values in enumerate(data):

        x = values[0]
        y = values[1]

        ylabel = values[2]
        color = values[3]
        print(ylabel)
        ax[num, 0].set(ylabel=ylabel)
        if ylabel == "Erkennungsrate":
            c = ["red" if i < 0 else "green" for i in y]
            ax[num, 0].axhline(0, linewidth=line_width, color='k')
            ax[num, 0].bar(x, y, width=bar_width, color=c)
        elif ylabel == "Häufigkeit":
            ax[num, 0].bar(x, y, width=bar_width2)

        else:
            ax[num, 0].plot(x, y, color)
        ax[num, 0].set_ylim(min(y), max(y))
        ax[num, 0].set_xlim(datetimes[0] + datetime.timedelta(hours=6), datetimes[0] + datetime.timedelta(hours=16))
        ax[num, 0].spines['right'].set_visible(False)
        ax[num, 0].spines['left'].set_visible(True)
        ax[num, 0].yaxis.tick_left()
        if ylabel == "Wetter":
            ax[num, 0].set_yticklabels(weather)


        d = .015  # how big to make the diagonal lines in axes coordinates
        # arguments to pass plot, just so we don't keep repeating them
        kwargs = dict(transform=ax[num, 0].transAxes, color='k', clip_on=False)
        ax[num, 0].plot((1 - d, 1 + d), (-d, +d), **kwargs)
        ax[num, 0].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
        kwargs.update(transform=ax[num, 1].transAxes)  # switch to the bottom axes
        ax[num, 1].plot((-d, +d), (1 - d, 1 + d), **kwargs)
        ax[num, 1].plot((-d, +d), (-d, +d), **kwargs)

        if ylabel == "Erkennungsrate":
            c = ["red" if i < 0 else "green" for i in y]
            ax[num, 1].axhline(0, linewidth=line_width, color='k')
            ax[num, 1].bar(x, y, width=bar_width, color=c)
        elif ylabel == "Häufigkeit":
            ax[num, 1].bar(x, y, width=bar_width2)

        else:
            ax[num, 1].plot(x, y, color)
        ax[num, 1].set_ylim(min(y), max(y))
        ax[num, 1].set_xlim(datetimes[1] + datetime.timedelta(hours=6), datetimes[1] + datetime.timedelta(hours=16))
        ax[num, 1].spines['right'].set_visible(False)
        ax[num, 1].spines['left'].set_visible(False)
        # ax[num,1].tick_params(labelright='off')
        # ax[num, 1].yaxis.tick_right()
        if ylabel == "Wetter":
            ax[num, 1].set_yticklabels(weather)

        d = .015  # how big to make the diagonal lines in axes coordinates
        # arguments to pass plot, just so we don't keep repeating them
        kwargs = dict(transform=ax[num, 1].transAxes, color='k', clip_on=False)
        ax[num, 1].plot((1 - d, 1 + d), (-d, +d), **kwargs)
        ax[num, 1].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
        kwargs.update(transform=ax[num, 2].transAxes)  # switch to the bottom axes
        ax[num, 2].plot((-d, +d), (1 - d, 1 + d), **kwargs)
        ax[num, 2].plot((-d, +d), (-d, +d), **kwargs)

        if ylabel == "Erkennungsrate":
            c = ["red" if i < 0 else "green" for i in y]
            ax[num, 2].axhline(0, linewidth=line_width, color='k')
            ax[num, 2].bar(x, y, width=bar_width, color=c)
        elif ylabel == "Häufigkeit":
            ax[num, 2].bar(x, y, width=bar_width2)

        else:
            ax[num, 2].plot(x, y, color)
        ax[num, 2].set_ylim(min(y), max(y))
        ax[num, 2].set_xlim(datetimes[2] + datetime.timedelta(hours=6), datetimes[2] + datetime.timedelta(hours=16))
        ax[num, 2].spines['right'].set_visible(False)
        ax[num, 2].spines['left'].set_visible(False)
        # ax[num,2].tick_params(labelright='off')
        # ax[num, 2].yaxis.tick_right()
        if ylabel == "Wetter":
            ax[num, 2].set_yticklabels(weather)

        d = .015  # how big to make the diagonal lines in axes coordinates
        # arguments to pass plot, just so we don't keep repeating them
        kwargs = dict(transform=ax[num, 2].transAxes, color='k', clip_on=False)
        ax[num, 2].plot((1 - d, 1 + d), (-d, +d), **kwargs)
        ax[num, 2].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
        kwargs.update(transform=ax[num, 3].transAxes)  # switch to the bottom axes
        ax[num, 3].plot((-d, +d), (1 - d, 1 + d), **kwargs)
        ax[num, 3].plot((-d, +d), (-d, +d), **kwargs)

        if ylabel == "Erkennungsrate":
            c = ["red" if i < 0 else "green" for i in y]
            ax[num, 3].axhline(0, linewidth=line_width, color='k')
            ax[num, 3].bar(x, y, width=bar_width, color=c)
        elif ylabel == "Häufigkeit":
            ax[num, 3].bar(x, y, width=bar_width2)

        else:
            ax[num, 3].plot(x, y, color)
        ax[num, 3].set_ylim(min(y), max(y))
        ax[num, 3].set_xlim(datetimes[3] + datetime.timedelta(hours=6), datetimes[3] + datetime.timedelta(hours=16))
        ax[num, 3].spines['right'].set_visible(False)
        ax[num, 3].spines['left'].set_visible(False)
        # ax[num,3].tick_params(labelright='off')
        # ax[num, 3].yaxis.tick_right()
        if ylabel == "Wetter":
            ax[num, 3].set_yticklabels(weather)

        d = .015  # how big to make the diagonal lines in axes coordinates
        # arguments to pass plot, just so we don't keep repeating them
        kwargs = dict(transform=ax[num, 3].transAxes, color='k', clip_on=False)
        ax[num, 3].plot((1 - d, 1 + d), (-d, +d), **kwargs)
        ax[num, 3].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
        kwargs.update(transform=ax[num, 4].transAxes)  # switch to the bottom axes
        ax[num, 4].plot((-d, +d), (1 - d, 1 + d), **kwargs)
        ax[num, 4].plot((-d, +d), (-d, +d), **kwargs)

        if ylabel == "Erkennungsrate":
            c = ["red" if i < 0 else "green" for i in y]
            ax[num, 4].axhline(0, linewidth=line_width, color='k')
            ax[num, 4].bar(x, y, width=bar_width, color=c)
        elif ylabel == "Häufigkeit":
            ax[num, 4].bar(x, y, width=bar_width2)

        else:
            ax[num, 4].plot(x, y, color)
        ax[num, 4].set_ylim(min(y), max(y))
        ax[num, 4].set_xlim(datetimes[4] + datetime.timedelta(hours=6), datetimes[4] + datetime.timedelta(hours=16))
        ax[num, 4].spines['right'].set_visible(False)
        ax[num, 4].spines['left'].set_visible(False)
        # ax[num,4].tick_params(labelright='off')
        # ax[num, 4].yaxis.tick_right()
        if ylabel == "Wetter":
            ax[num, 4].set_yticklabels(weather)

        d = .015  # how big to make the diagonal lines in axes coordinates
        # arguments to pass plot, just so we don't keep repeating them
        kwargs = dict(transform=ax[num, 4].transAxes, color='k', clip_on=False)
        ax[num, 4].plot((1 - d, 1 + d), (-d, +d), **kwargs)
        ax[num, 4].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
        kwargs.update(transform=ax[num, 5].transAxes)  # switch to the bottom axes
        ax[num, 5].plot((-d, +d), (1 - d, 1 + d), **kwargs)
        ax[num, 5].plot((-d, +d), (-d, +d), **kwargs)

        if ylabel == "Erkennungsrate":
            c = ["red" if i < 0 else "green" for i in y]
            ax[num, 5].axhline(0, linewidth=line_width, color='k')
            ax[num, 5].bar(x, y, width=bar_width, color=c)
        elif ylabel == "Häufigkeit":
            ax[num, 5].bar(x, y, width=bar_width2)

        else:
            ax[num, 5].plot(x, y, color)
        ax[num, 5].set_ylim(min(y), max(y))
        ax[num, 5].set_xlim(datetimes[5] + datetime.timedelta(hours=6), datetimes[5] + datetime.timedelta(hours=16))
        ax[num, 5].spines['right'].set_visible(False)
        ax[num, 5].spines['left'].set_visible(False)
        # ax[num,3].tick_params(labelright='off')
        # ax[num, 5].yaxis.tick_right()
        if ylabel == "Wetter":
            ax[num, 5].set_yticklabels(weather)

        d = .015  # how big to make the diagonal lines in axes coordinates
        # arguments to pass plot, just so we don't keep repeating them
        kwargs = dict(transform=ax[num, 5].transAxes, color='k', clip_on=False)
        ax[num, 5].plot((1 - d, 1 + d), (-d, +d), **kwargs)
        ax[num, 5].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)
        kwargs.update(transform=ax[num, 6].transAxes)  # switch to the bottom axes
        ax[num, 6].plot((-d, +d), (1 - d, 1 + d), **kwargs)
        ax[num, 6].plot((-d, +d), (-d, +d), **kwargs)

        if ylabel == "Erkennungsrate":
            c = ["red" if i < 0 else "green" for i in y]
            ax[num, 6].axhline(0, linewidth=line_width, color='k')
            ax[num, 6].bar(x, y, width=bar_width, color=c)
        elif ylabel == "Häufigkeit":
            ax[num, 6].bar(x, y, width=bar_width2)

        else:
            ax[num, 6].plot(x, y, color)
        ax[num, 6].set_ylim(min(y), max(y))
        ax[num, 6].set_xlim(datetimes[6] + datetime.timedelta(hours=6), datetimes[6] + datetime.timedelta(hours=16))
        ax[num, 6].spines['right'].set_visible(True)
        ax[num, 6].spines['left'].set_visible(False)
        # ax[num,6].tick_params(labelright='off')
        # ax[num, 6].yaxis.tick_right()
        if ylabel == "Wetter":
            ax[num, 6].set_yticklabels(weather)
    fig.autofmt_xdate()

    # plt.show()
    plt.savefig('multiplot_bar.png')
    # savefig('foo.png', bbox_inches='tight')


subplots(data)
