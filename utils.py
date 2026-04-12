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

def assess_agriculture(temp_max, temp_min, precip, humidity, wind):
    results = {}

    # PLANTING
    if 15 <= temp_max <= 30 and precip <= 5:
        results["Planting"] = ("good", f"✅ Good — temp {temp_max}°C, precip {precip}mm. Ideal for planting.")
    elif 10 <= temp_max <= 35 and precip <= 10:
        results["Planting"] = ("marginal", f"⚠️ Marginal — temp {temp_max}°C (ideal 15–30°C), precip {precip}mm. Soil may be wet.")
    else:
        results["Planting"] = ("poor", f"❌ Poor — temp {temp_max}°C, precip {precip}mm. Too extreme for planting.")

    # IRRIGATION
    if 10 <= temp_max <= 35 and precip <= 2:
        results["Irrigation"] = ("good", f"✅ Good — only {precip}mm rain expected. Irrigation beneficial today.")
    elif precip <= 5:
        results["Irrigation"] = ("marginal", f"⚠️ Marginal — {precip}mm rain expected. Irrigation may not be needed.")
    else:
        results["Irrigation"] = ("poor", f"❌ Poor — {precip}mm rain expected. Skip irrigation, field already wet.")

    # HARVESTING
    if 15 <= temp_max <= 35 and precip <= 1:
        results["Harvesting"] = ("good", f"✅ Good — temp {temp_max}°C, only {precip}mm rain. Dry conditions for harvest.")
    elif precip <= 5:
        results["Harvesting"] = ("marginal", f"⚠️ Marginal — {precip}mm rain possible. Harvest early morning to avoid wet crops.")
    else:
        results["Harvesting"] = ("poor", f"❌ Poor — {precip}mm rain expected. Wet conditions will damage harvested crops.")

    return results

@st.cache_data
def get_air_quality(lat, lon):
    # Separate Open-Meteo endpoint specifically for air quality data
    # Different base URL from weather API — air-quality-api instead of api
    url = "https://air-quality-api.open-meteo.com/v1/air-quality"
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "european_aqi",      # AQI on European scale 0-500
            "uv_index",          # UV index 0-11+
            "carbon_monoxide",   # CO in μg/m³
            "pm2_5",  # particulate matter — the real cause of Delhi's pollution problem
        ],
        "timezone": "auto"
    }
    response = requests.get(url, params=params)
    return response.json()

def interpret_aqi(aqi):
    # European AQI scale — different from US AQI but same concept
    # Returns category name, color class, and health message
    if aqi <= 20:
        return "Good", "good", "Air quality is excellent. No health concerns."
    elif aqi <= 40:
        return "Fair", "fair", "Air quality is acceptable. Sensitive individuals should consider limiting prolonged outdoor exposure."
    elif aqi <= 60:
        return "Moderate", "moderate", "Sensitive groups (children, elderly, respiratory conditions) should reduce outdoor activity."
    elif aqi <= 80:
        return "Poor", "poor", "Everyone should reduce prolonged outdoor exertion. Wear a mask if going outside."
    elif aqi <= 100:
        return "Very Poor", "verypoor", "Avoid outdoor activity. Keep windows closed. Wear N95 mask if going out."
    else:
        return "Hazardous", "hazardous", "Health emergency. Stay indoors. Seal windows and doors."

def interpret_uv(uv):
    # WHO UV index scale
    if uv <= 2:
        return "Low", "No protection needed."
    elif uv <= 5:
        return "Moderate", "Wear sunscreen SPF 30+. Seek shade during midday."
    elif uv <= 7:
        return "High", "Wear SPF 50+, hat, and UV-blocking sunglasses. Limit midday exposure."
    elif uv <= 10:
        return "Very High", "Minimise sun exposure 10am–4pm. Full protective clothing recommended."
    else:
        return "Extreme", "Avoid going outside during midday hours. Full protection mandatory."

def interpret_co(co):
    # CO in μg/m³ — WHO guideline is 4000 μg/m³ for 1hr exposure
    if co <= 1000:
        return "Safe", "CO levels are well within safe limits."
    elif co <= 4000:
        return "Acceptable", "CO levels are within WHO guidelines. Ventilate indoor spaces."
    elif co <= 10000:
        return "Elevated", "CO levels are elevated. Avoid prolonged outdoor exposure. Check indoor ventilation."
    else:
        return "Dangerous", "Dangerous CO levels. Stay indoors with windows closed. Seek medical advice if feeling unwell."
    
def interpret_pm25(pm):
    # WHO guideline: 15 μg/m³ daily average
    # India's national standard is 60 μg/m³ — still 4x WHO limit
    if pm <= 15:
        return "Safe", "good", "Within WHO safe limits. No health concern."
    elif pm <= 35:
        return "Moderate", "fair", "Slightly above WHO limit. Sensitive individuals should limit prolonged outdoor exposure."
    elif pm <= 55:
        return "Unhealthy", "moderate", "Above safe limits. Reduce outdoor activity, especially exercise."
    elif pm <= 150:
        return "Very Unhealthy", "poor", "Significantly elevated. Everyone should limit outdoor time. Wear N95 mask."
    elif pm <= 250:
        return "Hazardous", "verypoor", "Extremely high PM2.5. Stay indoors. Run air purifier if available."
    else:
        return "Severely Hazardous", "hazardous", "Emergency level PM2.5. Avoid all outdoor exposure completely."