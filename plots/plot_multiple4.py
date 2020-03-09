import datetime

import matplotlib.pyplot as plt
import numpy as np

import db_mac

# daytimes 2020-01-07


t_min_2020_01_07 = datetime.datetime.strptime('2020-01-07 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_07 = datetime.datetime.strptime('2020-01-07 17:00', '%Y-%m-%d %H:%M')
t_min_2020_01_08 = datetime.datetime.strptime('2020-01-08 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_08 = datetime.datetime.strptime('2020-01-08 17:00', '%Y-%m-%d %H:%M')
t_min_2020_01_09 = datetime.datetime.strptime('2020-01-09 07:00', '%Y-%m-%d %H:%M')
t_max_2020_01_09 = datetime.datetime.strptime('2020-01-09 17:00', '%Y-%m-%d %H:%M')

nine_hours_from_now = datetime.datetime.strptime('2020-01-09', '%Y-%m-%d') + datetime.timedelta(hours=6)


#ERROR

sorted_errors = []
errors = []

error_t = []

sql = "select * from error_log where timestamp >= '2020-01-07' order by timestamp asc"
result = db_mac.execute(sql)
for row in result:

    errors.append(row)



for i, error in enumerate(errors):
    try:
        if datetime.datetime.timestamp(errors[i+1][1]) - datetime.datetime.timestamp(error[1]) > 60:
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
    error_t.append(t[1])

print("count2", count_2)



# weather_status
weather_lbl = set()
object_lbl = ["","Keine", "1", "2", "3", "4", "5"]
weather_status = []
weather_status_t = []
sql = "select weather_status_detail, timestamp from od2 where weather_status_detail is not null order by timestamp asc"
result = db_mac.execute(sql)


for e, row in enumerate(result):
    if row[0] == "mist":
        weather_lbl.add("mist")
        weather_status.append(12)
    if row[0] == "shower rain":
        weather_lbl.add("shower rain")
        weather_status.append(11)
    if row[0] == "light intensity shower rain":
        weather_lbl.add("light intensitiy shower rain")
        weather_status.append(10)
    if row[0] == "moderate rain":
        weather_lbl.add("moderate rain")
        weather_status.append(9)
    if row[0] == "light rain":
        weather_lbl.add("light rain")
        weather_status.append(8)
    if row[0] == "light intensity drizzle rain":
        weather_lbl.add("light intensity drizzle rain")
        weather_status.append(7)
    if row[0] == "light intensity drizzle":
        weather_lbl.add("light intensity drizzle")
        weather_status.append(6)
    if row[0] == "overcast clouds":
        weather_lbl.add("overcast clouds")
        weather_status.append(5)
    if row[0] == "broken clouds":
        weather_lbl.add("broken clouds")
        weather_status.append(4)
    if row[0] == "scattered clouds":
        weather_lbl.add("scattered clouds")
        weather_status.append(3)
    if row[0] == "few clouds":
        weather_lbl.add("few clouds")
        weather_status.append(2)
    if row[0] == "clear sky":
        weather_lbl.add("clear sky")
        weather_status.append(1)


    weather_status_t.append(row[1])

print(weather_status_t)
print(weather_status)
weather_lbl = list(weather_lbl)

#Anzahl
sql = """select date_trunc('hour', timestamp),  count(1) from od2 where bound like 'in' group by 1 order by 1"""
result = db_mac.execute(sql)


data = np.array(list(db_mac.execute(sql))).T
flights_t = [i + datetime.timedelta(hours=0.5) for i in data[0, :]]
flights_count_buckets = data[1, :]

# precision
prec = []
prec_t = []
sql = "select precision, timestamp from od2 where  precision is not null order by timestamp asc"
result = db_mac.execute(sql)
for row in result:
    prec_list = row[0].replace("[","").replace("]","").split(",")

    values = []
    for i in prec_list:

        values.append(float(i))
    if len(values) < 6:
        p = round(np.mean(values) * 100,2)
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



# Objekterkennungen
object = []
object_t = []
sql = "select object , timestamp from od2 where bound like 'in'  order by timestamp asc"
result = db_mac.execute(sql)
for row in result:

    if row[0] is not None:
        dets = len(row[0].split(","))

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
#https://htmlcolorcodes.com/

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

data = [[error_t, error_msg, "Fehlertypen", "#e74c3c"],
        [flights_t, flights_count_buckets, "Flugzeuge landend\n pro Stunde", cmap[2]],
        #[temps_t, temps, "Temperatur", cmap[0]],
        [hum_t, hum, "rel. Luftfeuchtigkeit\nin %", cmap[4]],
        [clouds_t, clouds, "Wolkenbedeckung\nin %", cmap[8]],
        [brightness_t, brightness, "Luminanz", cmap[12]],
        #[weather_status_t, weather_status, "Wetterstatus", cmap[16]],
        [object_t, object, "Objekterkennungen", cmap[0]],
        [prec_t, prec, "Ähnlichkeits-\nwahrscheinlichkeit in %", cmap[19]]]

bar_width = 0.004
bar_width2 = 0.04
line_width = 0.3
def subplots(data):
    # nine_hours_from_now = datetime.datetime.strptime('2020-01-09', '%Y-%m-%d') + datetime.timedelta(hours=6)
    dates = set()
    for d in intensity_t:
        dates.add(d.date())

    dates = (sorted(list(dates)))
    datetimes = [datetime.datetime.combine(d, datetime.datetime.min.time()) for d in dates]

    l = len(datetimes)
    for d in range(0, 2):
        fig, ax = plt.subplots(len(data), 4, figsize=(20, 12))
        # Remove horizontal space between axes
        fig.subplots_adjust(wspace=0.1)
        fig.subplots_adjust(hspace=0.1)


        for num, values in enumerate(data):

            x = values[0]
            y = values[1]

            ylabel = values[2]
            color = values[3]
            print(ylabel)
            ax[num, 0].set(ylabel=ylabel)

            if "landend" in ylabel:
                width = bar_width2
            else:
                width = bar_width


            if ylabel == "Objekterkennungen":
                c = ["#e74c3c" if i < 0 else "#229954" for i in y]
                ax[num, 0].axhline(0, linewidth=line_width, color='k')
                ax[num, 0].bar(x, y, width=width, color=c)
            elif "landend" in ylabel or "wahrscheinlichkeit" in ylabel:
                ax[num, 0].bar(x, y, width=width)

            elif ylabel == "Fehlertypen":
                ax[num, 0].scatter(x, y, 50, color="#e74c3c", alpha=0.5)

            else:
                ax[num, 0].plot(x, y, color)

            if ylabel != "Fehlertypen":
                ax[num, 0].set_ylim(min(y), max(y))
            else:
                ax[num, 0].set_ylim(0,4)
            ax[num, 0].set_xlim(datetimes[0 + d * 4] + datetime.timedelta(hours=6), datetimes[0 + d * 4] + datetime.timedelta(hours=16))
            ax[num, 0].spines['right'].set_visible(False)
            ax[num, 0].spines['left'].set_visible(True)
            ax[num, 0].yaxis.tick_left()
            if ylabel == "Wetterstatus":
                ax[num, 0].set_yticklabels(weather_lbl)
            if ylabel == "Objekterkennungen":
                ax[num, 0].set_yticklabels(object_lbl)


            if ylabel == "Objekterkennungen":
                c = ["#e74c3c" if i < 0 else "#229954" for i in y]
                ax[num, 1].axhline(0, linewidth=line_width, color='k')
                ax[num, 1].bar(x, y, width=width, color=c)
            elif "landend" in ylabel or "wahrscheinlichkeit" in ylabel:
                ax[num, 1].bar(x, y, width=width)
            elif ylabel == "Fehlertypen":
                ax[num, 1].scatter(x, y, 50, color="#e74c3c", alpha=0.5)

            else:
                ax[num, 1].plot(x, y, color)
            if ylabel != "Fehlertypen":
                ax[num, 1].set_ylim(min(y), max(y))
            else:
                ax[num, 1].set_ylim(0,4)
            ax[num, 1].set_xlim(datetimes[1 + d * 4] + datetime.timedelta(hours=6), datetimes[1 + d * 4] + datetime.timedelta(hours=16))
            ax[num, 1].spines['right'].set_visible(False)
            ax[num, 1].spines['left'].set_visible(False)
            # ax[num,1].tick_params(labelright='off')
            # ax[num, 1].yaxis.tick_right()
            if ylabel == "Wetterstatus":
                ax[num, 1].set_yticklabels(weather_lbl)
            if ylabel == "Objekterkennungen":
                ax[num, 1].set_yticklabels(object_lbl)


            if ylabel == "Objekterkennungen":
                c = ["#e74c3c" if i < 0 else "#229954" for i in y]
                ax[num, 2].axhline(0, linewidth=line_width, color='k')
                ax[num, 2].bar(x, y, width=width, color=c)
            elif "landend" in ylabel or "wahrscheinlichkeit" in ylabel:
                ax[num, 2].bar(x, y, width=width)
            elif ylabel == "Fehlertypen":
                ax[num, 2].scatter(x, y, 50, color="#e74c3c", alpha=0.5)

            else:
                ax[num, 2].plot(x, y, color)
            if ylabel != "Fehlertypen":
                ax[num, 2].set_ylim(min(y), max(y))
            else:
                ax[num, 2].set_ylim(0,4)
            ax[num, 2].set_xlim(datetimes[2+ d * 4] + datetime.timedelta(hours=6), datetimes[2 + d * 4] + datetime.timedelta(hours=16))
            ax[num, 2].spines['right'].set_visible(False)
            ax[num, 2].spines['left'].set_visible(False)
            # ax[num,2].tick_params(labelright='off')
            # ax[num, 2].yaxis.tick_right()
            if ylabel == "Wetterstatus":
                ax[num, 2].set_yticklabels(weather_lbl)
            if ylabel == "Objekterkennungen":
                ax[num, 2].set_yticklabels(object_lbl)



            if ylabel == "Objekterkennungen":
                c = ["#e74c3c" if i < 0 else "#229954" for i in y]
                ax[num, 3].axhline(0, linewidth=line_width, color='k')
                ax[num, 3].bar(x, y, width=width, color=c)
            elif "landend" in ylabel or "wahrscheinlichkeit" in ylabel:
                ax[num, 3].bar(x, y, width=width)
            elif ylabel == "Fehlertypen":
                ax[num, 3].scatter(x, y, 50, color="#e74c3c", alpha=0.5)

            else:
                ax[num, 3].plot(x, y, color)
            if ylabel != "Fehlertypen":
                ax[num, 3].set_ylim(min(y), max(y))
            else:
                ax[num, 3].set_ylim(0,4)
            ax[num, 3].set_xlim(datetimes[3 + d * 4] + datetime.timedelta(hours=6), datetimes[3 + d * 4] + datetime.timedelta(hours=16))
            ax[num, 3].spines['right'].set_visible(True)
            ax[num, 3].spines['left'].set_visible(False)
            # ax[num,3].tick_params(labelright='off')
            # ax[num, 5].yaxis.tick_right()
            if ylabel == "Wetterstatus":
                ax[num, 3].set_yticklabels(weather_lbl)
            if ylabel == "Objekterkennungen":
                ax[num, 3].set_yticklabels(object_lbl)


        fig.autofmt_xdate()
        plt.tight_layout()
        #plt.show()
        plt.savefig("multiplot_ " +str(d)+ " .png")



subplots(data)
