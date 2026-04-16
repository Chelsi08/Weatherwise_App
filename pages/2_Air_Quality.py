import streamlit as st
from utils import get_coordinates, get_air_quality, interpret_aqi, interpret_uv, interpret_co, interpret_pm25
from styles import apply_styles

st.set_page_config(
    page_title="Air Quality | WeatherWise",
    page_icon="💨",
    layout="wide"
)

apply_styles()

st.title("💨 Air Quality & Weather")

city = st.session_state.get('city', None)

if not city:
    st.warning("⚠️ Please select a city on the Home page first.")
    st.stop()

st.markdown(f"### 🌍 Current conditions in **{city}**")

with st.spinner("Fetching air quality and weather data..."):
    try:
        lat, lon = get_coordinates(city)
        if lat is None:
            st.error("City not found.")
            st.stop()

        aq_data      = get_air_quality(lat, lon)
        aq           = aq_data["current"]
       
        

        st.divider()
        st.markdown("#### 💨 Air Quality Breakdown")

        # AQI card
        aqi_value = aq["european_aqi"]
        aqi_cat, aqi_cls, aqi_msg = interpret_aqi(aqi_value)
        st.markdown(f"""
<div class="aq-card aq-{aqi_cls}">
    <div class="aq-card-title">💨 Air Quality Index (AQI)</div>
    <div class="aq-badge badge-{aqi_cls}">{aqi_cat}</div>
    <div class="aq-value">{aqi_value}</div>
    <div class="aq-unit">European AQI Scale (0 = best, 500 = worst)</div>
    <div class="aq-message">{aqi_msg}</div>
    <div class="aq-advice">
        <div class="aq-advice-title">💡 What this means</div>
        {"No restrictions on outdoor activities today." if aqi_value <= 20 else
         "Healthy individuals can go about normal activities. Sensitive groups should monitor symptoms." if aqi_value <= 40 else
         "Children and elderly should limit time outdoors. Keep windows closed during peak traffic hours." if aqi_value <= 60 else
         "Limit all outdoor activity. Wear an N95 mask if going outside. Keep indoor air filtered." if aqi_value <= 80 else
         "Stay indoors. Run air purifiers if available. Avoid any outdoor exertion." if aqi_value <= 100 else
         "Health emergency conditions. Stay indoors completely. Seek medical advice if experiencing symptoms."}
    </div>
</div>
""", unsafe_allow_html=True)

        # UV card
        uv_value = aq["uv_index"]
        uv_cat, uv_msg = interpret_uv(uv_value)
        uv_cls = (
            "good" if uv_value <= 2 else
            "fair" if uv_value <= 5 else
            "moderate" if uv_value <= 7 else
            "poor" if uv_value <= 10 else
            "hazardous"
        )
        st.markdown(f"""
<div class="aq-card aq-{uv_cls}">
    <div class="aq-card-title">☀️ UV Index</div>
    <div class="aq-badge badge-{uv_cls}">{uv_cat}</div>
    <div class="aq-value">{uv_value}</div>
    <div class="aq-unit">WHO Scale (0 = no risk, 11+ = extreme)</div>
    <div class="aq-message">{uv_msg}</div>
    <div class="aq-advice">
        <div class="aq-advice-title">💡 Protection Advice</div>
        {"No sunscreen needed. Safe for outdoor activity at any time." if uv_value <= 2 else
         "Apply SPF 30+ sunscreen. Seek shade between 11am and 3pm." if uv_value <= 5 else
         "Apply SPF 50+ sunscreen every 2 hours. Wear a wide-brim hat and UV-blocking sunglasses. Avoid midday sun." if uv_value <= 7 else
         "Minimise sun exposure between 10am–4pm. Long sleeves, hat, SPF 50+ mandatory. Reapply sunscreen every 90 minutes." if uv_value <= 10 else
         "Avoid all outdoor exposure during daylight hours if possible. Full protective clothing and maximum SPF required."}
    </div>
</div>
""", unsafe_allow_html=True)

        # CO card
        co_value = aq["carbon_monoxide"]
        co_cat, co_msg = interpret_co(co_value)
        co_cls = (
            "good" if co_value <= 1000 else
            "fair" if co_value <= 4000 else
            "moderate" if co_value <= 10000 else
            "hazardous"
        )
        st.markdown(f"""
<div class="aq-card aq-{co_cls}">
    <div class="aq-card-title">🏭 Carbon Monoxide (CO)</div>
    <div class="aq-badge badge-{co_cls}">{co_cat}</div>
    <div class="aq-value">{co_value}</div>
    <div class="aq-unit">μg/m³ — WHO safe limit: 4,000 μg/m³ (1hr exposure)</div>
    <div class="aq-message">{co_msg}</div>
    <div class="aq-advice">
        <div class="aq-advice-title">💡 Safety Advice</div>
        {"CO levels are safe. No precautions needed." if co_value <= 1000 else
         "CO is within acceptable range. Ensure indoor spaces are well ventilated." if co_value <= 4000 else
         "Elevated CO detected. Avoid prolonged outdoor exposure." if co_value <= 10000 else
         "Dangerous CO levels. Stay indoors. Seek immediate medical attention if feeling dizzy."}
    </div>
</div>
""", unsafe_allow_html=True)

        # PM2.5 card
        pm25_value = aq["pm2_5"]
        pm25_cat, pm25_cls, pm25_msg = interpret_pm25(pm25_value)
        st.markdown(f"""
<div class="aq-card aq-{pm25_cls}">
    <div class="aq-card-title">🔬 PM2.5 Fine Particles</div>
    <div class="aq-badge badge-{pm25_cls}">{pm25_cat}</div>
    <div class="aq-value">{pm25_value}</div>
    <div class="aq-unit">μg/m³ — WHO safe limit: 15 μg/m³ daily average</div>
    <div class="aq-message">{pm25_msg}</div>
    <div class="aq-advice">
        <div class="aq-advice-title">💡 Health Advice</div>
        {"PM2.5 is within safe limits. No precautions needed." if pm25_value <= 15 else
         f"PM2.5 is {pm25_value} μg/m³ — {round(pm25_value/15, 1)}x the WHO daily limit. Sensitive groups should wear N95 masks outdoors." if pm25_value <= 55 else
         f"PM2.5 is {pm25_value} μg/m³ — {round(pm25_value/15, 1)}x the WHO limit. Everyone should wear N95 masks. Avoid outdoor exercise." if pm25_value <= 150 else
         f"PM2.5 is {pm25_value} μg/m³ — {round(pm25_value/15, 1)}x the WHO limit. Health emergency. Stay indoors, seal windows, run air purifiers."}
    </div>
</div>
""", unsafe_allow_html=True)

        # Overall health recommendation
        overall_risk = max(aqi_value / 100, uv_value / 11, co_value / 4000, pm25_value / 150)

        if overall_risk <= 0.3:
            overall = "Today's conditions are safe across all indicators. You can go about outdoor activities normally."
        elif overall_risk <= 0.6:
            overall = "Conditions are moderate. Sensitive individuals (children, elderly, those with respiratory conditions) should take precautions outlined above."
        elif overall_risk <= 0.9:
            overall = "Multiple indicators are elevated today. Limit outdoor time, wear protection, and keep windows closed."
        else:
            overall = "High risk conditions detected. Stay indoors, use air purification if available, and monitor health symptoms closely."

        st.markdown(f"""
<div class="health-card">
    <div class="health-title">🩺 Overall Health Recommendation</div>
    <div class="health-text">{overall}</div>
</div>
""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Something went wrong: {e}")