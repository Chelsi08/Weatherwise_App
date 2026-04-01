# utils.py — shared functions used across all pages
# Import once here, then every page just does: from utils import get_coordinates, get_weather, get_weather_condition

import requests
from geopy.geocoders import Nominatim
import streamlit as st
import json
import os

#st.cache_data-This decorator tells Streamlit: "if the input is the same as last time, return the stored result, don't call the API again." 
#Faster app, fewer API hits.
@st.cache_data
def get_coordinates(city_name):
    # Converts a city name to lat/lon using OpenStreetMap's geocoder
    geolocator = Nominatim(user_agent="weatherwise_app")  #geopy requires you to name your app;
    location = geolocator.geocode(city_name)   
    if location:
        return location.latitude, location.longitude
    return None, None

@st.cache_data
def get_weather(lat, lon):
    # Fetches current weather + today's hourly temps from Open-Meteo
    url = "https://api.open-meteo.com/v1/forecast"
    params = {              #this dictionary becomes the URL query string
        "latitude": lat,
        "longitude": lon,
        "current": [        #tells Open-Meteo which real-time values to return right now
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "weather_code",
            "apparent_temperature"       # Open-Meteo calculates this from temp + humidity + wind combined
        ],
        "hourly": "temperature_2m",   #requests hourly temps
        "timezone": "auto",   #Open-Meteo detects timezone from the lat/lon
        "forecast_days": 1    #we only want today's hourly data on this page
    }
    response = requests.get(url, params=params)    #requests api call to get params from url 
    return response.json()   #response comes in json format

def get_weather_condition(code):
    # Translates Open-Meteo's WMO weather code into a human-readable string
    if code == 0:
        return "☀️ Clear Sky"
    elif code in [1, 2, 3]:
        return "🌤️ Partly Cloudy"
    elif code in [45, 48]:
        return "🌫️ Foggy"
    elif code in [51, 53, 55, 61, 63, 65]:
        return "🌧️ Rainy"
    elif code in [71, 73, 75]:
        return "❄️ Snowy"
    elif code in [80, 81, 82]:
        return "🌦️ Showers"
    elif code in [95, 96, 99]:
        return "⛈️ Thunderstorm"
    else:
        return "🌡️ Unknown"


@st.cache_data
def get_16day_forecast(lat, lon):
    # Separate API call from get_weather() — different params, different data shape
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "temperature_2m_max",       # highest temp of the day
            "temperature_2m_min",       # lowest temp of the day
            "precipitation_sum",        # total rain/snow for the day in mm
            "wind_speed_10m_max",       # peak wind speed of the day
            "relative_humidity_2m_max", # peak humidity of the day
            "weather_code"              # WMO code representing dominant condition
        ],
        "timezone": "auto",   # local time based on coordinates
        "forecast_days": 16   # maximum Open-Meteo allows on free tier
    }
    response = requests.get(url, params=params)
    return response.json()