# 📘 Project Progress Log  
## Underground Subway NOx Monitoring System  

This file records daily development updates.

---

### Day 1  
Studied NOx pollution sources in underground subway tunnels. Reviewed environmental factors affecting tunnel air quality. Outlined possible dataset features for NOx prediction. Planned project folder structure for ML pipeline.

### Day 2  
Explored research papers on subway air pollution and NOx estimation. Identified key variables such as ventilation rate, tunnel geometry, and train frequency.

### Day 3  
Learned about OpenAQ API and its data structure. Tested API calls and explored available pollutant datasets.

### Day 4  
Collected sample air quality data using OpenAQ. Performed initial inspection and cleaning of raw data.

### Day 5  
Researched time-series data handling techniques. Understood challenges in multi-frequency data synchronization.

### Day 6  
Implemented basic data preprocessing pipeline using Pandas. Handled missing values and time alignment.

### Day 7  
Studied subway tunnel physics and ventilation principles. Understood mass balance equation.

### Day 8  
Derived basic formula for NOx concentration estimation using physical laws.

### Day 9  
Explored proxy features for unavailable subway data (train frequency, passenger load).

### Day 10  
Created synthetic dataset combining environmental and proxy features.

---

### Day 11  
Performed exploratory data analysis (EDA) on dataset. Identified correlations between variables.

### Day 12  
Visualized trends in pollutant concentration using matplotlib.

### Day 13  
Studied machine learning models for regression tasks.

### Day 14  
Implemented baseline Linear Regression model.

### Day 15  
Evaluated model performance using MSE and R² score.

### Day 16  
Improved dataset by feature engineering.

### Day 17  
Implemented Random Forest model.

### Day 18  
Compared multiple ML models for performance benchmarking.

### Day 19  
Learned about neural networks and deep learning basics.

### Day 20  
Built first simple neural network using TensorFlow.

---

### Day 21  
Studied Physics-Informed Machine Learning (PIML) concepts.

### Day 22  
Understood Physics-Informed Neural Networks (PINNs).

### Day 23  
Designed hybrid feature space (ML + physics features).

### Day 24  
Implemented custom loss function combining MSE and physics constraint.

### Day 25  
Trained PIML model on dataset.

### Day 26  
Analyzed model predictions and physical consistency.

### Day 27  
Fine-tuned hyperparameters for improved accuracy.

### Day 28  
Validated model against physical constraints.

### Day 29  
Improved model stability and generalization.

### Day 30  
Documented PIML model design.

---

### Day 31  
Studied SHAP for model interpretability.

### Day 32  
Implemented SHAP for feature importance analysis.

### Day 33  
Analyzed impact of ventilation and outdoor pollution.

### Day 34  
Learned about LIME for local explanations.

### Day 35  
Applied LIME to explain specific prediction cases.

### Day 36  
Designed safety threshold system using NAAQS standards.

### Day 37  
Implemented alert mechanism for high NOx levels.

### Day 38  
Tested explainability outputs with sample data.

### Day 39  
Improved interpretability visualization.

### Day 40  
Documented explainability module.

---

### Day 41  
Started backend development using FastAPI.

### Day 42  
Created API endpoints for prediction requests.

### Day 43  
Integrated trained model into backend service.

### Day 44  
Tested API performance and response time.

### Day 45  
Implemented asynchronous request handling.

### Day 46  
Designed database schema for time-series data.

### Day 47  
Set up PostgreSQL / TimescaleDB.

### Day 48  
Integrated backend with database.

### Day 49  
Stored prediction and historical data.

### Day 50  
Optimized database queries.

---

### Day 51  
Started frontend development using React.

### Day 52  
Designed UI layout for dashboard.

### Day 53  
Implemented data visualization components.

### Day 54  
Created real-time NOx heatmap visualization.

### Day 55  
Added forecasting graphs for 24-hour prediction.

### Day 56  
Connected frontend with backend API.

### Day 57  
Tested full system integration.

### Day 58  
Performed debugging and performance improvements.

### Day 59  
Prepared documentation and GitHub repository.

### Day 60  
Final review of system architecture, testing, and deployment readiness.

---

## ✅ Summary

- Built a complete **Physics-Informed ML pipeline**
- Integrated **data ingestion, modeling, explainability, and visualization**
- Developed a **full-stack system for NOx monitoring**
- Ensured **real-time prediction + physical consistency**

---
