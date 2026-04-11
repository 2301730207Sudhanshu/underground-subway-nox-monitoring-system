import streamlit as st
import pandas as pd
import numpy as np
import pickle
import sqlite3
import logging
import os
import time
from datetime import datetime

# ================= CONFIGURATION =================
class Config:
    """Centralized configuration for the NOx Control Center."""
    MODEL_PATH = os.getenv("MODEL_PATH", "nox_rf_model.pkl")
    DB_PATH = os.getenv("DB_PATH", "nox_data.db")
    DEFAULT_SAFE = float(os.getenv("SAFE_THRESHOLD", 40))
    DEFAULT_MOD = float(os.getenv("MODERATE_THRESHOLD", 80))
    ANOMALY_Z = 2.5
    DRIFT_THRESHOLD = 20
    LOG_FILE = "app.log"

# ================= LOGGING =================
logging.basicConfig(
    filename=Config.LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================= UI SETUP =================
st.set_page_config(page_title="NOx AI Control Center v13", layout="wide")

st.markdown("""
<style>
    .big {font-size:40px; font-weight:700;}
    .safe {color:#00ff9c;}
    .mod {color:orange;}
    .unsafe {color:red;}
    .banner {padding:15px; border-radius:10px; text-align:center; font-weight:bold; margin-bottom:20px;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big">⚡ NOx AI Control Center v13 (Pro Max)</p>', unsafe_allow_html=True)

# ================= DATA & MODEL LIBRARIES =================
@st.cache_resource
def load_model():
    """Loads the pre-trained Random Forest model."""
    try:
        if os.path.exists(Config.MODEL_PATH):
            return pickle.load(open(Config.MODEL_PATH, "rb"))
        else:
            st.error(f"Model file {Config.MODEL_PATH} not found.")
            return None
    except Exception as e:
        logging.error(f"Error loading model: {e}")
        return None

@st.cache_resource
def init_db():
    """Initializes the SQLite database."""
    conn = sqlite3.connect(Config.DB_PATH, check_same_thread=False)
    conn.execute("""
    CREATE TABLE IF NOT EXISTS readings(
        time TEXT PRIMARY KEY,
        ml REAL,
        physics REAL,
        residual REAL,
        status TEXT,
        alert TEXT
    )
    """)
    return conn

db_conn = init_db()
model = load_model()

def save_reading(row):
    """Saves a single telemetry row to the database."""
    try:
        with db_conn:
            db_conn.execute("INSERT OR REPLACE INTO readings VALUES (?, ?, ?, ?, ?, ?)", row)
    except sqlite3.Error as e:
        logging.error(f"Database error: {e}")

def load_history(limit=300):
    """Retrieves historical data from the database."""
    query = f"SELECT * FROM readings ORDER BY time DESC LIMIT {limit}"
    df = pd.read_sql(query, db_conn)
    return df.iloc[::-1].reset_index(drop=True)

# ================= LOGIC & ANALYTICS =================
def get_sensor_data(manual=False):
    """Generates synthetic or manual sensor data."""
    now = datetime.now()
    if manual:
        return {
            "no": st.sidebar.slider("NO", 0.0, 300.0, 50.0),
            "no2": st.sidebar.slider("NO2", 0.0, 300.0, 40.0),
            "relativehumidity": st.sidebar.slider("Humidity", 0.0, 100.0, 50.0),
            "temperature": st.sidebar.slider("Temp", 0.0, 60.0, 30.0),
            "wind_direction": st.sidebar.slider("Wind Dir", 0.0, 360.0, 180.0),
            "wind_speed": st.sidebar.slider("Wind Speed", 0.0, 20.0, 5.0),
            "hour": now.hour, "day": now.day, "weekday": now.weekday(), "month": now.month
        }
    return {
        "no": np.random.uniform(10, 200),
        "no2": np.random.uniform(10, 200),
        "relativehumidity": np.random.uniform(30, 90),
        "temperature": np.random.uniform(20, 50),
        "wind_direction": np.random.uniform(0, 360),
        "wind_speed": np.random.uniform(0, 10),
        "hour": now.hour, "day": now.day, "weekday": now.weekday(), "month": now.month
    }

def physics_model(s):
    """Baseline physics calculation for comparison."""
    return 0.5*s["no"] + 0.3*s["no2"] - 0.2*s["wind_speed"] + 0.1*s["temperature"]

def run_inference(s):
    """Calculates ML prediction and residual."""
    phy = physics_model(s)
    if model:
        df = pd.DataFrame([s])
        ml = float(model.predict(df)[0])
    else:
        ml = phy + np.random.normal(0, 5) # Fallback if model is missing
    
    return ml, phy, abs(ml - phy)

def get_adaptive_thresholds(series):
    if len(series) < 20:
        return Config.DEFAULT_SAFE, Config.DEFAULT_MOD
    return series.mean() - series.std(), series.mean() + series.std()

# ================= SIDEBAR & STATE =================
st.sidebar.header("🕹️ Controls")
manual_mode = st.sidebar.toggle("Manual Mode", False)
refresh_rate = st.sidebar.slider("Refresh Rate (s)", 1, 10, 3)

# ================= MAIN EXECUTION =================
sensor_input = get_sensor_data(manual_mode)
ml_val, phy_val, residual = run_inference(sensor_input)

# Load context for analytics
history_df = load_history()
safe_t, mod_t = get_adaptive_thresholds(history_df["ml"]) if not history_df.empty else (Config.DEFAULT_SAFE, Config.DEFAULT_MOD)

# Classification
if ml_val < safe_t:
    status, css = "SAFE", "safe"
elif ml_val < mod_t:
    status, css = "MODERATE", "mod"
else:
    status, css = "UNSAFE", "unsafe"

# Anomaly detection
is_anomaly = False
if not history_df.empty and len(history_df) > 10:
    z_score = (ml_val - history_df["ml"].mean()) / (history_df["ml"].std() or 1)
    is_anomaly = abs(z_score) > Config.ANOMALY_Z

# Save and Refresh History
save_reading((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ml_val, phy_val, residual, status, "OK"))
history_df = load_history()

# ================= DASHBOARD RENDERING =================
# Status Banner
banner_color = "#00ff9c" if status == "SAFE" else "orange" if status == "MODERATE" else "#ff4b4b"
st.markdown(f"<div class='banner' style='background:{banner_color}; color:black;'>SYSTEM STATUS: {status}</div>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("📈 Real-time NOx Telemetry")
    if not history_df.empty:
        history_df["ema"] = history_df["ml"].ewm(alpha=0.3).mean()
        st.line_chart(history_df.set_index("time")[["ml", "physics", "ema"]])

    st.subheader("📉 Prediction Error (Residual)")
    if not history_df.empty:
        st.area_chart(history_df.set_index("time")["residual"])

with col2:
    st.subheader("🤖 Engine Metrics")
    st.metric("AI Predicted", f"{ml_val:.2f} ppb")
    st.metric("Physics Baseline", f"{phy_val:.2f} ppb")
    st.metric("Residual Delta", f"{residual:.2f}", delta_color="inverse")

    if is_anomaly:
        st.error("🚨 ANOMALY DETECTED")
    
    st.write(f"**Thresholds:**")
    st.caption(f"Safe < {safe_t:.1f} | Mod < {mod_t:.1f}")

# Auto-refresh logic
time.sleep(refresh_rate)
st.rerun()
