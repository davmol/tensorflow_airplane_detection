import matplotlib.pyplot as plt

"""legend 
'best'	0
'upper right'	1
'upper left'	2
'lower left'	3
'lower right'	4
'right'	5
'center left'	6
'center right'	7
'lower center'	8
'upper center'	9
'center'	10

"""
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
    "#DCE319FF",
    "#FDE725FF"
]

airlines = [

    "easyJet",
    "Lufthansa",
    "Eurowings",
    "NULL",
    "Swiss Air",
    "Ryanair",
    "Air France",
    "Austrian Airlines",
    "KLM Royal Dutch Airlines",
    "Turkish Airlines",
    "British Airways",

]

aircrafts = [

    "Airbus 320",
    "Airbus319",
    "Boeing 738",
    "Airbus 321",
    "NULL",
    "Airbus 220",
    "Airbus 320neu",
    "Airbus 321neu",
    "De Havilland DHC-8",
    "Airbus 318",
    "ATR-76"

]

counts2 = [
    595,
    477,
    178,
    125,
    102,
    55,
    52,
    23,
    18,
    15,
    13,

]

counts = [459,
          241,
          208,
          102,
          73,
          69,
          55,
          54,
          51,
          47,
          47]


def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return '{p:.1f}%'.format(p=pct)

    return my_autopct


# airlines

fig = plt.figure(figsize=(10, 5))
colors = [cmap[i] for i in range(0, len(counts))]
patches, texts, junk = plt.pie(counts, colors=colors, startangle=90, autopct=make_autopct(counts))

plt.legend(patches, airlines, loc=1)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.tight_layout()
plt.show()

# aircrafts

fig = plt.figure(figsize=(10, 5))
colors = [cmap[i] for i in range(0, len(counts2))]
patches, texts, junk = plt.pie(counts2, colors=colors, startangle=90, autopct=make_autopct(counts))

aircrafts = [i + " " + make_autopct(counts2) for i in aircrafts]
plt.legend(patches, aircrafts, loc=1)
# Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
plt.tight_layout()
plt.show()
