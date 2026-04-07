import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sqlite3
from datetime import datetime
import time
import logging

# ---------------- CONFIG CLASS ----------------
class Config:
    SAFE = 40
    MODERATE = 80
    ANOMALY_Z = 2.0
    DRIFT_THRESHOLD = 20

# ---------------- LOGGING ----------------
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------- UI ----------------
st.set_page_config(page_title="NOx AI Control Center", layout="wide")

st.markdown("""
<style>
.big-font {font-size:40px !important; font-weight:700;}
.status-safe {color: #00ff9c; font-weight:bold;}
.status-mod {color: orange; font-weight:bold;}
.status-unsafe {color: red; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">⚡ NOx AI Control Center (v7 - Hybrid AI)</p>', unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    return pickle.load(open("nox_rf_model.pkl", "rb"))

model = load_model()

# ---------------- DATABASE ----------------
@st.cache_resource
def init_db():
    conn = sqlite3.connect("nox_data.db", check_same_thread=False)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS readings(
        time TEXT PRIMARY KEY,
        ml_prediction REAL,
        physics_prediction REAL,
        residual REAL,
        status TEXT
    )
    """)
    return conn

conn = init_db()

# ---------------- SENSOR ----------------
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

# ---------------- PHYSICS MODEL ----------------
def physics_model(sensor):
    # Simple proxy equation (you can justify in research)
    return (
        0.5 * sensor["no"] +
        0.3 * sensor["no2"] -
        0.2 * sensor["wind_speed"] +
        0.1 * sensor["temperature"]
    )

# ---------------- CLASSIFICATION ----------------
def classify(val):
    if val < Config.SAFE:
        return "SAFE", "status-safe"
    elif val < Config.MODERATE:
        return "MODERATE", "status-mod"
    else:
        return "UNSAFE", "status-unsafe"

# ---------------- ANALYTICS ----------------
def detect_anomaly(series):
    if len(series) < 10:
        return False
    z = (series.iloc[-1] - series.mean()) / (series.std() or 1)
    return abs(z) > Config.ANOMALY_Z

def detect_drift(series):
    if len(series) < 20:
        return False
    return abs(series.iloc[-1] - series.mean()) > Config.DRIFT_THRESHOLD

# ---------------- DB ----------------
def save_reading(ml, phy, residual, status):
    try:
        conn.execute(
            "INSERT INTO readings VALUES (?, ?, ?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ml, phy, residual, status)
        )
        conn.commit()
    except:
        logging.warning("DB write skipped")

def load_history():
    df = pd.read_sql("SELECT * FROM readings ORDER BY time DESC LIMIT 300", conn)
    return df[::-1]

# ---------------- SESSION ----------------
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
    status, css = classify(ml_pred)

    save_reading(ml_pred, phy_pred, residual, status)

# ---------------- LOAD ----------------
hist = load_history()

# ---------------- ANALYTICS ----------------
if not hist.empty:
    anomaly = detect_anomaly(hist["ml_prediction"])
    drift = detect_drift(hist["ml_prediction"])
else:
    anomaly = drift = False

# ================= DASHBOARD =================
col1, col2 = st.columns([2, 1])

# ---------------- LEFT ----------------
with col1:
    st.subheader("📈 ML vs Physics NOx")

    if not hist.empty:
        st.line_chart(
            hist.set_index("time")[["ml_prediction", "physics_prediction"]]
        )

    st.subheader("📉 Residual Error")
    if not hist.empty:
        st.line_chart(hist.set_index("time")["residual"])

# ---------------- RIGHT ----------------
with col2:
    st.subheader("🤖 AI Decision")

    if not hist.empty:
        latest = hist.iloc[-1]

        st.metric("ML NOx", f"{latest['ml_prediction']:.2f}")
        st.metric("Physics NOx", f"{latest['physics_prediction']:.2f}")
        st.metric("Residual", f"{latest['residual']:.2f}")

        st.markdown(f"<h2 class='{classify(latest['ml_prediction'])[1]}'>{latest['status']}</h2>", unsafe_allow_html=True)

        if anomaly:
            st.error("🚨 Anomaly")
        if drift:
            st.warning("⚠ Drift")

# ---------------- AUTO REFRESH ----------------
time.sleep(1)
st.rerun()
