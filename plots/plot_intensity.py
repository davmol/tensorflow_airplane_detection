import db_mac
import numpy as np
import pandas as pd
from matplotlib import pyplot

# series = read_csv('daily-minimum-temperatures.csv', header=0, index_col=0, parse_dates=True, squeeze=True)


timestamps = []
intensity = []



result = db_mac.execute("select * from brightness where timestamp > '2020-01-10' and timestamp < '2020-01-11'")

for row in result:
    timestamps.append(row[0])
    intensity.append(float(row[-1]))


print(timestamps)
print(intensity)
data = np.array(intensity)
series = pd.Series(data,index=timestamps)

series.plot()
pyplot.show()

"https://machinelearningmastery.com/time-series-data-visualization-with-python/"

"https://www.geeksforgeeks.org/python-pandas-series/"