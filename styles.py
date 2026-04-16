import streamlit as st

def apply_styles():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

/* ── Base ─────────────────────────────────────────────────────────── */
* { box-sizing: border-box; }

.stApp {
    background: #080c14;
    font-family: 'Plus Jakarta Sans', sans-serif;
}

/* ── Sidebar ──────────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1117 0%, #0a0e18 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
}

/* Sidebar page links */
[data-testid="stSidebarNav"] a {
    color: rgba(255,255,255,0.5) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 10px 16px !important;
    border-radius: 10px !important;
    margin: 2px 8px !important;
    transition: all 0.2s ease !important;
    text-decoration: none !important;
}

[data-testid="stSidebarNav"] a:hover {
    background: rgba(255,255,255,0.06) !important;
    color: rgba(255,255,255,0.9) !important;
}

/* Active sidebar link */
[data-testid="stSidebarNav"] a[aria-selected="true"] {
    background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(99,102,241,0.2)) !important;
    color: #ffffff !important;
    border: 1px solid rgba(99,102,241,0.3) !important;
}

/* Sidebar top logo area */
[data-testid="stSidebarHeader"] {
    padding: 1.5rem 1rem 0.5rem !important;
    border-bottom: 1px solid rgba(255,255,255,0.05) !important;
}

/* ── Main container ───────────────────────────────────────────────── */
.block-container {
    padding-top: 2.5rem !important;
    padding-left: 3rem !important;
    padding-right: 3rem !important;
    max-width: 100% !important;
}

header[data-testid="stHeader"] {
    background: transparent !important;
    border-bottom: none !important;
}

/* ── Typography ───────────────────────────────────────────────────── */
h1 {
    color: #ffffff !important;
    font-weight: 800 !important;
    letter-spacing: -0.5px !important;
}

h2, h3 {
    color: rgba(255,255,255,0.9) !important;
    font-weight: 700 !important;
}

h4 {
    color: rgba(255,255,255,0.75) !important;
    font-weight: 600 !important;
}

p, li {
    color: rgba(255,255,255,0.65) !important;
}

label {
    color: rgba(255,255,255,0.55) !important;
    font-size: 13px !important;
}

/* ── Selectbox ────────────────────────────────────────────────────── */
[data-testid="stSelectbox"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
}

/* ── Date input ───────────────────────────────────────────────────── */
[data-testid="stDateInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 12px !important;
    color: #ffffff !important;
}

/* ── Radio buttons ────────────────────────────────────────────────── */
[data-testid="stRadio"] label {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    padding: 8px 16px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stRadio"] label:hover {
    background: rgba(99,102,241,0.1) !important;
    border-color: rgba(99,102,241,0.3) !important;
}

/* ── Spinner ──────────────────────────────────────────────────────── */
[data-testid="stSpinner"] {
    color: #6366f1 !important;
}

/* ── Divider ──────────────────────────────────────────────────────── */
hr {
    border-color: rgba(255,255,255,0.06) !important;
    margin: 1.5rem 0 !important;
}

/* ── Warning / Error boxes ────────────────────────────────────────── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
}

/* ── Home page weather cards ──────────────────────────────────────── */
.cards-row {
    display: flex;
    gap: 14px;
    margin: 24px 0;
    flex-wrap: wrap;
}

.weather-card {
    flex: 1;
    min-width: 130px;
    background: linear-gradient(145deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 24px 16px;
    text-align: center;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}

/* Subtle top accent line on each card */
.weather-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.5), transparent);
}

.weather-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0,0,0,0.4), 0 0 0 1px rgba(99,102,241,0.2);
}

.card-icon { font-size: 28px; margin-bottom: 12px; }

.card-label {
    font-size: 10px;
    color: rgba(255,255,255,0.35);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-bottom: 8px;
}

.card-value {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff;
    word-break: break-word;
    line-height: 1.3;
}

/* ── City hero ────────────────────────────────────────────────────── */
.city-hero {
    text-align: center;
    padding: 32px 0 8px 0;
}

