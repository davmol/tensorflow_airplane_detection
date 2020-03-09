#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Objekterkennung Skript


import configparser
import datetime
import math
import os
import time
import traceback
from collections import defaultdict

import flightradar24
import pytz
import requests

import db
import gpsinfo
import mail
import openweather

# Variables
# ------------------------------------------------------------------------------------------------------------------------------------

config = configparser.ConfigParser()
config.read('creds.conf')


url = config['paths']['url']
img_dir = config['paths']['img_dir']
weather_api_key = config['weather']['api_key']
_350deg_interesect_x = int(config['location']['x'])
_350deg_interesect_y = int(config['location']['y'])


hex_list = []
inbound = defaultdict(lambda: [])
outbound = defaultdict(lambda: [])
day = datetime.datetime.today().day
detected_flights = defaultdict(list)


fr = flightradar24.Api()
gps = gpsinfo.get_gps()

# Functions
# ------------------------------------------------------------------------------------------------------------------------------------




def meter_to_feet(meter):
    feet = int(round(meter / 0.3048))
    return feet

def feet_to_meter(feet):
    meter = int(round(feet * 0.3048))
    return meter

def ktph_to_mps(ktph):
    msps = ktph * 0.514444
    return msps

def insert_table_error_log(error):
    server_timezone = pytz.timezone("Europe/Amsterdam")
    timestamp = datetime.datetime.now(server_timezone)


    sql = '''INSERT INTO public.error_log (error_msg, timestamp) VALUES (%s, %s);'''
    vals = (error, timestamp)

    db.execute((sql, vals))


def insert_table_od(flightinfo):
    colnames = ['hex', 'squawk', 'flightnumber', 'aircraft', 'validposition', 'altitude', 'vert_rate', 'track',
                'validtrack', 'speed', 'messages', 'seen', 'timestamp', 'precision', 'img_url', 'bound', 'object',
                'callsign', 'origin', 'destination', 'airline', 'weather_status', 'weather_status_detail',
                'temperature', 'pressure', 'humidity', 'visibility', 'wind_speed', 'wind_direction', 'cloud_coverage',
                'detection_time', 'sunrise_time', 'sunset_time', 'location_name', "framerate_avg", "det_dist_surf", "det_eta", "geom"]

    makepoint = "ST_TRANSFORM(ST_setSRID(ST_MakePoint(%s, %s),4326),32633)"
    flightinfo.update({"geom": ""})


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
    sql = """INSERT INTO public.od3 ({cols}) VALUES ({vals_str})""".format(
        cols=cols, vals_str=vals_str)


    db.execute((sql, vals))


def buffer(lat, lon, name):


    sql = "SELECT name, ST_WITHIN(ST_Transform(ST_SetSRID(ST_MakePoint({},{}),4326), 32633), geom) from public.bufferzone where name = '{}';".format(lon, lat, name)
    result = db.execute(sql)

    if result[0][1] == True:

        return (result[0][0], result[0][1])
    else:

        return ("", False)

def trigger(lat, lon, speed, altitude, bound):
    #print("trigger bound", bound)
    # TODO geopandas?
    # Todo richtige Distanzen
    sql = "SELECT ST_X( ST_Transform(ST_SetSRID(ST_MakePoint({},{}),4326), 32633)), ST_Y( ST_Transform(ST_SetSRID(ST_MakePoint({},{}),4326), 32633)) ".format(
        lon, lat, lon, lat)
    result = db.execute(sql)

    x = result[0][0]
    y = result[0][1]

    __x_cent = 382983
    __y_cent = 5824610


    dist_surf = round(math.sqrt(math.pow(_350deg_interesect_x - x, 2) + math.pow(_350deg_interesect_y - y, 2)))
    dist_hypo = round(math.sqrt(math.pow(dist_surf,2) + math.pow(altitude,2)))
    print("dists", dist_surf, dist_hypo)
    if bound == "in":
        det_eta = round(dist_surf / speed)
        #t2 = timer.trigger(dist_hypo)

    trig = {"det_eta": det_eta, "det_dist_surf": dist_surf}
    return trig

