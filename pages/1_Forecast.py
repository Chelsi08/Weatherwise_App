import streamlit as st
import pandas as pd
import plotly.express as px

# Import shared functions from utils — get_coordinates already handles geocoding
# get_16day_forecast is the new function we just added
from utils import get_coordinates, get_weather, get_weather_condition, save_default_city, load_default_city


# Page config — must be first Streamlit call
st.set_page_config(
    page_title="16-Day Forecast | WeatherWise",
    page_icon="📅",
    layout="wide"
)

# Same CSS as Home page — keeps dark theme consistent across all pages
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&display=swap');

.stApp {
    background: linear-gradient(160deg, #0a0f1e 0%, #0d1b3e 50%, #0a0f1e 100%);
    font-family: 'Outfit', sans-serif;
}
header[data-testid="stHeader"] { background: transparent; }
.block-container {
    padding-top: 2rem;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    max-width: 100% !important;
}
h1 { color: #ffffff !important; }
h3 { color: rgba(255,255,255,0.85) !important; }
label { color: rgba(255,255,255,0.6) !important; }

/* Forecast cards scroll horizontally on small screens */
.forecast-row {
    display: flex;
    gap: 12px;
    margin: 24px 0;
    flex-wrap: wrap;
}

/* Each day card — slightly taller than home cards to fit more data */
.forecast-card {
    flex: 1;
    min-width: 140px;
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(96,165,250,0.2);
    border-radius: 20px;
    padding: 20px 12px;
    text-align: center;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.forecast-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 8px 32px rgba(96,165,250,0.25);
}

/* Day label at top of card e.g. "Mon 31 Mar" */
.forecast-date {
    font-size: 11px;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-bottom: 8px;
}

.forecast-icon { font-size: 26px; margin-bottom: 8px; }

/* Max temp — bright white, prominent */
.forecast-temp-max {
    font-size: 22px;
    font-weight: 700;
    color: #ffffff;
}

/* Min temp — muted, smaller */
.forecast-temp-min {
    font-size: 14px;
    color: rgba(255,255,255,0.45);
    margin-bottom: 10px;
}

/* Small data rows for wind/humidity/precip */
.forecast-detail {
    font-size: 11px;
    color: rgba(255,255,255,0.5);
    margin: 3px 0;
}

/* Highlighted value within detail row */
.forecast-detail span {
    color: #93c5fd;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.title("📅 16-Day Forecast")

# Smart city logic:
# Check if user already selected a city on the Home page via session_state
# session_state persists across pages during the same browser session
if 'city' in st.session_state and st.session_state['city']:
    # City already chosen on Home — use it directly, no selector needed
    city = st.session_state['city']
    st.markdown(f"### 🌍 Forecast for **{city}**")
else:
    # No city in session yet — show the selector same as Home page
    st.markdown("### 📍 Select a City")


popular_cities = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata",
    "London", "New York", "Tokyo", "Paris", "Dubai",
    "Sydney", "Singapore"
]

# Load from disk first — persists even after browser closes
# Falls back to session_state if nothing saved on disk yet
default_city = load_default_city() or st.session_state.get('city', None)

# Pre-select in dropdown if it's a known city
if default_city in popular_cities:
    default_index = popular_cities.index(default_city)
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
    saved_other = default_city if default_city not in popular_cities else ""
    city = st.text_input("Enter city name", value=saved_other)
    if city:
        st.session_state['city'] = city
        save_default_city(city)  # persist to disk
else:
    city = city_option
    st.session_state['city'] = city
    save_default_city(city)  # persist to disk