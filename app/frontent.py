import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sqlite3
from datetime import datetime
import time
import logging
import os

# ================= CONFIG =================
class Config:
    SAFE = float(os.getenv("SAFE_THRESHOLD", 40))
    MODERATE = float(os.getenv("MODERATE_THRESHOLD", 80))
    ANOMALY_Z = 2.0
    DRIFT_THRESHOLD = 20

# ================= LOGGING =================
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ================= UI =================
st.set_page_config(page_title="NOx AI Control Center", layout="wide")

st.markdown("""
<style>
.big-font {font-size:40px !important; font-weight:700;}
.status-safe {color: #00ff9c; font-weight:bold;}
.status-mod {color: orange; font-weight:bold;}
.status-unsafe {color: red; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">⚡ NOx AI Control Center (v9 - Enterprise AI)</p>', unsafe_allow_html=True)

# ================= LOAD MODEL =================
@st.cache_resource
def load_model():
    return pickle.load(open("nox_rf_model.pkl", "rb"))

model = load_model()

# ================= DATABASE SERVICE =================
@st.cache_resource
def init_db():
    conn = sqlite3.connect("nox_data.db", check_same_thread=False)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS readings(
        time TEXT PRIMARY KEY,
        ml REAL,
        physics REAL,
        residual REAL,
        status TEXT
    )
    """)
    return conn

conn = init_db()

def save_reading(ml, phy, residual, status, retries=3):
    for _ in range(retries):
        try:
            conn.execute(
                "INSERT INTO readings VALUES (?, ?, ?, ?, ?)",
                (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ml, phy, residual, status)
            )
            conn.commit()
            return
        except:
            time.sleep(0.1)
    logging.warning("DB write failed after retries")

def load_history():
    df = pd.read_sql("SELECT * FROM readings ORDER BY time DESC LIMIT 300", conn)
    return df[::-1]

# ================= SENSOR SERVICE =================
def generate_sensor_data():
    now = datetime.now()
    return {
        "no": np.random.uniform(10, 200),
        "no2": np.random.uniform(10, 200),
        "relativehumidity": np.random.uniform(30, 90),
        "temperature": np.random.uniform(20, 50),
        "wind_direction": np.random.uniform(0, 360),
        "wind_speed": np.random.uniform(0, 10),
        "hour": now.hour,
        "day": now.day,
        "weekday": now.weekday(),
        "month": now.month
    }

# ================= MODELS =================
def physics_model(s):
    return (
        0.5*s["no"] +
        0.3*s["no2"] -
        0.2*s["wind_speed"] +
        0.1*s["temperature"]
    )

def classify(val, safe, moderate):
    if val < safe:
        return "SAFE", "status-safe"
    elif val < moderate:
        return "MODERATE", "status-mod"
    return "UNSAFE", "status-unsafe"

# ================= ANALYTICS =================
def adaptive_thresholds(series):
    if len(series) < 20:
        return Config.SAFE, Config.MODERATE
    return series.mean() - series.std(), series.mean() + series.std()

def detect_anomaly(series):
    if len(series) < 10:
        return False
    z = (series.iloc[-1] - series.mean()) / (series.std() or 1)
    return abs(z) > Config.ANOMALY_Z

def detect_drift(series):
    if len(series) < 20:
        return False
    return abs(series.iloc[-1] - series.mean()) > Config.DRIFT_THRESHOLD

def stability_score(series):
    if len(series) < 5:
        return 0.5
    return max(0, min(1, 1 / (1 + series.std())))

def health_score(anomaly, drift, stability):
    score = stability * 100
    if anomaly:
        score -= 30
    if drift:
        score -= 20
    return max(0, min(100, score))

# ================= SESSION CONTROL =================
if "last_run" not in st.session_state:
    st.session_state.last_run = 0

refresh_rate = st.sidebar.slider("Refresh Rate", 1, 10, 3)

if time.time() - st.session_state.last_run > refresh_rate:
    st.session_state.last_run = time.time()

    sensor = generate_sensor_data()
    df_input = pd.DataFrame([sensor])

    ml_pred = float(model.predict(df_input)[0])
    phy_pred = physics_model(sensor)
    residual = abs(ml_pred - phy_pred)

    hist_temp = load_history()
    safe_t, mod_t = adaptive_thresholds(hist_temp["ml"] if not hist_temp.empty else pd.Series())

    status, css = classify(ml_pred, safe_t, mod_t)

    save_reading(ml_pred, phy_pred, residual, status)

# ================= LOAD DATA =================
hist = load_history()

# ================= ANALYTICS =================
if not hist.empty:
    hist["smooth"] = hist["ml"].rolling(5).mean()

    anomaly = detect_anomaly(hist["ml"])
    drift = detect_drift(hist["ml"])
    stability = stability_score(hist["ml"])
    health = health_score(anomaly, drift, stability)
else:
    anomaly = drift = False
    stability = 0
    health = 0

# ================= DASHBOARD =================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📈 Hybrid NOx Monitoring")
    if not hist.empty:
        st.line_chart(hist.set_index("time")[["ml", "physics", "smooth"]])

    st.subheader("📉 Residual Error")
    if not hist.empty:
        st.line_chart(hist.set_index("time")["residual"])

with col2:
    st.subheader("🤖 AI Decision Engine")

    if not hist.empty:
        latest = hist.iloc[-1]

        st.metric("ML", f"{latest['ml']:.2f}")
        st.metric("Physics", f"{latest['physics']:.2f}")
        st.metric("Residual", f"{latest['residual']:.2f}")
        st.metric("Health Score", f"{health:.1f}/100")

        st.markdown(f"<h2 class='{classify(latest['ml'], Config.SAFE, Config.MODERATE)[1]}'>{latest['status']}</h2>", unsafe_allow_html=True)

        if anomaly:
            st.error("🚨 Anomaly Detected")
        if drift:
            st.warning("⚠ Drift Detected")

# ================= AUTO REFRESH =================
time.sleep(1)
st.rerun()
