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
model = pickle.load(open("nox_rf_model.pkl", "rb"))

# ---------------- DATABASE ----------------
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

# ---------------- SENSOR ENGINE ----------------
def generate_sensor_data():
    now = datetime.now()

    data = {
        "no": np.random.uniform(10,200),
        "no2": np.random.uniform(10,200),
        "relativehumidity": np.random.uniform(30,90),
        "temperature": np.random.uniform(20,50),
        "wind_direction": np.random.uniform(0,360),
        "wind_speed": np.random.uniform(0,10),
        "hour": now.hour,
        "day": now.day,
        "weekday": now.weekday(),
        "month": now.month
    }

    return data

# ---------------- CLASSIFICATION ----------------
def classify(val):
    if val < 40:
        return "SAFE", "status-safe"
    elif val < 80:
        return "MODERATE", "status-mod"
    else:
        return "UNSAFE", "status-unsafe"

# ---------------- LIVE LOOP ----------------
placeholder = st.empty()

while True:
    with placeholder.container():

        # Generate sensors
        sensor = generate_sensor_data()
        df_input = pd.DataFrame([sensor])

        # Model prediction
        prediction = model.predict(df_input)[0]
        status, css = classify(prediction)

        # Save to DB
        c.execute("INSERT INTO readings VALUES (?, ?, ?)",
                  (datetime.now(), prediction, status))
        conn.commit()

        # ================= DASHBOARD LAYOUT =================
        col1, col2 = st.columns([2,1])

        # ---------------- LEFT PANEL ----------------
        with col1:

            st.subheader("🎮 Sensor Control Panel")

            sensor_df = pd.DataFrame(sensor.items(), columns=["Sensor", "Value"])
            st.dataframe(sensor_df, use_container_width=True)

            st.subheader("📈 Live NOx Trend")

            hist = pd.read_sql("SELECT * FROM readings ORDER BY time DESC LIMIT 100", conn)
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

    time.sleep(3)
