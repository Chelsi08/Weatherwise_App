import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import get_coordinates, get_16day_forecast, comfort_score
from styles import apply_styles

st.set_page_config(
    page_title="Weather Insights | WeatherWise",
    page_icon="📊",
    layout="wide"
)

apply_styles()

st.title("📊 Weather Insights")

city = st.session_state.get('city', None)

if not city:
    st.warning("⚠️ Please select a city on the Home page first.")
    st.stop()

st.markdown(f"### 🌍 Analysing 16-day patterns for **{city}**")

with st.spinner("Running analysis..."):
    try:
        lat, lon = get_coordinates(city)
        if lat is None:
            st.error("City not found.")
            st.stop()

        forecast_data = get_16day_forecast(lat, lon)
        daily = forecast_data["daily"]

        # ── Build a proper DataFrame — this is the core data analysis step ──
        df = pd.DataFrame({
            "date":      pd.to_datetime(daily["time"]),
            "temp_max":  daily["temperature_2m_max"],
            "temp_min":  daily["temperature_2m_min"],
            "precip":    daily["precipitation_sum"],
            "humidity":  daily["relative_humidity_2m_max"],
            "wind":      daily["wind_speed_10m_max"],
        })

        # Add derived columns — this is what makes it analysis, not just display
        df["day_of_week"] = df["date"].dt.strftime("%A")  # Monday, Tuesday etc.
        df["day_short"]   = df["date"].dt.strftime("%a")  # Mon, Tue etc.
        df["score"]       = df.apply(
            lambda row: comfort_score(
                row["temp_max"], row["temp_min"],
                row["precip"], row["humidity"], row["wind"]
            ), axis=1
        )

        # ── Analysis 1: Best and worst days of the week ───────────────────
        st.markdown("---")
        st.markdown("#### 📅 Best & Worst Days of the Week")

        # Group by day of week — average score per day
        # This tells us: across the 16-day window, which weekday is best?
        day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

        day_scores = (
            df.groupby("day_of_week")["score"]
            .agg(["mean", "count", "min", "max"])
            .reset_index()
        )
        day_scores.columns = ["Day", "Avg Score", "Count", "Min Score", "Max Score"]

        # Only keep days that appear in our 16-day window
        day_scores = day_scores[day_scores["Day"].isin(day_order)]
        day_scores["Avg Score"] = day_scores["Avg Score"].round(1)

        # Sort by average score descending — best day first
        day_scores = day_scores.sort_values("Avg Score", ascending=False).reset_index(drop=True)

        # Color each bar based on score
        def bar_color(score):
            if score >= 7:
                return "#4ade80"   # green
            elif score >= 5:
                return "#facc15"   # yellow
            else:
                return "#f87171"   # red

        colors = [bar_color(s) for s in day_scores["Avg Score"]]

        fig = go.Figure(go.Bar(
            x=day_scores["Day"],
            y=day_scores["Avg Score"],
            marker_color=colors,
            marker_line_width=0,
            text=day_scores["Avg Score"],
            textposition="outside",
            textfont=dict(color="white", size=12),
        ))

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.03)",
            font=dict(color="rgba(255,255,255,0.7)", family="Plus Jakarta Sans"),
            xaxis=dict(
                gridcolor="rgba(255,255,255,0.05)",
                title="Day of Week",
                categoryorder="array",
                categoryarray=day_scores["Day"].tolist()
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.05)",
                title="Comfort Score (0-10)",
                range=[0, 11]
            ),
            height=380,
            margin=dict(t=20, b=20),
            showlegend=False,
        )

        st.plotly_chart(fig, use_container_width=True)

        # ── Written insight ───────────────────────────────────────────────
        best_day  = day_scores.iloc[0]
        worst_day = day_scores.iloc[-1]

        # Find actual dates for best and worst days
        best_dates  = df[df["day_of_week"] == best_day["Day"]]["date"].dt.strftime("%d %b").tolist()
        worst_dates = df[df["day_of_week"] == worst_day["Day"]]["date"].dt.strftime("%d %b").tolist()

        # Explain why the best day is best
        best_day_data = df[df["day_of_week"] == best_day["Day"]].mean(numeric_only=True)
        worst_day_data = df[df["day_of_week"] == worst_day["Day"]].mean(numeric_only=True)

        best_reason = []
        if best_day_data["precip"] < 2:
            best_reason.append(f"low rainfall ({best_day_data['precip']:.1f}mm avg)")
        if 18 <= best_day_data["temp_max"] <= 28:
            best_reason.append(f"comfortable temperatures ({best_day_data['temp_max']:.1f}°C avg)")
        if best_day_data["humidity"] < 70:
            best_reason.append(f"manageable humidity ({best_day_data['humidity']:.0f}%)")
        if best_day_data["wind"] < 20:
            best_reason.append(f"calm winds ({best_day_data['wind']:.1f}km/h)")

        worst_reason = []
        if worst_day_data["precip"] > 5:
            worst_reason.append(f"heavy rainfall ({worst_day_data['precip']:.1f}mm avg)")
        if worst_day_data["temp_max"] > 35:
            worst_reason.append(f"extreme heat ({worst_day_data['temp_max']:.1f}°C avg)")
        if worst_day_data["humidity"] > 80:
            worst_reason.append(f"high humidity ({worst_day_data['humidity']:.0f}%)")
        if worst_day_data["wind"] > 30:
            worst_reason.append(f"strong winds ({worst_day_data['wind']:.1f}km/h)")

        best_reason_str  = ", ".join(best_reason)  if best_reason  else "generally pleasant conditions"
        worst_reason_str = ", ".join(worst_reason) if worst_reason else "consistently poor conditions"

        st.markdown(f"""
<div class="suggestion-box">
    <div class="box-title">📊 What the data shows</div>
    <p style="color:rgba(255,255,255,0.75); font-size:14px; line-height:1.8; margin:0;">
        <strong style="color:#4ade80;">{best_day['Day']}s are your best days</strong> 
        in the next 16 days — averaging a comfort score of 
        <strong style="color:#4ade80;">{best_day['Avg Score']}/10</strong> 
        driven by {best_reason_str}.
        Upcoming {best_day['Day']}s: <strong>{', '.join(best_dates)}</strong>.
        <br><br>
        <strong style="color:#f87171;">{worst_day['Day']}s look worst</strong> 
        — averaging just <strong style="color:#f87171;">{worst_day['Avg Score']}/10</strong> 
        due to {worst_reason_str}.
        Upcoming {worst_day['Day']}s to avoid: <strong>{', '.join(worst_dates)}</strong>.
    </p>
</div>
""", unsafe_allow_html=True)

        # ── Analysis 2: Daily scores over 16 days ────────────────────────
        st.markdown("---")
        st.markdown("#### 📈 Day-by-Day Comfort Score")

        # Color each point by score
        df["color"] = df["score"].apply(bar_color)
        df["date_label"] = df["date"].dt.strftime("%a %d %b")

        fig2 = go.Figure()

        # Add the line
        fig2.add_trace(go.Scatter(
            x=df["date_label"],
            y=df["score"],
            mode="lines+markers",
            line=dict(color="#6366f1", width=2.5),
            marker=dict(
                color=df["color"],
                size=10,
                line=dict(color="#080c14", width=2)
            ),
            hovertemplate="<b>%{x}</b><br>Score: %{y}/10<extra></extra>"
        ))

        # Add reference lines for context
        fig2.add_hline(y=7, line_dash="dash", line_color="rgba(74,222,128,0.3)",
                       annotation_text="Good (7)", annotation_font_color="rgba(74,222,128,0.6)")
        fig2.add_hline(y=5, line_dash="dash", line_color="rgba(234,179,8,0.3)",
                       annotation_text="Moderate (5)", annotation_font_color="rgba(234,179,8,0.6)")

        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(255,255,255,0.03)",
            font=dict(color="rgba(255,255,255,0.7)", family="Plus Jakarta Sans"),
            xaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Date"),
            yaxis=dict(gridcolor="rgba(255,255,255,0.05)", title="Comfort Score", range=[0,11]),
            height=350,
            margin=dict(t=20, b=20),
            showlegend=False,
        )

        st.plotly_chart(fig2, use_container_width=True)

        # Written insight for day-by-day
        best_single  = df.loc[df["score"].idxmax()]
        worst_single = df.loc[df["score"].idxmin()]
        avg_score    = df["score"].mean().round(1)
        good_days    = len(df[df["score"] >= 7])

        st.markdown(f"""
<div class="suggestion-box">
    <div class="box-title">📊 What the data shows</div>
    <p style="color:rgba(255,255,255,0.75); font-size:14px; line-height:1.8; margin:0;">
        Over the next 16 days, the average comfort score for <strong>{city}</strong> is 
        <strong style="color:#a5b4fc;">{avg_score}/10</strong> with 
        <strong style="color:#4ade80;">{good_days} days scoring 7 or above</strong>.
        <br><br>
        <strong>Best single day:</strong> 
        <strong style="color:#4ade80;">{best_single['date_label']}</strong> 
        with a score of {best_single['score']}/10 
        (max {best_single['temp_max']}°C, {best_single['precip']}mm rain).
        <br>
        <strong>Worst single day:</strong> 
        <strong style="color:#f87171;">{worst_single['date_label']}</strong> 
        with a score of {worst_single['score']}/10 
        (max {worst_single['temp_max']}°C, {worst_single['precip']}mm rain).
    </p>
</div>
""", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Something went wrong: {e}")