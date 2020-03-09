#!/usr/bin/python
# -*- coding: utf-8 -*-

import psycopg2
from psycopg2.extensions import AsIs
import configparser
import datetime

config = configparser.ConfigParser()
config.read('creds.conf')

connection = psycopg2.connect(user=config["db_config"]["user"],
                              password=config["db_config"]["password"],
                              host=config["db_config"]["host"],
                              port=config["db_config"]["port"],
                              database=config["db_config"]["dbname"])

cursor = connection.cursor()




def execute(command):
    try:
        if type(command) == str:
            cursor.execute(command)
            result = cursor.fetchall()
            return result
        elif type(command) == tuple:
            cursor.execute(command[0], command[1])
            connection.commit()
    except Exception as e:
        print(e)


def insert(table, dict):

    columns = dict.keys()
    values = [dict[column] for column in columns]
    print(columns)
    print(values)
    insert_statement = """insert into {} (%s) values %s""".format(table)

    cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
    connection.commit()


if __name__ == "__main__":




    flightinfo = {'airline': 'easyJet', 'icao': 'EJU', 'callsign': 'EJU21RF', 'flightnumber': 'U25734', 'aircraft': 'A319', 'origin': 'HEL', 'destination': 'TXL', 'hex': '44039e', 'squawk': '7670', 'speed': 68.421052, 'lat': 52.562597, 'lon': 13.316607, 'track': 262, 'validposition': 1, 'validtrack': 1, 'messages': 869, 'seen': 0, 'altitude': 198, 'vert_rate': -768, 'timestamp': datetime.datetime(2019, 12, 12, 22, 15, 23, 264741), 'buffer': 'TXL', 'bound': 'in', 'object': None, 'precision': None, 'img_url': None, 'weather_status': 'Clouds', 'weather_status_detail': 'broken clouds', 'icon': 'http://openweathermap.org/img/wn/04n@2x.png', 'temperature': 1.57, 'pressure': 999, 'humidity': 93, 'visibility': 10000, 'wind_speed': 4.1, 'wind_direction': 150, 'cloud_coverage': 65, 'detection_time': datetime.datetime(2019, 12, 12, 22, 16, 1), 'sunrise_time': datetime.datetime(2019, 12, 12, 8, 8, 7), 'sunset_time': datetime.datetime(2019, 12, 12, 8, 8, 7), 'location_name': 'Berlin Reinickendorf'}

    cursor.execute("Select * FROM od LIMIT 0")
    colnames = [desc[0] for desc in cursor.description]
    #print(colnames)
    colnames = ['hex', 'squawk', 'flightnumber', 'aircraft', 'validposition', 'altitude', 'vert_rate', 'track', 'validtrack', 'speed', 'messages', 'seen', 'timestamp', 'precision', 'img_url', 'bound', 'object', 'callsign', 'origin', 'destination', 'airline', 'weather_status', 'weather_status_detail', 'temperature', 'pressure', 'humidity', 'visibility', 'wind_speed', 'wind_direction', 'cloud_coverage', 'detection_time', 'sunrise_time', 'sunset_time', 'location_name', 'geom']

    makepoint = "ST_TRANSFORM(ST_setSRID(ST_MakePoint(%s, %s),4326),32633)"
    flightinfo.update({"geom": ""})

    db_dict = {}

    vals = []
    for name in colnames:
        if name == "geom":
            pass
        else:
            vals.append(flightinfo[name])

    vals_str_list = ["%s"] * len(vals)
    vals_str = ", ".join(vals_str_list)
    vals_str = vals_str + ", " + makepoint
    vals.append(flightinfo["lon"])
    vals.append((flightinfo["lat"]))
    cols = ', '.join(colnames)
    sql = """INSERT INTO public.od ({cols}) VALUES ({vals_str})""".format(
        cols=cols, vals_str=vals_str)

    print(vals)
    print(sql)
    cursor.execute(sql, vals)
    connection.commit()

