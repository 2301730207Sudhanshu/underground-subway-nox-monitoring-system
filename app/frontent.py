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
    DEFAULT_SAFE = float(os.getenv("SAFE_THRESHOLD", 40))
    DEFAULT_MOD = float(os.getenv("MODERATE_THRESHOLD", 80))
    ANOMALY_Z = 2.5
    DRIFT_THRESHOLD = 20

# ================= LOGGING =================
logging.basicConfig(filename="app.log", level=logging.INFO)

# ================= UI =================
st.set_page_config(page_title="NOx AI Control Center v13", layout="wide")

st.markdown("""
<style>
.big {font-size:40px; font-weight:700;}
.safe {color:#00ff9c;}
.mod {color:orange;}
.unsafe {color:red;}
.banner {padding:10px; border-radius:10px; text-align:center; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big">⚡ NOx AI Control Center v13 (Pro Max)</p>', unsafe_allow_html=True)

# ================= MODEL =================
@st.cache_resource
def load_model():
    return pickle.load(open("nox_rf_model.pkl", "rb"))

model = load_model()

# ================= DATABASE =================
@st.cache_resource
def init_db():
    conn = sqlite3.connect("nox_data.db", check_same_thread=False)
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

conn = init_db()

def save(row):
    try:
        conn.execute("INSERT INTO readings VALUES (?, ?, ?, ?, ?, ?)", row)
        conn.commit()
    except:
        pass

def load():
    df = pd.read_sql("SELECT * FROM readings ORDER BY time DESC LIMIT 300", conn)
    return df[::-1]

# ================= SIDEBAR =================
st.sidebar.subheader("⚙ Controls")

manual_mode = st.sidebar.toggle("Manual Mode", False)
refresh = st.sidebar.slider("Refresh",1,10,2)

# ================= SENSOR =================
def sensor():
    now = datetime.now()
    return {
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

def manual_sensor():
    return {
        "no": st.sidebar.slider("NO",0.0,300.0,50.0),
        "no2": st.sidebar.slider("NO2",0.0,300.0,40.0),
        "relativehumidity": st.sidebar.slider("Humidity",0.0,100.0,50.0),
        "temperature": st.sidebar.slider("Temp",0.0,60.0,30.0),
        "wind_direction": st.sidebar.slider("Wind Dir",0.0,360.0,180.0),
        "wind_speed": st.sidebar.slider("Wind Speed",0.0,20.0,5.0),
        "hour": datetime.now().hour,
        "day": datetime.now().day,
        "weekday": datetime.now().weekday(),
        "month": datetime.now().month
    }

s = manual_sensor() if manual_mode else sensor()

# ================= MODELS =================
def physics(s):
    return 0.5*s["no"] + 0.3*s["no2"] - 0.2*s["wind_speed"] + 0.1*s["temperature"]

def predict(s):
    df = pd.DataFrame([s])
    ml = float(model.predict(df)[0])
    phy = physics(s)
    res = abs(ml - phy)
    return ml, phy, res

# ================= ANALYTICS =================
def adaptive_thresholds(series):
    if len(series) < 20:
        return Config.DEFAULT_SAFE, Config.DEFAULT_MOD
    mean = series.mean()
    std = series.std()
    return mean - std, mean + std

def classify(v, safe, mod):
    if v < safe:
        return "SAFE","safe"
    elif v < mod:
        return "MOD","mod"
    return "UNSAFE","unsafe"

def anomaly(series):
    if len(series) < 10: return False
    z = (series.iloc[-1] - series.mean()) / (series.std() or 1)
    return abs(z) > Config.ANOMALY_Z

def drift(series):
    if len(series) < 20: return False
    return abs(series.iloc[-1] - series.mean()) > Config.DRIFT_THRESHOLD

def ema(series):
    return series.ewm(alpha=0.3).mean()

# ================= MAIN =================
ml, phy, res = predict(s)

hist = load()

safe_t, mod_t = adaptive_thresholds(hist["ml"]) if not hist.empty else (Config.DEFAULT_SAFE, Config.DEFAULT_MOD)

status, css = classify(ml, safe_t, mod_t)

anom = anomaly(hist["ml"]) if not hist.empty else False
drift_flag = drift(hist["ml"]) if not hist.empty else False

save((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ml, phy, res, status, "OK"))

hist = load()

if not hist.empty:
    hist["ema"] = ema(hist["ml"])

# ================= STATUS BANNER =================
color = "#00ff9c" if status=="SAFE" else "orange" if status=="MOD" else "red"
st.markdown(f"<div class='banner' style='background:{color}'>SYSTEM STATUS: {status}</div>", unsafe_allow_html=True)

st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

# ================= DASHBOARD =================
col1,col2 = st.columns([2,1])

with col1:
    st.subheader("📈 NOx Trends")
    if not hist.empty:
        st.line_chart(hist.set_index("time")[["ml","physics","ema"]])

    st.subheader("📉 Residual")
    if not hist.empty:
        st.line_chart(hist.set_index("time")["residual"])

with col2:
    st.subheader("🤖 AI Engine")

    st.metric("ML", f"{ml:.2f}")
    st.metric("Physics", f"{phy:.2f}")
    st.metric("Residual", f"{res:.2f}")

    st.markdown(f"<h2 class='{css}'>{status}</h2>", unsafe_allow_html=True)

    if anom:
        st.error("🚨 Anomaly")
    if drift_flag:
        st.warning("⚠ Drift")

# ================= AUTO REFRESH =================
time.sleep(refresh)
st.rerun()
