import streamlit as st
import pandas as pd
from utils import get_coordinates, get_16day_forecast, get_weather_condition

st.set_page_config(
    page_title="16-Day Forecast | WeatherWise",
    page_icon="📅",
    layout="wide"
)

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

.forecast-row {
    display: ;
    grid-template-columns: repeat(8, 1fr);
    gap: 10px;
    margin: 24px 0;
    
}
@media (max-width: 900px) {
    .forecast-row {
        grid-template-columns: repeat(4, 1fr);
    }
}
.forecast-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03));
    border: 1px solid rgba(96,165,250,0.2);
    border-radius: 16px;
    padding: 12px 8px;
    text-align: center;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.forecast-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(96,165,250,0.25);
}

.forecast-date {
    font-size: 9px;
    color: rgba(255,255,255,0.45);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
}

.forecast-icon { font-size: 26px; margin-bottom: 8px; }

.forecast-temp-max {
    font-size: 16px;
    font-weight: 700;
    color: #ffffff;
}

.forecast-temp-min {
    font-size: 11px;
    color: rgba(255,255,255,0.45);
    margin-bottom: 4px;
}

.forecast-detail {
    font-size: 9px;
    color: rgba(255,255,255,0.5);
    margin: 2px 0;
}

.forecast-detail span {
    color: #93c5fd;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

st.title("📅 16-Day Forecast")

popular_cities = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata",
    "London", "New York", "Tokyo", "Paris", "Dubai",
    "Sydney", "Singapore"
]

# Read city from session_state if already selected on Home
saved_city = st.session_state.get('city', None)

if saved_city:
    # City exists — show it as heading, no selector needed
    city = saved_city
    st.markdown(f"### 🌍 Forecast for **{city}**")
else:
    # No city yet — show selector
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
                    # Convert "2024-03-30" to "Sat 30 Mar"
                    date = pd.to_datetime(daily["time"][i]).strftime("%a %d %b")
                    condition = get_weather_condition(daily["weather_code"][i])
                    temp_max = daily["temperature_2m_max"][i]
                    temp_min = daily["temperature_2m_min"][i]
                    precip   = daily["precipitation_sum"][i]
                    wind     = daily["wind_speed_10m_max"][i]
                    humidity = daily["relative_humidity_2m_max"][i]

                    cards_html += f"""
                        <div class="forecast-card">
                        <div class="forecast-date">{date}</div>
                        <div class="forecast-icon">{condition.split()[0]}</div>
                        <div class="forecast-temp-max">{temp_max}°C</div>
                        <div class="forecast-temp-min">{temp_min}°C</div>
                        <div class="forecast-detail">💧 <span>{humidity}%</span></div>
                        <div class="forecast-detail">🌬️ <span>{wind} km/h</span></div>
                        <div class="forecast-detail">🌧️ <span>{precip} mm</span></div>
                        </div>
                    """

                    cards_html += '</div>'
                st.markdown(cards_html, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong: {e}")