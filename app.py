import streamlit as st
import pickle
import numpy as np
import pandas as pd
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

st.set_page_config(layout="wide")
st.title("🚇 Real-Time NOx Monitoring System")

model = pickle.load(open("nox_rf_model.pkl","rb"))

st_autorefresh(interval=2000)

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

df = pd.DataFrame([data])

prediction = model.predict(df)[0]

status = "SAFE" if prediction < 200 else "UNSAFE"

col1,col2,col3,col4 = st.columns(4)
col1.metric("NO",round(data["no"],2))
col2.metric("NO2",round(data["no2"],2))
col3.metric("Temp",round(data["temperature"],2))
col4.metric("Predicted NOx",round(prediction,2))

if status=="UNSAFE":
    st.error("🚨 HIGH NOx ALERT")
else:
    st.success("Air Quality Normal")

if "history" not in st.session_state:
    st.session_state.history=[]

st.session_state.history.append(prediction)

chart_data=pd.DataFrame(st.session_state.history,columns=["NOx"])
st.line_chart(chart_data)
