import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils import get_coordinates, get_16day_forecast, score_activity

st.set_page_config(
    page_title="Activity Planner | WeatherWise",
    page_icon="🏃",
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

/* Score card — big centered block showing the number */
.score-card {
    text-align: center;
    padding: 40px 20px;
    border-radius: 24px;
    margin: 24px 0;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
}

/* The large score number */
.score-number {
    font-size: 80px;
    font-weight: 700;
    line-height: 1;
}

.score-label {
    font-size: 18px;
    margin-top: 10px;
    opacity: 0.8;
}

/* Green theme for good scores */
.score-green {
    background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(34,197,94,0.05));
    border: 1px solid rgba(34,197,94,0.3);
    color: #4ade80;
}

/* Yellow theme for moderate scores */
.score-yellow {
    background: linear-gradient(135deg, rgba(234,179,8,0.15), rgba(234,179,8,0.05));
    border: 1px solid rgba(234,179,8,0.3);
    color: #facc15;
}

/* Red theme for poor scores */
.score-red {
    background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(239,68,68,0.05));
    border: 1px solid rgba(239,68,68,0.3);
    color: #f87171;
}

/* Precaution box — shown for yellow scores */
.precaution-box {
    background: rgba(234,179,8,0.08);
    border: 1px solid rgba(234,179,8,0.2);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 16px 0;
    color: rgba(255,255,255,0.8);
}

/* Next best date suggestion — shown for red scores */
.suggestion-box {
    background: rgba(96,165,250,0.08);
    border: 1px solid rgba(96,165,250,0.2);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 16px 0;
    color: rgba(255,255,255,0.8);
}

.box-title {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏃 Activity Planner")

# Get city from session_state — same city user picked on Home or Forecast
city = st.session_state.get('city', None)

if not city:
    # No city selected yet — tell user to go pick one
    st.warning("⚠️ Please select a city on the Home page first.")
    st.stop()  # stops the rest of the page from running

st.markdown(f"### 🌍 Planning for **{city}**")

# Date picker — today as default, max 16 days ahead since that's our forecast limit
selected_date = st.date_input(
    "📅 Pick a date",
    value=date.today(),           # defaults to today
    min_value=date.today(),       # can't pick past dates
    max_value=date.today() + timedelta(days=15)  # 16 days including today
)

# Activity selector — radio gives one choice at a time, horizontal saves space
activity = st.radio(
    "🎯 Choose an activity",
    options=["⚽ Sport", "🥾 Hiking", "🏖️ Beach"],
    horizontal=True  # displays options side by side instead of stacked
)
if city and selected_date and activity:
    with st.spinner("Analysing conditions..."):
        try:
            lat, lon = get_coordinates(city)
            if lat is None:
                st.error("City not found.")
                st.stop()

            forecast_data = get_16day_forecast(lat, lon)
            daily = forecast_data["daily"]

            # Find which index in the forecast matches the selected date
            # daily["time"] is a list like ["2026-04-08", "2026-04-09", ...]
            forecast_dates = [pd.to_datetime(d).date() for d in daily["time"]]

            if selected_date not in forecast_dates:
                st.error("Selected date is outside the 16-day forecast range.")
                st.stop()

            # Get the index of the selected date
            idx = forecast_dates.index(selected_date)  

            # Extract weather values for that specific day
            temp_max  = daily["temperature_2m_max"][idx]
            temp_min  = daily["temperature_2m_min"][idx]
            humidity  = daily["relative_humidity_2m_max"][idx]
            precip    = daily["precipitation_sum"][idx]
            wind      = daily["wind_speed_10m_max"][idx]

            # Run the scoring function from utils
            score, precautions = score_activity(activity, temp_max, temp_min, humidity, precip, wind)

            # Determine color theme based on score
            if score >= 8:
                theme = "score-green"
                verdict = "Great day for this activity! 🎉"
            elif score >= 5:
                theme = "score-yellow"
                verdict = "Manageable — but take precautions ⚠️"
            else:
                theme = "score-red"
                verdict = "Poor conditions — consider another day ❌"

            # Display the score card
            st.markdown(f"""
<div class="score-card {theme}">
    <div class="score-number">{score}</div>
    <div class="score-label">{verdict}</div>
</div>
""", unsafe_allow_html=True)

            # Show weather summary for that day
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("🌡️ Max Temp", f"{temp_max}°C")
            col2.metric("💧 Humidity", f"{humidity}%")
            col3.metric("🌧️ Precipitation", f"{precip} mm")
            col4.metric("🌬️ Wind", f"{wind} km/h")

            # Show precautions if score is 5-7
            if 5 <= score < 8 and precautions:
                precaution_items = "".join([f"<li>{p}</li>" for p in precautions])
                st.markdown(f"""
<div class="precaution-box">
    <div class="box-title">⚠️ Precautions</div>
    <ul style="margin:0; padding-left:18px; line-height:2;">
        {precaution_items}
    </ul>
</div>
""", unsafe_allow_html=True)

            # Find next best date if score is below 5
            if score < 5:
                best_date = None
                best_score = 0

                # Loop through all 16 days to find the highest scoring day
                for i, d in enumerate(forecast_dates):
                    if d <= selected_date:
                        continue  # skip past dates and the selected date itself
                    s, _ = score_activity(
                        activity,
                        daily["temperature_2m_max"][i],
                        daily["temperature_2m_min"][i],
                        daily["relative_humidity_2m_max"][i],
                        daily["precipitation_sum"][i],
                        daily["wind_speed_10m_max"][i]
                    )
                    if s > best_score:
                        best_score = s
                        best_date = d

                if best_date:
                    st.markdown(f"""
<div class="suggestion-box">
    <div class="box-title">📅 Next Best Date</div>
    <p style="margin:0; font-size:16px;">
        Try <strong>{best_date.strftime("%A, %d %b")}</strong> — 
        forecast score: <strong>{best_score}/10</strong>
    </p>
</div>
""", unsafe_allow_html=True)
                else:
                    st.markdown("""
<div class="suggestion-box">
    <div class="box-title">📅 Next Best Date</div>
    <p style="margin:0;">No significantly better day found in the 16-day window.</p>
</div>
""", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong: {e}")