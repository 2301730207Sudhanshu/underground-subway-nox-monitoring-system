import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sqlite3
from datetime import datetime
import time

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
        return pickle.load(open("nox_rf_model.pkl", "rb"))
    except Exception as e:
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
    conn.commit()
    return conn

conn = init_db()

# ---------------- SENSOR ENGINE ----------------
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

# ---------------- CLASSIFICATION ----------------
def classify(val):
    if val < 40:
        return "SAFE", "status-safe"
    elif val < 80:
        return "MODERATE", "status-mod"
    else:
        return "UNSAFE", "status-unsafe"

# ---------------- SAVE DATA ----------------
def save_reading(prediction, status):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO readings VALUES (?, ?, ?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prediction, status)
    )
    conn.commit()

# ---------------- LOAD HISTORY ----------------
def load_history():
    try:
        df = pd.read_sql(
            "SELECT * FROM readings ORDER BY time DESC LIMIT 100",
            conn
        )
        return df[::-1]  # reverse for proper timeline
    except:
        return pd.DataFrame(columns=["time", "prediction", "status"])

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙ Control Panel")
refresh_rate = st.sidebar.slider("Refresh Rate (sec)", 1, 10, 3)
simulate = st.sidebar.toggle("Simulate Sensor Data", True)

# ---------------- MAIN LOGIC ----------------
if simulate:
    sensor = generate_sensor_data()
else:
    sensor = {k: 0 for k in [
        "no", "no2", "relativehumidity", "temperature",
        "wind_direction", "wind_speed",
        "hour", "day", "weekday", "month"
    ]}

df_input = pd.DataFrame([sensor])

# Prediction
try:
    prediction = float(model.predict(df_input)[0])
except:
    prediction = 0.0

status, css = classify(prediction)

# Save
save_reading(prediction, status)

# Load history
hist = load_history()

# ================= DASHBOARD =================
col1, col2 = st.columns([2, 1])

# ---------------- LEFT ----------------
with col1:
    st.subheader("🎮 Sensor Control Panel")

    sensor_df = pd.DataFrame(sensor.items(), columns=["Sensor", "Value"])
    st.dataframe(sensor_df, use_container_width=True)

    st.subheader("📈 Live NOx Trend")

    if not hist.empty:
        st.line_chart(hist.set_index("time")["prediction"])
    else:
        st.info("No data yet...")

# ---------------- RIGHT ----------------
with col2:
    st.subheader("🤖 AI Decision Engine")

    st.metric("Predicted NOx", f"{prediction:.2f}")
    st.markdown(f"<h2 class='{css}'>{status}</h2>", unsafe_allow_html=True)

    if status == "UNSAFE":
        st.error("🚨 CRITICAL POLLUTION ALERT")
    elif status == "MODERATE":
        st.warning("⚠ MODERATE POLLUTION")
    else:
        st.success("✅ Air Quality Safe")

    st.subheader("📊 System Stats")

    if not hist.empty:
        avg = hist["prediction"].mean()
        max_val = hist["prediction"].max()

        st.metric("Average NOx", f"{avg:.2f}")
        st.metric("Peak NOx", f"{max_val:.2f}")
    else:
        st.write("No stats available")

# ---------------- AUTO REFRESH ----------------
time.sleep(refresh_rate)
st.rerun()