.city-hero-name {
    font-size: 52px;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: -2px;
    background: linear-gradient(135deg, #ffffff, #a5b4fc);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.city-hero-coords {
    font-size: 12px;
    color: rgba(255,255,255,0.3);
    margin-top: 8px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* ── Forecast cards ───────────────────────────────────────────────── */
.forecast-row {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 10px;
    margin: 24px 0;
}

@media (max-width: 900px) {
    .forecast-row { grid-template-columns: repeat(4, 1fr); }
}

.forecast-card {
    background: linear-gradient(145deg, rgba(255,255,255,0.07), rgba(255,255,255,0.02));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 14px 10px;
    text-align: center;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
    position: relative;
    overflow: hidden;
}

.forecast-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.4), transparent);
}

.forecast-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 32px rgba(0,0,0,0.4);
}

.forecast-date {
    font-size: 9px;
    color: rgba(255,255,255,0.4);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}

.forecast-icon { font-size: 22px; margin-bottom: 6px; }

.forecast-temp-max {
    font-size: 17px;
    font-weight: 700;
    color: #ffffff;
}

.forecast-temp-min {
    font-size: 11px;
    color: rgba(255,255,255,0.4);
    margin-bottom: 6px;
}

.forecast-detail {
    font-size: 9px;
    color: rgba(255,255,255,0.45);
    margin: 2px 0;
}

.forecast-detail span {
    color: #a5b4fc;
    font-weight: 600;
}

/* ── Activity / Agriculture / AQ cards ───────────────────────────── */
.score-card {
    text-align: center;
    padding: 40px 20px;
    border-radius: 24px;
    margin: 24px 0;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}

.score-number { font-size: 80px; font-weight: 800; line-height: 1; }
.score-label  { font-size: 16px; margin-top: 12px; opacity: 0.8; }

.score-green   { background: linear-gradient(135deg, rgba(34,197,94,0.15), rgba(34,197,94,0.03));  border: 1px solid rgba(34,197,94,0.2);  color: #4ade80; }
.score-yellow  { background: linear-gradient(135deg, rgba(234,179,8,0.15), rgba(234,179,8,0.03));  border: 1px solid rgba(234,179,8,0.2);  color: #facc15; }
.score-red     { background: linear-gradient(135deg, rgba(239,68,68,0.15), rgba(239,68,68,0.03));  border: 1px solid rgba(239,68,68,0.2);  color: #f87171; }

.precaution-box {
    background: rgba(234,179,8,0.06);
    border: 1px solid rgba(234,179,8,0.15);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 16px 0;
}

.suggestion-box {
    background: rgba(99,102,241,0.07);
    border: 1px solid rgba(99,102,241,0.15);
    border-radius: 16px;
    padding: 20px 24px;
    margin: 16px 0;
}

.box-title {
    font-size: 11px;
    font-weight: 700;
    margin-bottom: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: rgba(255,255,255,0.5) !important;
}

/* Agriculture / AQ detail cards */
.activity-card, .aq-card {
    border-radius: 20px;
    padding: 28px 32px;
    margin-bottom: 20px;
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    position: relative;
    overflow: hidden;
}

.card-good,    .aq-good     { background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.02));   border: 1px solid rgba(34,197,94,0.2); }
.card-marginal,.aq-moderate  { background: linear-gradient(135deg, rgba(234,179,8,0.1), rgba(234,179,8,0.02));   border: 1px solid rgba(234,179,8,0.2); }
.card-poor,    .aq-poor      { background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.02));   border: 1px solid rgba(239,68,68,0.2); }
.aq-fair                     { background: linear-gradient(135deg, rgba(163,230,53,0.1), rgba(163,230,53,0.02)); border: 1px solid rgba(163,230,53,0.2); }
.aq-verypoor                 { background: linear-gradient(135deg, rgba(239,68,68,0.1), rgba(239,68,68,0.02));   border: 1px solid rgba(239,68,68,0.2); }
.aq-hazardous                { background: linear-gradient(135deg, rgba(168,85,247,0.1), rgba(168,85,247,0.02)); border: 1px solid rgba(168,85,247,0.2); }

