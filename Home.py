import streamlit as st  #The entire UI framework — every button, card, chart lives here
import pandas as pd   #Shapes the API's JSON response into a table the chart can read
import plotly.express as px     #Draws the interactive hourly temperature chart
from utils import get_coordinates, get_weather, get_weather_condition
from styles import apply_styles

st.set_page_config(     #sets the browser tab title, icon, and makes the app use full screen width.
    page_title="WeatherWise",   
    page_icon="🌦️",
    layout="wide" 
)

apply_styles()

st.title("🌦️ WeatherWise")  
st.markdown("Your intelligent weather companion.")

st.markdown("### 📍 Select your location")

popular_cities = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata",
    "London", "New York", "Tokyo", "Paris", "Dubai",
    "Sydney", "Singapore"
]

# Check session_state for previously selected city
saved_city = st.session_state.get('city', None)

# Pre-select in dropdown if it's a known city
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
    saved_other = saved_city if saved_city not in popular_cities else ""
    city = st.text_input("Enter city name", value=saved_other)
    if city:
        st.session_state['city'] = city
else:
    city = city_option
    st.session_state['city'] = city

if city:
    with st.spinner("Fetching weather data..."):   # shows a loading animation while the API calls run; disappears when the block exits
        try:
            lat, lon = get_coordinates(city)
            if lat is None:   #this is your guard for when geopy finds nothing
                st.error("City not found. Please check the spelling and try again.")
            else:
                weather_data = get_weather(lat, lon)
                current = weather_data["current"] #unpacks just the current weather slice of the JSON 
                hourly = weather_data["hourly"]
               

                # Resolve the condition string once so we can use it in the HTML below
                condition = get_weather_condition(current['weather_code'])
                
                # Render the city name as a large centered hero heading using raw HTML
                # # f-string lets us inject the Python variable `city` directly into the HTML
                st.markdown(f"""
                <div class="city-hero">
                    <div class="city-hero-name">🌍 {city}</div>
                    <div class="city-hero-coords">{lat:.2f}° N &nbsp;·&nbsp; {lon:.2f}° E</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Render all 5 cards in one HTML block instead of using st.metric
                # # Why: st.metric truncates text — our custom HTML card does not
                # # The CSS class .card-value has word-break:break-word which handles long strings like "Partly Cloudy"
                
                st.markdown(f"""
<div class="cards-row">
    <div class="weather-card">
        <div class="card-icon">🌡️</div>
        <div class="card-label">Temperature</div>
        <div class="card-value">{current['temperature_2m']}°C</div>
    </div>
    <div class="weather-card">
        <div class="card-icon">💧</div>
        <div class="card-label">Humidity</div>
        <div class="card-value">{current['relative_humidity_2m']}%</div>
    </div>
    <div class="weather-card">
        <div class="card-icon">🌬️</div>
        <div class="card-label">Wind Speed</div>
        <div class="card-value">{current['wind_speed_10m']} km/h</div>
    </div>
    <div class="weather-card">
        <div class="card-icon">🌧️</div>
        <div class="card-label">Precipitation</div>
        <div class="card-value">{current['precipitation']} mm</div>
    </div>
    <div class="weather-card">
        <div class="card-icon">☁️</div>
        <div class="card-label">Condition</div>
        <div class="card-value">{condition}</div>
    </div>
</div>
<p style="
    text-align: center;
    font-size: 11px;
    color: rgba(255,255,255,0.25);
    margin-top: 4px;
    letter-spacing: 0.5px;
">
    Data sourced from Open-Meteo weather models · Minor variance from real-time sensors is normal
</p>
""", unsafe_allow_html=True)

                st.divider()
                st.subheader("🕐 Hourly Temperature Today")

                hourly_df = pd.DataFrame({   #takes the two lists from the API response (a list of time strings, a list of temperature floats) and pairs them into a proper table with named columns
                    "Time": pd.to_datetime(hourly["time"]),
                    "Temperature (°C)": hourly["temperature_2m"]
                })

                fig = px.line(   #creates an interactive line chart
                    hourly_df,
                    x="Time",
                    y="Temperature (°C)",
                    title="Today's Hourly Temperature",
                    markers=True
                )

                fig.update_layout(
                    xaxis_title="Hour",
                    yaxis_title="Temperature (°C)",
                    hovermode="x unified",
                    height=350,
                    paper_bgcolor='rgba(0,0,0,0)',          # chart outer background — transparent so page bg shows through
                    plot_bgcolor='rgba(255,255,255,0.04)',   # chart plot area — barely-visible tint
                    font=dict(color='rgba(255,255,255,0.7)'),# all chart text becomes white
                    xaxis=dict(gridcolor='rgba(255,255,255,0.08)'),  # subtle grid lines
                    yaxis=dict(gridcolor='rgba(255,255,255,0.08)'),
                )

                # Style the line and dots to match the blue palette
                fig.update_traces(
                    line=dict(color='#60a5fa', width=2.5),  # sky blue line
                    marker=dict(color='#93c5fd', size=6),   # lighter blue dots
                )

                st.plotly_chart(fig, width='stretch')  #makes the chart stretch to fill whatever column or page width it's in, instead of a fixed pixel size
        except Exception as e:
            st.error(f"Something went wrong: {e}")