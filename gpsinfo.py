import serial
import pynmea2
from collections import defaultdict
import numpy as np
port = "/dev/ttyACM0"


#$GPGGA,105040.00,5232.74928,N,01321.29342,E,1,05,11.25,84.3,M,42.2,M,,*5C
#Timestamp: 10:50:40 -- Lat: 5232.74928 N -- Lon: 01321.29342 E -- Altitude: 84.3 M -- Satellites: 05


def get_gps():
    gps = defaultdict(list)
    i = 1
    serialPort = serial.Serial(port, baudrate = 9600, timeout = 0.5)
    print("warm up GPS")
    while True:
        try:

            str = serialPort.readline()
            str = str.decode("utf-8")
            if str.find('GGA') > 0:

                msg = pynmea2.parse(str)
                print(i, msg)

                values = str.split(",")
                gps_time_utc = float(values[1])
                y = values[2].replace(".", "")
                x = values[4].replace(".", "")

                altitude = float(values[9])
                satellites = int(msg.num_sats)

                deg_lat = float(y[0:2])
                min_lat = float(y[2:]) / 10E4
                deg_lon = float(x[1:3])
                min_lon = float(x[3:]) / 10E4

                lat = round(deg_lat + min_lat / 60, 5)
                lon = round(deg_lon + min_lon / 60, 5)

                if i > 5:

                    gps["lat"].append(lat)
                    gps["lon"].append(lon)
                    gps["satellites"].append(satellites)
                    gps["altitude"].append(altitude)

                if i == 15:
                    gps = {"lat": round(np.mean(gps["lat"]),6), "lon": round(np.mean(gps["lon"]),6), "altitude": round(np.mean(gps["altitude"]),1),
                           "satellite": round(np.mean(gps["satellites"]),1)}
                    print(gps)
                    return gps

                i += 1


        except:
            print("no gpsinfo")
            return {"lat": None, "lon": None, "satellites": None, "altitude": None}
            pass

if __name__ == "__main__":
    get_gps()
