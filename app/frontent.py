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
    ALERT_COOLDOWN = 10

# ================= LOGGING =================
logging.basicConfig(filename="app.log", level=logging.INFO)

# ================= UI =================
st.set_page_config(page_title="NOx AI Control Center v11", layout="wide")

st.markdown("""
<style>
.big {font-size:40px; font-weight:700;}
.safe {color:#00ff9c;}
.mod {color:orange;}
.unsafe {color:red;}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big">⚡ NOx AI Control Center v11 (Final System)</p>', unsafe_allow_html=True)

# ================= LOAD MODEL =================
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

# ================= PHYSICS MODEL =================
def physics(s):
    return 0.5*s["no"] + 0.3*s["no2"] - 0.2*s["wind_speed"] + 0.1*s["temperature"]

# ================= PREDICTION SERVICE =================
class PredictionService:

    @staticmethod
    def validate(sensor):
        for v in sensor.values():
            if isinstance(v, (int,float)):
                if np.isnan(v) or np.isinf(v):
                    return False
        return True

    @staticmethod
    def predict(sensor):
        if not PredictionService.validate(sensor):
            return None

        df = pd.DataFrame([sensor])
        ml = float(model.predict(df)[0])
        phy = physics(sensor)
        residual = abs(ml - phy)

        return ml, phy, residual

# ================= CLASSIFICATION =================
def classify(v):
    if v < Config.SAFE:
        return "SAFE","safe"
    elif v < Config.MODERATE:
        return "MOD","mod"
    return "UNSAFE","unsafe"

# ================= ANALYTICS =================
def ema(series, alpha=0.3):
    return series.ewm(alpha=alpha).mean()

def anomaly(series):
    if len(series)<10: return False
    z=(series.iloc[-1]-series.mean())/(series.std() or 1)
    return abs(z)>Config.ANOMALY_Z

def drift(series):
    if len(series)<20: return False
    return abs(series.iloc[-1]-series.mean())>Config.DRIFT_THRESHOLD

def confidence(ml, phy):
    return max(0, 100 - abs(ml-phy))

def health(anom, drift_flag, conf):
    score = conf
    if anom: score -= 30
    if drift_flag: score -= 20
    return max(0, min(100, score))

# ================= ALERT SYSTEM =================
if "last_alert" not in st.session_state:
    st.session_state.last_alert = 0

def alert_score(residual, anomaly_flag, drift_flag):
    score = residual
    if anomaly_flag: score += 30
    if drift_flag: score += 20
    return score

def alert_label(score):
    if score > 80: return "CRITICAL"
    elif score > 40: return "WARNING"
    return "NORMAL"

# ================= EXPLAINABILITY =================
def feature_importance(sensor):
    return {
        "NO": sensor["no"] * 0.5,
        "NO2": sensor["no2"] * 0.3,
        "Wind": -sensor["wind_speed"] * 0.2,
        "Temp": sensor["temperature"] * 0.1
    }

# ================= MAIN LOOP =================
refresh = st.sidebar.slider("Refresh",1,10,2)

s = sensor()

result = PredictionService.predict(s)

if result:
    ml, phy, res = result
else:
    st.error("Invalid sensor data")
    st.stop()

status, css = classify(ml)

hist = load()

anom = anomaly(hist["ml"]) if not hist.empty else False
drift_flag = drift(hist["ml"]) if not hist.empty else False

score = alert_score(res, anom, drift_flag)
alert = alert_label(score)

save((datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ml, phy, res, status, alert))

hist = load()

if not hist.empty:
    hist["ema"] = ema(hist["ml"])
    conf = confidence(hist.iloc[-1]["ml"], hist.iloc[-1]["physics"])
    health_score = health(anom, drift_flag, conf)
else:
    conf = health_score = 0

# ================= DASHBOARD =================
col1,col2 = st.columns([2,1])

with col1:
    st.subheader("📈 Real-time NOx Monitoring")
    if not hist.empty:
        st.line_chart(hist.set_index("time")[["ml","physics","ema"]])

    st.subheader("📉 Residual Error")
    if not hist.empty:
        st.line_chart(hist.set_index("time")["residual"])

    st.subheader("🧠 Feature Contribution")
    st.bar_chart(pd.Series(feature_importance(s)))

with col2:
    st.subheader("🤖 AI Decision Engine")

    if not hist.empty:
        latest = hist.iloc[-1]

        st.metric("ML", f"{latest['ml']:.2f}")
        st.metric("Physics", f"{latest['physics']:.2f}")
        st.metric("Residual", f"{latest['residual']:.2f}")
        st.metric("Confidence", f"{conf:.1f}%")
        st.metric("Health", f"{health_score:.1f}/100")

        st.markdown(f"<h2 class='{css}'>{latest['status']}</h2>", unsafe_allow_html=True)

        if latest["alert"] == "CRITICAL":
            st.error("🚨 CRITICAL ALERT")
        elif latest["alert"] == "WARNING":
            st.warning("⚠ WARNING")

        if anom:
            st.error("🚨 Anomaly Detected")
        if drift_flag:
            st.warning("⚠ Drift Detected")

# ================= AUTO REFRESH =================
time.sleep(refresh)
st.rerun()
