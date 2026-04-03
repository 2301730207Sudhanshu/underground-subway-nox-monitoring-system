# 🏛️ Physics-Informed NOx Monitoring System (Delhi Metro)

## 📌 Overview

This project presents a **Modular Physics-Informed Machine Learning (PIML) Pipeline** designed for estimating and monitoring NOx levels in underground subway environments such as the Delhi Metro.

The system integrates **data engineering, physics-based modeling, and full-stack visualization** into decoupled microservices for scalability and real-time performance.

---

## 🧩 System Architecture

### 1. Data Ingestion & Orchestration Layer

This layer handles heterogeneous and asynchronous data sources:

- **External API Integration**
  - Fetches ambient air quality data from OpenAQ
  - Establishes outdoor pollution baseline

- **Subway Proxy Metrics**
  - Train frequency
  - Station depth
  - Estimated passenger load

- **Data Synchronizer**
  - Aligns multi-frequency data streams
  - Uses time-series resampling techniques

---

### 2. Physics-Informed ML (PIML) Core

The core intelligence of the system combining ML with physics constraints.

#### Hybrid Feature Space

- Environmental Features:
  - Temperature, Humidity, Traffic

- Physical Parameters:
  - Tunnel Diameter
  - Ventilation Fan Capacity (m³/s)

#### Physics-Constrained Loss Function
Loss = MSE_pred + α × Physics_Violation


- Ensures adherence to **Conservation of Mass**
- Penalizes physically inconsistent predictions

#### Model Options

- Physics-Informed Neural Networks (PINNs)
- Ensemble Models with chemical decay constraints

---

### 3. Explainability & Risk Assessment Module

Enhances transparency and decision-making:

- **SHAP Analysis**
  - Global feature importance

- **LIME**
  - Local explanations for pollution spikes

- **Safety Thresholding**
  - Compares predictions against NAAQS standards
  - Generates health alerts

---

### 4. Full-Stack Delivery Layer

#### Backend (FastAPI)

- High-performance API
- <100ms inference latency
- Asynchronous request handling

#### Database (TimescaleDB / PostgreSQL)

- Time-series optimized storage
- Supports historical and seasonal analysis

#### Frontend (React.js)

- Interactive dashboards
- Live NOx heatmaps
- 24-hour predictive forecasting

---

## 🛠️ Tech Stack

| Segment            | Technology                     | Purpose                          |
|-------------------|------------------------------|----------------------------------|
| Data Science      | Pandas, NumPy, Scikit-learn  | Data processing & baseline ML     |
| PIML Core         | PyTorch / TensorFlow         | Custom physics-based modeling     |
| Database          | PostgreSQL / InfluxDB        | Time-series data storage          |
| Explainability    | SHAP, LIME                  | Model interpretability            |
| Backend API       | FastAPI + Uvicorn            | High-performance inference API    |
| Frontend          | React, Tailwind, D3.js       | Visualization dashboard           |
| DevOps            | Docker, GitHub Actions       | CI/CD and deployment              |

---

## 🔄 Process Flow

1. **Ingest Data**
   - AQI data + tunnel metadata

2. **Apply Physical Constraint**
   - Mass balance equation:
     ```
     C = E / V
     ```

3. **Train / Predict**
   - Execute PIML model

4. **Validate**
   - Ensure predictions obey physical laws

5. **Serve**
   - Display insights via web dashboard

---

## 🎯 Key Contributions

- Integration of **Physics + Machine Learning**
- Real-time NOx prediction in underground tunnels
- Explainable AI for environmental monitoring
- Scalable microservice-based architecture

---

## 🚀 Future Scope

- Integration with real-time metro sensor data
- Reinforcement learning for ventilation optimization
- Multi-city deployment

---

## 📎 Data Sources

- OpenAQ API: https://openaq.org/

---

## 👨‍💻 Author

Sudhanshu Ranjan Singh
