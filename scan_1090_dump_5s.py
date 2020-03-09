#!/usr/bin/python
# -*- coding: utf-8 -*-

from urllib.request import urlopen
import json
import psycopg2

import datetime
import pytz
import flightradar24
import time

import os

global day
global flights_list

url = "http://0.0.0.0:8080/data.json"

connection = psycopg2.connect(user="XXX",
                              password="XXX",
                              host="XXX",
                              port="XXX",
                              database="dump1090")

cursor = connection.cursor()
fr = flightradar24.Api()



def get_aircraft_type(flight_number):
    #print(flight_number)

    if flight_number not in flights_list.keys():
        airline = flight_number[0:3]
        flights = fr.get_flights(airline)
        for key, flight in flights.items():
            if type(flight) == list:
                if flight_number in flight:

                    aircraft_type = flight[8]

                    flights_list[flight_number] = aircraft_type

                    return aircraft_type
    else:

        return flights_list[flight_number]


def db_parser(ident):

    try:
        json_url = urlopen(url)
        data = json.loads(json_url.read())

        for flight in data:

            if flight["validposition"] != 0:

                os.system('cls' if os.name == 'nt' else 'clear')
                #print("airborne: ", flights_list)
                server_timezone = pytz.timezone("Europe/Amsterdam")
                server_time = datetime.datetime.now(server_timezone)
                print(server_time)


                sql = '''INSERT INTO public.dump (id, hex, squawk, flight, a_type, validposition, altitude, vert_rate, track, validtrack, speed, messages, seen, geom, timestamp) 
                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s, ST_TRANSFORM(ST_setSRID(ST_MakePoint(%s, %s),4326), 32633), %s)'''
                flight_number = flight["flight"].replace(" ", "")

                values = \
                    (ident,
                     flight["hex"],
                     flight["squawk"],
                     flight_number,
                     get_aircraft_type(flight_number),
                     flight["validposition"],
                     flight["altitude"],
                     flight["vert_rate"],
                     flight["track"],
                     flight["validtrack"],
                     flight["speed"],
                     flight["messages"],
                     flight["seen"],
                     flight["lon"],
                     flight["lat"],
                     server_time,

                     )

                cursor.execute(sql, values)

                connection.commit()


    except (Exception, psycopg2.Error) as error:
        print("Error", error)


def run():
    global day
    ident = 0
    while True:
        ident += 1
        db_parser(ident)
        time.sleep(5)



while True:
    run()
    


