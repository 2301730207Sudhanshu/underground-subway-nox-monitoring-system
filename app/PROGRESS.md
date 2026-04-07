🔥 NOx AI Control Center v4 (Industry + Research Grade)

- Added logging system for monitoring
- Implemented input validation
- Added alert tracking system
- Introduced rolling average smoothing
- Improved performance & architecture
- Enhanced real-time analytics dashboard
🔥 NOx AI Control Center v5 (Final Boss)

- Added anomaly detection (Z-score based)
- Implemented trend analysis (rising/falling)
- Integrated feature importance visualization
- Config-driven classification thresholds
- Improved database reliability
- Upgraded to research-grade AI monitoring system

🚀 NOx AI Control Center v6 (Ultimate Production System)

- Added drift detection for model reliability
- Implemented confidence scoring
- Improved anomaly detection using Z-score
- Added session-controlled execution
- Enhanced analytics and monitoring features
- Upgraded to production-grade AI system

- 🔥 NOx AI Control Center v7 (Hybrid Physics-Informed AI)

- Integrated physics-based NOx estimation
- Added hybrid ML vs Physics comparison
- Implemented residual error tracking
- Improved anomaly & drift detection
- Upgraded to research-grade AI monitoring system

- 🔥 NOx AI Control Center v8 (Ultimate Production System)

- Implemented adaptive thresholding
- Added stability scoring metric
- Integrated hybrid ML + Physics model
- Improved anomaly and drift detection
- Environment-based configuration support
- Fully production-ready AI monitoring system

🚀 NOx AI Control Center v9 (Enterprise AI Platform)

- Implemented hybrid ML + Physics system
- Added adaptive thresholds and health scoring
- Integrated anomaly and drift detection
- Improved DB reliability with retry logic
- Designed layered architecture for scalability
- Fully production-ready AI monitoring platform

- # ⚡ NOx AI Control Center (v10 - Real-Time Intelligent Monitoring System)

## 🚀 Overview
The **NOx AI Control Center** is a real-time, hybrid AI-based monitoring system designed for predicting and analyzing Nitrogen Oxides (NOx) levels in underground subway environments.

It combines:
- 🤖 Machine Learning (Random Forest Model)
- ⚙ Physics-Based Modeling
- 📡 Real-Time Streaming Simulation
- 🚨 Intelligent Alert System

This system ensures **high reliability, explainability, and robustness** in dynamic environmental conditions.

---

## 🧠 Key Features

### 🔥 AI + Physics Hybrid System
- ML model predicts NOx levels
- Physics model validates predictions
- Residual error ensures trustworthiness

### ⚡ Real-Time Streaming
- Continuous sensor simulation
- Sliding window processing
- EMA smoothing for stable trends

### 🚨 Smart Alerting
- Multi-level alerts (Normal, Warning, Critical)
- Cooldown mechanism to prevent alert spam

### 📊 Advanced Analytics
- Anomaly detection (Z-score based)
- Drift detection (distribution shift)
- Confidence score (ML vs Physics agreement)
- Health score (system reliability)

### 💾 Persistent Storage
- SQLite database for historical tracking
- Stores predictions, residuals, alerts

---

## 🏗️ System Architecture
# 🔄 v11 Update – Changes Only

## 🧠 Architecture Upgrade
- Introduced **PredictionService layer**
- Separated ML + Physics logic from UI
- Made system **API-ready (FastAPI integration possible)**

---

## ✅ Data Validation
- Added input validation for sensor data
- Prevents NaN / infinite values from entering model
- Improves system reliability

---

## 🤖 Hybrid Prediction Enhancement
- Centralized prediction pipeline:
  - ML prediction
  - Physics prediction
  - Residual calculation
- Cleaner and reusable structure

---

## 🧠 Explainability (NEW)
- Added **feature contribution module**
- Lightweight SHAP-style approximation:
  - NO contribution
  - NO2 contribution
  - Wind effect
  - Temperature effect
- Visualized using bar chart in dashboard

---

## 🚨 Alert System Upgrade
- Replaced simple alerts with **scoring-based alert system**
- Introduced:
  - `alert_score()` → combines residual + anomaly + drift
  - `alert_label()` → maps score → NORMAL / WARNING / CRITICAL
- More intelligent and realistic alerting

---

## 📊 Analytics Improvements
- Integrated alert logic with:
  - Anomaly detection
  - Drift detection
- Better decision-making using combined signals

---

## ⚡ Performance Improvements
- Reduced redundant computations
- Optimized prediction flow using service layer
- Cleaner execution pipeline

---

## 🧩 Code Quality Improvements
- Modular structure (services, analytics, UI separation)
- Improved readability and maintainability
- Easier future extension (API / IoT integration)

---

## 🌐 Deployment Readiness
- System is now:
  - Backend-ready
  - Scalable
  - Suitable for real-world integration

---

## 🎯 Summary
v11 transforms the system into a:
- **Modular AI platform**
- **Explainable hybrid model**
- **Reliable real-time monitoring system**
- **Deployment-ready architecture**