def scan():
    response = requests.get(url)
    data = response.json()
    server_timezone = pytz.timezone("Europe/Amsterdam")
    server_time = datetime.datetime.now(server_timezone)

    for flight in data:
        callsign = flight["flight"].replace(" ", "")
        if len(callsign) > 2:
            if flight["validposition"] != 0:
                if flight["seen"] <= 5:
                    speed = round(ktph_to_mps(ktph=flight["speed"]))
                    if speed >= 28: # 100 km/h
                        altitude = feet_to_meter(flight["altitude"])
                        if altitude <= 300:
                            if flight["hex"] not in hex_list:

                            #if 2 > len(inbound[callsign]) and 2 > len(outbound[callsign]):

                                buffer_result = buffer(lat=flight["lat"], lon=flight["lon"], name="TXL")
                                buffer_name = str(buffer_result[0])
                                geo_buffer = buffer_result[1]

                                if geo_buffer:

                                    info = {"hex": flight["hex"], "squawk": flight["squawk"], "speed": speed,
                                            "lat": flight["lat"], "lon": flight["lon"], "track": flight["track"], "validposition": flight["validposition"], "validtrack": flight["validtrack"],
                                            "messages": flight["messages"], "seen": flight["seen"],
                                            "altitude": altitude, "vert_rate": flight["vert_rate"],
                                            "timestamp": server_time,"buffer": buffer_name}

                                    if flight["vert_rate"] > 0: #START

                                        #if buffer_name not in outbound[callsign]:
                                        print("")
                                        print(server_time.strftime("%d.%m.%Y %H:%M:%S"))
                                        print("---> out: " + callsign)
                                        outbound[callsign].append(buffer_name)
                                        img_name = "out_" + server_time.strftime("%Y_%m_%d-%H_%M_%S") + ".png"

                                        flightinfo = get_flight_info(callsign=callsign)

                                        flightinfo.update(info)
                                        flightinfo.update({"bound": "out"})


                                        if flight["track"] >= 70 and flight["track"] <= 90:

                                            detection = {"object": None, "precision": None, "img_url": None,
                                                         "framerate_avg": None}

                                        else:
                                            detection = {"object": None, "precision": None, "img_url": None,
                                             "framerate_avg": None}
                                            trig = {"det_eta": None, "det_dist_surf": None}


                                        trig = {"det_eta": None, "det_dist_surf": None}

                                        flightinfo.update(trig)
                                        flightinfo.update(detection)
                                        flightinfo.update(info)
                                        weather = openweather.get_weather(lat=gps["lat"],lon=gps["lon"], api_key=weather_api_key)
                                        flightinfo.update(weather)
                                        print("flightinfo", flightinfo)
                                        if len(outbound[callsign]) < 2:
                                            insert_table_od(flightinfo=flightinfo)

                                        hex_list.append(flight["hex"])


                                    elif flight["vert_rate"] <= 0:  # LANDING

                                        #if buffer_name not in inbound[callsign]:
                                        print(server_time.strftime("%d.%m.%Y %H:%M:%S"))
                                        print("---> in: " + callsign)
                                        inbound[callsign].append(buffer_name)
                                        img_name = "in_" + server_time.strftime("%Y_%m_%d-%H_%M_%S") + ".png"

                                        flightinfo = get_flight_info(callsign=callsign)
                                        flightinfo.update(info)
                                        flightinfo.update({"bound": "in"})

                                        if flight["track"] >= 250 and flight["track"] <= 270:
                                            landing_dir_260 = time.time()



                                            trig = trigger(lat=flight["lat"], lon=flight["lon"], speed=speed, altitude=altitude,  bound=flightinfo["bound"])
                                            print("det_eta", trig["det_eta"])

                                            wait = trig["det_eta"] + 20

                                            detection = od3.detect(runtime=wait, wait=wait, img_dir=img_dir, img_name=img_name)

                                        else:
                                            #landing_dir_80 = time.time()
                                            detection = {"object": None, "precision": None, "img_url": None}
                                            trig = {"det_eta": None, "det_dist_surf": None}


                                        flightinfo.update(trig)
                                        flightinfo.update(detection)

                                        flightinfo.update(info)
                                        weather = openweather.get_weather(lat=gps["lat"], lon=gps["lon"], api_key=weather_api_key)
                                        flightinfo.update(weather)
                                        print("flightinfo", flightinfo)
                                        if len(inbound[callsign]) < 2:
                                            insert_table_od(flightinfo)

                                        hex_list.append(flight["hex"])

                                        # global count_80
                                        # global count_260
                                        # count_80 = 0
                                        # count_260 = 0
                                        #
                                        # if landing_dir_260 > landing_dir_80:
                                        #     if count_260 == 0:
                                        #         mail.send("landing 260°", "")
                                        #         count_260 += 1
                                        #         count_80 = 0
                                        # else:
                                        #     if count_80 == 0:
                                        #         mail.send("landing 80°", "")
                                        #         count_80 += 1
                                        #         count_260 = 0







def get_flight_info(callsign):

    if callsign not in detected_flights.values():


        icao = callsign[0:3]

        if icao == "EZY":  # easyjet hack
            icao = "EJU"

        try:
            db_response = db.execute("SELECT name from airlines where active = 'Y' and icao = '{}';".format(icao))
            airline = db_response[0][0]

        except:
            airline = "None"

        if icao == "EJU": #easyjet hack
            icao = "EZY"

        try:
            flights = fr.get_flights(icao)

            for key, flight in flights.items():

                if type(flight) == list:
                    if callsign in flight:

                        detected_flights[airline].append(callsign)

                        aircraft = flight[8]
                        if icao == "EZY":  # easyjet hack
                            icao = "EJU"
                        origin = flight[11]
                        destination = flight[12]
                        flight_number = flight[13]

                        flightinfo = { "airline": airline, "icao": icao, "callsign": callsign, "flightnumber": flight_number, "aircraft": aircraft, "origin": origin, "destination": destination}
                        return flightinfo


            flightinfo = {"airline": None, "icao": icao, "callsign": callsign, "flightnumber": None,
                          "aircraft": None, "origin": None, "destination": None}
            return flightinfo

        except:
            flightinfo = {"airline": None, "icao": icao, "callsign": callsign, "flightnumber": None, "aircraft": None, "origin": None, "destination": None}


            return flightinfo




if __name__ == "__main__":
    try:
        mail.send("start", "")
    except:
        pass

    try:
        while True:
            scan()
            time.sleep(3)
    except:

        error = traceback.format_exc()
        print(error)
        if "KeyboardInterrupt" not in error and "During handling of the above exception, another exception occurred:" not in error:
            insert_table_error_log(error)
            mail.send("error", error)
            os.system('sudo shutdown -r now')

