#!/usr/bin/python
# -*- coding: utf-8 -*-

#owm
#https://readthedocs.org/projects/pyowm/downloads/pdf/stable/
#


#API
#https://openweathermap.org/price
#https://openweathermap.org/current
#icons
#https://openweathermap.org/weather-conditions

import datetime

# import requests
import requests


def get_weather(lat, lon, api_key):
    try:

        url = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}".format(lat, lon, api_key)
        response = requests.get(url)
        data = response.json()
        print(data)
        #TODO Timestamp mit Zeitzone!!
        weather = {
            "weather_status": data["weather"][0]["main"],
            "weather_status_detail": data["weather"][0]["description"],
            "icon": "http://openweathermap.org/img/wn/" + data["weather"][0]["icon"] + "@2x.png",
            "temperature": data["main"]["temp"],
            "pressure": data["main"]["pressure"],
            "humidity": data["main"]["humidity"],
            "visibility": data["visibility"],
            "wind_speed": data["wind"]["speed"],
            "wind_direction": data["wind"]["deg"],
            "cloud_coverage": data["clouds"]["all"],
            "detection_time": datetime.datetime.fromtimestamp(data["dt"]),
            "sunrise_time": datetime.datetime.fromtimestamp(data["sys"]["sunrise"]),
            "sunset_time": datetime.datetime.fromtimestamp(data["sys"]["sunrise"]),
            "location_name": data["name"]

        }

        return weather

    except:

         weather = {
            "weather_status": None,
            "weather_status_detail": None,
            "icon": None,
            "temperature": None,
            "pressure": None,
            "humidity": None,
            "visibility": None,
            "wind_speed": None,
            "wind_direction": None,
            "cloud_coverage": None,
            "detection_time": None,
            "sunrise_time": None,
            "sunset_time": None,
            "location_name": None
         }

         return weather



if __name__ == "__main__":
    api_key = "f7fe74adbba155937d732e486250f7d9"
    weather = get_weather(52.560969, 13.310329, api_key)
    print(weather)
