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

def score_activity(activity, temp_max, temp_min, humidity, precip, wind):
    # Each activity has 4 parameters — temp, humidity, precip, wind
    # Each parameter contributes 2.5 points max → 4 × 2.5 = 10 total
    # We use temp_max for worst-case heat, temp_min for worst-case cold

    score = 0
    precautions = []  # list of warning strings shown when score is 5-7
    
    if activity == "⚽ Sport":
        # Ideal: temp 15-28°C, humidity ≤70%, precip ≤1mm, wind ≤30kph

        # Temperature scoring
        if 15 <= temp_max <= 28:
            score += 2.5  # ideal range — full points
        elif 10 <= temp_max <= 32:
            score += 1.5  # borderline — partial points
            precautions.append("Temperature is outside ideal range (15–28°C). Stay hydrated.")
        else:
            precautions.append("Temperature is too extreme for sport.")

        # Humidity scoring
        if humidity <= 70:
            score += 2.5
        elif humidity <= 85:
            score += 1.0
            precautions.append("High humidity (>70%). Take frequent breaks.")
        else:
            precautions.append("Very high humidity. Risk of heat exhaustion.")

        # Precipitation scoring
        if precip == 0:
            score += 2.5
        elif precip <= 1:
            score += 1.5
            precautions.append("Light rain expected. Wear appropriate footwear.")
        else:
            precautions.append("Too much rain for outdoor sport.")

        # Wind scoring
        if wind <= 30:
            score += 2.5
        elif wind <= 45:
            score += 1.0
            precautions.append("Moderate wind expected. May affect performance.")
        else:
            precautions.append("Very strong wind. Outdoor sport not advisable.")

    elif activity == "🥾 Hiking":
        # Ideal: temp 10-25°C, humidity ≤80%, precip ≤5mm, wind ≤40kph

        if 10 <= temp_max <= 25:
            score += 2.5
        elif 5 <= temp_max <= 30:
            score += 1.5
            precautions.append("Temperature outside ideal hiking range (10–25°C).")
        else:
            precautions.append("Temperature too extreme for hiking.")

        if humidity <= 80:
            score += 2.5
        elif humidity <= 90:
            score += 1.0
            precautions.append("High humidity. Carry extra water.")
        else:
            precautions.append("Very high humidity. Risk of dehydration.")

        if precip <= 5:
            score += 2.5
        elif precip <= 10:
            score += 1.0
            precautions.append("Moderate rain expected. Waterproof gear recommended.")
        else:
            precautions.append("Heavy rain. Trail conditions may be dangerous.")

        if wind <= 40:
            score += 2.5
        elif wind <= 55:
            score += 1.0
            precautions.append("Strong wind on exposed trails. Stay cautious.")
        else:
            precautions.append("Dangerous wind speeds for hiking.")

    elif activity == "🏖️ Beach":
        # Ideal: temp 25-35°C, humidity ≤85%, precip 0mm, wind ≤20kph

        if 25 <= temp_max <= 35:
            score += 2.5
        elif 20 <= temp_max <= 38:
            score += 1.5
            precautions.append("Temperature outside ideal beach range (25–35°C).")
        else:
            precautions.append("Too cold or too hot for beach.")

        if humidity <= 85:
            score += 2.5
        elif humidity <= 92:
            score += 1.0
            precautions.append("High humidity. Stay in shade periodically.")
        else:
            precautions.append("Very high humidity. Not comfortable for beach.")

        if precip == 0:
            score += 2.5
        elif precip <= 2:
            score += 1.0
            precautions.append("Some rain possible. Check forecast before heading out.")
        else:
            precautions.append("Rain expected. Beach not advisable.")

        if wind <= 20:
            score += 2.5
        elif wind <= 35:
            score += 1.0
            precautions.append("Breezy conditions. Secure umbrellas and belongings.")
        else:
            precautions.append("Too windy for comfortable beach experience.")

    # Round to 1 decimal place — avoids ugly floats like 7.000000001
    return round(score, 1), precautions
