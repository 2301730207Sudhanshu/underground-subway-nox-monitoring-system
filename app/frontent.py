import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sqlite3
from datetime import datetime
import time
import logging

# ---------------- LOGGING ----------------
logging.basicConfig(level=logging.INFO)

# ---------------- CONFIG ----------------
st.set_page_config(page_title="NOx AI Control Center", layout="wide")

st.markdown("""
<style>
.big-font {font-size:40px !important; font-weight:700;}
.status-safe {color: #00ff9c; font-weight:bold;}
.status-mod {color: orange; font-weight:bold;}
.status-unsafe {color: red; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">⚡ AI NOx Control Center</p>', unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model():
    try:
        model = pickle.load(open("nox_rf_model.pkl", "rb"))
        logging.info("Model loaded successfully")
        return model
    except Exception as e:
        logging.error("Model loading failed")
        st.error("❌ Model loading failed")
        st.stop()

model = load_model()

# ---------------- DATABASE ----------------
@st.cache_resource
def init_db():
    conn = sqlite3.connect("nox_data.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS readings(
        time TEXT,
        prediction REAL,
        status TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS alerts(
        time TEXT,
        level TEXT
    )
    """)

    conn.commit()
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

# ---------------- VALIDATION ----------------
def validate_input(data):
    for key, val in data.items():
        if val is None or np.isnan(val):
            return False
    return True

# ---------------- CLASSIFY ----------------
def classify(val):
    if val < 40:
        return "SAFE", "status-safe"
    elif val < 80:
        return "MODERATE", "status-mod"
    else:
        return "UNSAFE", "status-unsafe"

# ---------------- DB OPS ----------------
def save_reading(prediction, status):
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("INSERT INTO readings VALUES (?, ?, ?)", (now, prediction, status))

    if status == "UNSAFE":
        cursor.execute("INSERT INTO alerts VALUES (?, ?)", (now, status))

    conn.commit()

def load_history():
    df = pd.read_sql("SELECT * FROM readings ORDER BY time DESC LIMIT 300", conn)
    return df[::-1]

def load_alerts():
    return pd.read_sql("SELECT * FROM alerts ORDER BY time DESC LIMIT 50", conn)

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙ Control Panel")

refresh_rate = st.sidebar.slider("Refresh Rate (sec)", 1, 10, 3)
simulate = st.sidebar.toggle("Simulate Sensor", True)

# ---------------- SESSION CONTROL ----------------
if "last_run" not in st.session_state:
    st.session_state.last_run = 0

current_time = time.time()

run_prediction = False
if current_time - st.session_state.last_run > refresh_rate:
    run_prediction = True
    st.session_state.last_run = current_time

# ---------------- MAIN ----------------
if run_prediction:

    sensor = generate_sensor_data() if simulate else {}

    if validate_input(sensor):
        df_input = pd.DataFrame([sensor])

        try:
            prediction = float(model.predict(df_input)[0])
        except:
            prediction = 0.0
            logging.warning("Prediction failed")

        status, css = classify(prediction)

        save_reading(prediction, status)

# Load data
hist = load_history()
alerts = load_alerts()

# Add smoothing (rolling mean)
if not hist.empty:
    hist["smoothed"] = hist["prediction"].rolling(window=5).mean()

# ================= DASHBOARD =================
col1, col2 = st.columns([2, 1])

# ---------------- LEFT ----------------
with col1:
    st.subheader("📈 NOx Trend (Raw vs Smoothed)")

    if not hist.empty:
        st.line_chart(hist.set_index("time")[["prediction", "smoothed"]])
    else:
        st.info("No data available")

# ---------------- RIGHT ----------------
with col2:
    st.subheader("🤖 AI Decision Engine")

    if not hist.empty:
        latest = hist.iloc[-1]

        st.metric("NOx", f"{latest['prediction']:.2f}")
        st.markdown(f"<h2 class='{classify(latest['prediction'])[1]}'>{latest['status']}</h2>", unsafe_allow_html=True)

        if latest["status"] == "UNSAFE":
            st.error("🚨 CRITICAL ALERT")
        elif latest["status"] == "MODERATE":
            st.warning("⚠ MODERATE")
        else:
            st.success("✅ SAFE")

        st.subheader("📊 Insights")

        st.metric("Avg", f"{hist['prediction'].mean():.2f}")
        st.metric("Peak", f"{hist['prediction'].max():.2f}")
        st.metric("Alerts", len(alerts))

# ---------------- ALERT PANEL ----------------
st.subheader("🚨 Alert History")

if not alerts.empty:
    st.dataframe(alerts, use_container_width=True)
else:
    st.info("No alerts triggered")

# ---------------- AUTO REFRESH ----------------
time.sleep(1)
st.rerun()
