import csv

import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator)

mp03 = []
mp800x600 = []
mp1024x768 = []
mp1 = []
mp2 = []
mp3 = []
mp4 = []
mp5 = []
mp6 = []
mp7 = []
mp8 = []

means = []
cpu = []
with open('fps_mean_test2.csv', 'r', newline='') as csvfile:
    fieldnames = ['format', 'width', "height", "max_fps", "fps", "fps_mean", "cpu"]
    reader = csv.DictReader(csvfile, fieldnames=fieldnames)

    for i, row in enumerate(reader):
        if i > 0:
            means.append(str(round(float(row["fps_mean"]), 1)))
            cpu.append(str(round(float(row["cpu"]))))

        if row["format"] == "0.3":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp03.append(float(i))

        if row["format"] == "800x600":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp800x600.append(float(i))

        if row["format"] == "1024x768":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp1024x768.append(float(i))

        if row["format"] == "1":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp1.append(float(i))

        if row["format"] == "2":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp2.append(float(i))

        if row["format"] == "3":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp3.append(float(i))

        if row["format"] == "4":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp4.append(float(i))

        if row["format"] == "5":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp5.append(float(i))

        if row["format"] == "6":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp6.append(float(i))

        if row["format"] == "7":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp7.append(float(i))

        if row["format"] == "8":
            fps = row["fps"].replace("[", "").replace("]", "").split(",")
            for i in fps:
                mp8.append(float(i))

# print("0.3",mp03)
# print("mp800x600",mp800x600)
# print("mp1024x768",mp1024x768)
# print("mp1",mp1)
# print("mp2",mp2)
# print("mp3", mp3)
# print("mp4",mp4)
# print("mp5", mp5)
# print("mp6",mp6)
# print("mp7", mp7)
# print("mp8",mp8)

frames = [i for i in range(1, len(mp03) + 1)]
# print(frames)

print(means)
print(cpu)
virdis = [
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

diverging = [

    "#67001f",
    "#b2182b",
    "#d6604d",
    "#f4a582",
    "#fddbc7",
    "#f7f7f7",
    "#d1e5f0",
    "#92c5de",
    "#4393c3",
    "#2166ac",
    "#053061"
]

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

fig, ax = plt.subplots(figsize=(10, 4))  # inch

ax.plot(frames, mp03, cmap[0], label="640x480p - " + means[0] + " - " + cpu[0] + "%")
ax.plot(frames, mp800x600, cmap[1], label="800x600p - " + means[1] + " - " + cpu[1] + "%")
ax.plot(frames, mp1024x768, cmap[2], label="1024x768p - " + means[2] + " - " + cpu[2] + "%")
ax.plot(frames, mp1, cmap[3], label="1 MP - " + means[3] + " - " + cpu[3] + "%")
ax.plot(frames, mp2, cmap[4], label="2 MP - " + means[4] + " - " + cpu[4] + "%")
ax.plot(frames, mp3, cmap[5], label="3 MP - " + means[5] + " - " + cpu[5] + "%")
ax.plot(frames, mp4, cmap[6], label="4 MP - " + means[6] + " - " + cpu[6] + "%")
ax.plot(frames, mp5, cmap[7], label="5 MP - " + means[7] + " - " + cpu[7] + "%")
ax.plot(frames, mp6, cmap[8], label="6 MP - " + means[8] + " - " + cpu[8] + "%")
ax.plot(frames, mp7, cmap[9], label="7 MP - " + means[9] + " - " + cpu[9] + "%")
ax.plot(frames, mp8, cmap[10], label="8 MP - " + means[10] + " - " + cpu[10] + "%")

ax.set(ylabel="FPS")
ax.set(xlabel="Bilder")
ax.yaxis.set_major_locator(MultipleLocator(10))
ax.xaxis.set_major_locator(MultipleLocator(10))

ax.margins(0)
plt.legend(loc="upper right")
plt.style.use('seaborn-dark-palette')
# plt.show()
fig.tight_layout()
plt.savefig('fps.png')
