import streamlit as st
import pandas as pd
from datetime import date, timedelta
from utils import get_coordinates, get_16day_forecast
from styles import apply_styles

st.set_page_config(
    page_title="Agriculture Advisor | WeatherWise",
    page_icon="🌾",
    layout="wide"
)

apply_styles()

st.title("🌾 Agriculture Advisor")

city = st.session_state.get('city', None)

if not city:
    st.warning("⚠️ Please select a city on the Home page first.")
    st.stop()

st.markdown(f"### 🌍 Planning for **{city}**")

selected_date = st.date_input(
    "📅 Pick a date to analyse",
    value=date.today(),
    min_value=date.today(),
    max_value=date.today() + timedelta(days=15)
)

if selected_date:
    with st.spinner("Analysing agricultural conditions..."):
        try:
            lat, lon = get_coordinates(city)
            if lat is None:
                st.error("City not found.")
                st.stop()

            forecast_data = get_16day_forecast(lat, lon)
            daily = forecast_data["daily"]

            # Find index matching selected date
            forecast_dates = [pd.to_datetime(d).date() for d in daily["time"]]
            if selected_date not in forecast_dates:
                st.error("Date outside forecast range.")
                st.stop()

            idx = forecast_dates.index(selected_date)

            # Extract actual values for that day
            temp_max = daily["temperature_2m_max"][idx]
            temp_min = daily["temperature_2m_min"][idx]
            precip   = daily["precipitation_sum"][idx]
            humidity = daily["relative_humidity_2m_max"][idx]
            wind     = daily["wind_speed_10m_max"][idx]

            st.markdown(f"#### Weather on {selected_date.strftime('%A, %d %B %Y')}")

            # ── Build detailed assessment for each activity ──────────────────

            activities = {
                "🌱 Planting": None,
                "💧 Irrigation": None,
                "🌾 Harvesting": None,
            }

            # PLANTING assessment
            if 15 <= temp_max <= 30 and precip <= 5:
                activities["🌱 Planting"] = {
                    "status": "good",
                    "reason": (
                        f"Temperature is {temp_max}°C (ideal range: 15–30°C) and precipitation is only {precip}mm "
                        f"(threshold: ≤5mm). Soil conditions are workable and temperature supports seed germination."
                    ),
                    "advice": (
                        "✔ Proceed with planting. Morning hours are best to avoid afternoon heat stress on seedlings. "
                        "Ensure proper seed depth and spacing. "
                        f"With {humidity}% humidity, monitor for fungal issues in the following days."
                    )
                }
            elif 10 <= temp_max <= 35 and precip <= 10:
                activities["🌱 Planting"] = {
                    "status": "marginal",
                    "reason": (
                        f"Temperature is {temp_max}°C and precipitation is {precip}mm. "
                        f"{'Temperature is slightly outside the ideal 15–30°C range.' if not (15 <= temp_max <= 30) else ''} "
                        f"{'Rainfall of ' + str(precip) + 'mm may leave soil too wet for optimal planting.' if precip > 5 else ''}"
                    ),
                    "advice": (
                        "⚠ Planting is possible but risky. Check soil moisture before proceeding — if soil clumps heavily when squeezed, wait one day. "
                        f"If temperature exceeds 30°C like today's {temp_max}°C, plant in the evening to reduce heat stress. "
                        "Use raised beds if waterlogging is a concern."
                    )
                }
            else:
                activities["🌱 Planting"] = {
                    "status": "poor",
                    "reason": (
                        f"Temperature is {temp_max}°C and precipitation is {precip}mm. "
                        f"{'Extreme temperature will inhibit germination.' if temp_max > 35 or temp_max < 10 else ''} "
                        f"{'Heavy rainfall of ' + str(precip) + 'mm will waterlog soil and rot seeds.' if precip > 10 else ''}"
                    ),
                    "advice": (
                        "✘ Avoid planting today. Waterlogged or extremely hot/cold soil will kill seeds before germination. "
                        "Use this day to prepare equipment, check seeds, or apply compost to improve soil structure. "
                        "Wait for a drier, moderate temperature window."
                    )
                }

            # IRRIGATION assessment
            if 10 <= temp_max <= 35 and precip <= 2:
                activities["💧 Irrigation"] = {
                    "status": "good",
                    "reason": (
                        f"Only {precip}mm of rain expected today and temperature is {temp_max}°C. "
                        f"With {humidity}% humidity, crops will experience moisture stress without irrigation."
                    ),
                    "advice": (
                        f"✔ Irrigate today. Early morning (before 8am) is optimal to minimise evaporation — "
                        f"at {temp_max}°C, midday evaporation losses can be significant. "
                        "Drip irrigation is most efficient in these conditions. "
                        f"With wind at {wind}km/h, avoid sprinkler irrigation as drift losses will be high."
                        if wind > 20 else
                        "✔ Irrigate today. Early morning irrigation before 8am is optimal to minimise evaporation losses."
                    )
                }
            elif precip <= 5:
                activities["💧 Irrigation"] = {
                    "status": "marginal",
                    "reason": (
                        f"Rainfall of {precip}mm is expected — this may partially meet crop water needs depending on soil type and crop stage."
                    ),
                    "advice": (
                        f"⚠ Check soil moisture before irrigating. If soil is still moist from the {precip}mm rainfall, skip irrigation today. "
                        "Sandy soils will drain quickly and may still need supplemental irrigation. "
                        "Clay soils will retain moisture longer — probe before deciding."
                    )
                }
            else:
                activities["💧 Irrigation"] = {
                    "status": "poor",
                    "reason": (
                        f"Rainfall of {precip}mm is forecast — this exceeds crop water requirements for most crops."
                    ),
                    "advice": (
                        f"✘ Do not irrigate today. {precip}mm of rainfall is sufficient and additional irrigation risks waterlogging and root rot. "
                        "Use this time to check drainage channels and ensure fields can handle the rainfall without flooding."
                    )
                }

            # HARVESTING assessment
            if 15 <= temp_max <= 35 and precip <= 1:
                activities["🌾 Harvesting"] = {
                    "status": "good",
                    "reason": (
                        f"Dry conditions with only {precip}mm rain forecast and temperature at {temp_max}°C. "
                        f"Low precipitation means harvested crops won't absorb moisture, preserving quality."
                    ),
                    "advice": (
                        f"✔ Excellent harvest conditions. Begin early morning when temperature is closer to {temp_min}°C "
                        f"to reduce crop stress. Wind at {wind}km/h — "
                        + ("minimal interference expected." if wind <= 20 else "moderate wind may scatter lightweight crops, use nets or covers.")
                        + f" With {humidity}% humidity, drying time post-harvest will be "
                        + ("short — good for storage." if humidity <= 60 else "longer than ideal — ensure proper ventilation in storage.")
                    )
                }
            elif precip <= 5:
                activities["🌾 Harvesting"] = {
                    "status": "marginal",
                    "reason": (
                        f"Light rain of {precip}mm is possible. Harvested crops may absorb surface moisture, "
                        f"affecting weight and storage quality."
                    ),
                    "advice": (
                        f"⚠ Harvest in the early morning before any rain arrives. {precip}mm is light but enough to wet "
                        "crop surfaces. If harvesting grain crops, ensure immediate drying after collection. "
                        "Avoid leaving cut crops in the field overnight — bring them under cover."
                    )
                }
            else:
                activities["🌾 Harvesting"] = {
                    "status": "poor",
                    "reason": (
                        f"Heavy rainfall of {precip}mm forecast. Wet crops are prone to mould, weight loss, "
                        f"and quality degradation. Machinery may also struggle in waterlogged fields."
                    ),
                    "advice": (
                        f"✘ Do not harvest today. {precip}mm of rain will wet crops and significantly reduce quality. "
                        "Use this day for equipment maintenance, storage preparation, or applying fertiliser "
                        "if soil conditions allow. Wait for at least 2 consecutive dry days before harvesting."
                    )
                }

            # ── Render each activity card ────────────────────────────────────
            for activity_name, data in activities.items():
                status  = data["status"]
                reason  = data["reason"]
                advice  = data["advice"]
                label   = {"good": "IDEAL", "marginal": "CAUTION", "poor": "AVOID"}[status]

                st.markdown(f"""
<div class="activity-card card-{status}">
    <div class="card-title">{activity_name}</div>
    <div class="status-badge badge-{status}">{label}</div>
    <div class="weather-row">
        <div class="weather-item">
            <div class="weather-item-label">Max Temp</div>
            <div class="weather-item-value">{temp_max}°C</div>
        </div>
        <div class="weather-item">
            <div class="weather-item-label">Min Temp</div>
            <div class="weather-item-value">{temp_min}°C</div>
        </div>
        <div class="weather-item">
            <div class="weather-item-label">Rainfall</div>
            <div class="weather-item-value">{precip}mm</div>
        </div>
        <div class="weather-item">
            <div class="weather-item-label">Humidity</div>
            <div class="weather-item-value">{humidity}%</div>
        </div>
        <div class="weather-item">
            <div class="weather-item-label">Wind</div>
            <div class="weather-item-value">{wind}km/h</div>
        </div>
    </div>
    <div class="card-reason">{reason}</div>
    <div class="card-advice">
        <div class="card-advice-title">💡 Recommended Action</div>
        {advice}
    </div>
</div>
""", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong: {e}")