.card-title, .aq-card-title {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff !important;
    margin-bottom: 8px;
}

.status-badge, .aq-badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    padding: 4px 14px;
    border-radius: 20px;
    margin-bottom: 18px;
}

.badge-good     { background: rgba(34,197,94,0.15);  color: #4ade80; }
.badge-fair     { background: rgba(163,230,53,0.15); color: #a3e635; }
.badge-moderate { background: rgba(234,179,8,0.15);  color: #facc15; }
.badge-poor     { background: rgba(249,115,22,0.15); color: #fb923c; }
.badge-verypoor { background: rgba(239,68,68,0.15);  color: #f87171; }
.badge-hazardous{ background: rgba(168,85,247,0.15); color: #c084fc; }
.badge-marginal { background: rgba(234,179,8,0.15);  color: #facc15; }

.weather-row {
    display: flex;
    gap: 28px;
    margin-bottom: 20px;
    flex-wrap: wrap;
}

.weather-item { display: flex; flex-direction: column; gap: 4px; }

.weather-item-label {
    font-size: 10px;
    color: rgba(255,255,255,0.35) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.weather-item-value {
    font-size: 20px;
    font-weight: 700;
    color: #ffffff !important;
}

.card-reason, .aq-message {
    font-size: 14px;
    color: rgba(255,255,255,0.65) !important;
    margin-bottom: 16px;
    line-height: 1.7;
}

.card-advice, .aq-advice {
    font-size: 13px;
    color: rgba(255,255,255,0.5) !important;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 12px;
    padding: 14px 18px;
    line-height: 1.8;
}

.card-advice-title, .aq-advice-title {
    font-size: 10px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: rgba(255,255,255,0.3) !important;
    margin-bottom: 8px;
}

.aq-value {
    font-size: 52px;
    font-weight: 800;
    color: #ffffff !important;
    margin-bottom: 4px;
    line-height: 1;
}

.aq-unit {
    font-size: 12px;
    color: rgba(255,255,255,0.35) !important;
    margin-bottom: 16px;
}

.health-card {
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(99,102,241,0.02));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 20px;
    padding: 28px 32px;
    margin-top: 12px;
}

.health-title {
    font-size: 12px;
    font-weight: 700;
    color: #a5b4fc !important;
    margin-bottom: 12px;
    text-transform: uppercase;
    letter-spacing: 2px;
}

.health-text {
    font-size: 15px;
    color: rgba(255,255,255,0.7) !important;
    line-height: 1.8;
}

/* Agriculture grid */
.agri-grid {
    display: grid;
    grid-template-columns: 100px repeat(3, 140px);
    gap: 5px;
    margin: 24px 0;
    width: fit-content;
}

.agri-header {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 8px 12px;
    text-align: center;
    font-size: 11px;
    font-weight: 600;
    color: rgba(255,255,255,0.5) !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    width: 140px;
}

.agri-date {
    background: rgba(255,255,255,0.03);
    border-radius: 8px;
    padding: 6px 8px;
    font-size: 11px;
    color: rgba(255,255,255,0.4) !important;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    height: 36px;
}

.agri-cell {
    border-radius: 8px;
    padding: 6px 8px;
    text-align: center;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 1.5px;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 36px;
    width: 140px;
    cursor: pointer;
    text-transform: uppercase;
}

.cell-good     { background: rgba(34,197,94,0.12);  border: 1px solid rgba(34,197,94,0.2);  color: #4ade80; }
.cell-marginal { background: rgba(234,179,8,0.12);  border: 1px solid rgba(234,179,8,0.2);  color: #facc15; }
.cell-poor     { background: rgba(239,68,68,0.12);  border: 1px solid rgba(239,68,68,0.2);  color: #f87171; }

.legend {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;
    font-size: 12px;
    color: rgba(255,255,255,0.4) !important;
}

.legend-item { display: flex; align-items: center; gap: 6px; }
.legend-dot  { width: 8px; height: 8px; border-radius: 50%; }

</style>
""", unsafe_allow_html=True)