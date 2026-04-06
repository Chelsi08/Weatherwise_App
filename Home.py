import streamlit as st  #The entire UI framework — every button, card, chart lives here
import pandas as pd   #Shapes the API's JSON response into a table the chart can read
import plotly.express as px     #Draws the interactive hourly temperature chart
from utils import get_coordinates, get_weather, get_weather_condition


st.set_page_config(     #sets the browser tab title, icon, and makes the app use full screen width.
    page_title="WeatherWise",   
    page_icon="🌦️",
    layout="wide" 
)

# Inject custom CSS into the Streamlit page using a raw HTML style block.
# unsafe_allow_html=True is required — without it Streamlit strips the HTML.
# This is the standard way to style Streamlit beyond its built-in theme.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

/* Full page background — deep navy to midnight blue gradient */
.stApp {
    background: linear-gradient(160deg, #0a0f1e 0%, #0d1b3e 50%, #0a0f1e 100%);
    font-family: 'Outfit', sans-serif;
}

/* Hide the default Streamlit header bar */
header[data-testid="stHeader"] {
    background: transparent;
}

/* Hide the top padding Streamlit adds by default */
.block-container {
    padding-top: 2rem;
}

/* Make the main title white */
h1 { color: #ffffff !important; }

/* Make subheadings white */
h3 { color: rgba(255,255,255,0.85) !important; }

/* Style the dropdown label and widget to match the dark theme */
label { color: rgba(255,255,255,0.6) !important; }

/* Cards row — horizontal flex container */
.cards-row {
    display: flex;
    gap: 16px;
    margin: 28px 0;
    flex-wrap: wrap;
}

/* Individual card — glass panel with blue glow on hover */
.weather-card {
    flex: 1;
    min-width: 130px;
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(96, 165, 250, 0.2);
    border-radius: 20px;
    padding: 26px 16px;
    text-align: center;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

/* On hover: lift up + add a blue glow ring */
.weather-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 32px rgba(96, 165, 250, 0.25);
}

.card-icon { font-size: 30px; margin-bottom: 12px; }

.card-label {
    font-size: 10px;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 10px;
}

/* Large value — word-break prevents truncation on long strings like "Partly Cloudy" */
.card-value {
    font-size: 20px;
    font-weight: 700;
    color: #e0f0ff;
    word-break: break-word;
    line-height: 1.35;
}

/* City hero section — large centered heading */
.city-hero {
    text-align: center;
    padding: 30px 0 6px 0;
}

.city-hero-name {
    font-size: 46px;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -1px;
    text-shadow: 0 0 40px rgba(96,165,250,0.4);
}

.city-hero-coords {
    font-size: 13px;
    color: rgba(255,255,255,0.35);
    margin-top: 6px;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

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