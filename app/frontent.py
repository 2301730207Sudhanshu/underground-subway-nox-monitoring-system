import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sqlite3
from datetime import datetime
import time
import logging

# ---------------- CONFIG ----------------
CONFIG = {
    "SAFE": 40,
    "MODERATE": 80,
    "ANOMALY_THRESHOLD": 2.0
}

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

st.markdown('<p class="big-font">⚡ AI NOx Control Center (v5)</p>', unsafe_allow_html=True)

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
        time TEXT PRIMARY KEY,
        prediction REAL,
        status TEXT
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

# ---------------- CLASSIFICATION ----------------
def classify(val):
    if val < CONFIG["SAFE"]:
        return "SAFE", "status-safe"
    elif val < CONFIG["MODERATE"]:
        return "MODERATE", "status-mod"
    else:
        return "UNSAFE", "status-unsafe"

# ---------------- ANOMALY DETECTION ----------------
def detect_anomaly(series):
    if len(series) < 10:
        return False
    mean = series.mean()
    std = series.std()
    latest = series.iloc[-1]
    z_score = (latest - mean) / std if std != 0 else 0
    return abs(z_score) > CONFIG["ANOMALY_THRESHOLD"]

# ---------------- TREND ----------------
def get_trend(series):
    if len(series) < 5:
        return "→ Stable"
    if series.iloc[-1] > series.iloc[-5]:
        return "📈 Rising"
    elif series.iloc[-1] < series.iloc[-5]:
        return "📉 Falling"
    return "→ Stable"

# ---------------- SAVE ----------------
def save_reading(prediction, status):
    try:
        conn.execute(
            "INSERT INTO readings VALUES (?, ?, ?)",
            (datetime.now().strftime("%Y-%m-%d %H:%M:%S"), prediction, status)
        )
        conn.commit()
    except:
        pass

# ---------------- LOAD ----------------
def load_history():
    df = pd.read_sql("SELECT * FROM readings ORDER BY time DESC LIMIT 300", conn)
    return df[::-1]

# ---------------- SIDEBAR ----------------
st.sidebar.header("⚙ Control Panel")
refresh_rate = st.sidebar.slider("Refresh Rate", 1, 10, 3)

# ---------------- MAIN ----------------
sensor = generate_sensor_data()
df_input = pd.DataFrame([sensor])

prediction = float(model.predict(df_input)[0])
status, css = classify(prediction)

save_reading(prediction, status)

hist = load_history()

# Analytics
if not hist.empty:
    hist["rolling"] = hist["prediction"].rolling(5).mean()
    anomaly = detect_anomaly(hist["prediction"])
    trend = get_trend(hist["prediction"])
else:
    anomaly = False
    trend = "N/A"

# ================= DASHBOARD =================
col1, col2 = st.columns([2, 1])

# ---------------- LEFT ----------------
with col1:
    st.subheader("📈 NOx Trend")

    if not hist.empty:
        st.line_chart(hist.set_index("time")[["prediction", "rolling"]])

    # Feature Importance
    if hasattr(model, "feature_importances_"):
        importance = pd.DataFrame({
            "Feature": df_input.columns,
            "Importance": model.feature_importances_
        }).sort_values(by="Importance", ascending=False)

        st.subheader("🧠 Feature Importance")
        st.bar_chart(importance.set_index("Feature"))

# ---------------- RIGHT ----------------
with col2:
    st.subheader("🤖 AI Decision")

    st.metric("NOx", f"{prediction:.2f}")
    st.markdown(f"<h2 class='{css}'>{status}</h2>", unsafe_allow_html=True)

    st.metric("Trend", trend)

    if anomaly:
        st.error("🚨 Anomaly Detected!")

    st.subheader("📊 Stats")
    if not hist.empty:
        st.metric("Avg", f"{hist['prediction'].mean():.2f}")
        st.metric("Max", f"{hist['prediction'].max():.2f}")
        st.metric("Records", len(hist))

# ---------------- AUTO REFRESH ----------------
time.sleep(refresh_rate)
st.rerun()
