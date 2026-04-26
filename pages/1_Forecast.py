import streamlit as st
import pandas as pd
from utils import get_coordinates, get_16day_forecast, get_weather_condition
from styles import apply_styles

st.set_page_config(
    page_title="16-Day Forecast | WeatherWise",
    page_icon="📅",
    layout="wide"
)

apply_styles()

st.title("📅 16-Day Forecast")

popular_cities = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata",
    "London", "New York", "Tokyo", "Paris", "Dubai",
    "Sydney", "Singapore"
]

saved_city = st.session_state.get('city', None)

if saved_city:
    city = saved_city
    st.markdown(f"### 🌍 Forecast for **{city}**")
else:
    st.markdown("### 📍 Select a City")

    if saved_city in popular_cities:
        default_index = popular_cities.index(saved_city)
    else:
        default_index = None

    city_option = st.selectbox(
        "Choose a city",
        options=popular_cities + ["Other (type below)"],
        index=default_index,
        placeholder="Select a city..."
    )

    if city_option is None:
        city = None
    elif city_option == "Other (type below)":
        city = st.text_input("Enter city name")
        if city:
            st.session_state['city'] = city
    else:
        city = city_option
        st.session_state['city'] = city

if city:
    with st.spinner("Fetching 16-day forecast..."):
        try:
            lat, lon = get_coordinates(city)
            if lat is None:
                st.error("City not found. Please check the spelling and try again.")
            else:
                forecast_data = get_16day_forecast(lat, lon)
                daily = forecast_data["daily"]

                cards_html = '<div class="forecast-row">'

                for i in range(len(daily["time"])):
                    date      = pd.to_datetime(daily["time"][i]).strftime("%a %d %b")
                    condition = get_weather_condition(daily["weather_code"][i])
                    temp_max  = daily["temperature_2m_max"][i]
                    temp_min  = daily["temperature_2m_min"][i]
                    precip    = daily["precipitation_sum"][i]
                    wind      = daily["wind_speed_10m_max"][i]
                    humidity  = daily["relative_humidity_2m_max"][i]

                    cards_html += (
                        f'<div class="forecast-card">'
                        f'<div class="forecast-date">{date}</div>'
                        f'<div class="forecast-icon">{condition.split()[0]}</div>'
                        f'<div class="forecast-temp-max">{temp_max}°C</div>'
                        f'<div class="forecast-temp-min">{temp_min}°C</div>'
                        f'<div class="forecast-detail">💧 <span>{humidity}%</span></div>'
                        f'<div class="forecast-detail">🌬️ <span>{wind} km/h</span></div>'
                        f'<div class="forecast-detail">🌧️ <span>{precip} mm</span></div>'
                        f'</div>'
                    )

                cards_html += '</div>'
                st.markdown(cards_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong: {e}")