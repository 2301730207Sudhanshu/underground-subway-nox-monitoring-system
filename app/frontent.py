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
    return pickle.load(open("nox_rf_model.pkl", "rb"))

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

# ---------------- AUTO REFRESH ----------------
refresh_rate = st.sidebar.slider("Refresh Rate (seconds)", 1, 10, 3)

# ---------------- MAIN APP ----------------
sensor = generate_sensor_data()
df_input = pd.DataFrame([sensor])

prediction = model.predict(df_input)[0]
status, css = classify(prediction)

# Save to DB
cursor = conn.cursor()
cursor.execute(
    "INSERT INTO readings VALUES (?, ?, ?)",
    (datetime.now(), prediction, status)
)
conn.commit()

# Load history
hist = pd.read_sql("SELECT * FROM readings ORDER BY time DESC LIMIT 100", conn)

# ================= DASHBOARD =================
col1, col2 = st.columns([2, 1])

# ---------------- LEFT PANEL ----------------
with col1:
    st.subheader("🎮 Sensor Control Panel")

    sensor_df = pd.DataFrame(sensor.items(), columns=["Sensor", "Value"])
    st.dataframe(sensor_df, use_container_width=True)

    st.subheader("📈 Live NOx Trend")
    st.line_chart(hist["prediction"])

# ---------------- RIGHT PANEL ----------------
with col2:
    st.subheader("🤖 AI Decision Engine")

    st.metric("Predicted NOx", f"{prediction:.2f}")
    st.markdown(f"<h2 class='{css}'>{status}</h2>", unsafe_allow_html=True)

    if status == "UNSAFE":
        st.error("🚨 CRITICAL POLLUTION ALERT")
    elif status == "MODERATE":
        st.warning("⚠ MODERATE POLLUTION")

    st.subheader("📊 System Stats")

    avg = hist["prediction"].mean()
    max_val = hist["prediction"].max()

    st.metric("Average NOx", f"{avg:.2f}")
    st.metric("Peak NOx", f"{max_val:.2f}")

# ---------------- AUTO REFRESH ----------------
time.sleep(refresh_rate)
st.rerun()
