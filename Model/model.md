# 🤖 Model Development Log  
## Physics-Informed NOx Prediction Model  

This document records the **day-wise development, experimentation, and optimization** of the machine learning and physics-informed models used in the project.

---

## 🧠 Phase 1: Problem Framing & Baseline Models

### Day 1  
Defined the prediction objective: estimating NOx concentration in subway tunnels.

### Day 2  
Identified input features and target variable.

### Day 3  
Prepared dataset for modeling.

### Day 4  
Split data into training and testing sets.

### Day 5  
Implemented baseline Linear Regression model.

### Day 6  
Evaluated baseline model performance.

### Day 7  
Analyzed limitations of linear models.

### Day 8  
Implemented Decision Tree Regressor.

### Day 9  
Observed overfitting in tree-based models.

### Day 10  
Implemented Random Forest model for improved generalization.

---

## 🌲 Phase 2: Advanced Machine Learning Models

### Day 11  
Tuned Random Forest hyperparameters.

### Day 12  
Implemented Gradient Boosting model.

### Day 13  
Compared ensemble methods performance.

### Day 14  
Analyzed bias-variance tradeoff.

### Day 15  
Performed cross-validation.

### Day 16  
Optimized feature selection.

### Day 17  
Reduced noise in dataset.

### Day 18  
Improved model stability.

### Day 19  
Analyzed feature importance.

### Day 20  
Finalized best-performing ML baseline model.

---

## 🧠 Phase 3: Neural Network Development

### Day 21  
Designed neural network architecture.

### Day 22  
Implemented model using TensorFlow/PyTorch.

### Day 23  
Trained initial neural network.

### Day 24  
Evaluated performance vs traditional models.

### Day 25  
Tuned network parameters (layers, neurons).

### Day 26  
Added regularization techniques.

### Day 27  
Handled overfitting issues.

### Day 28  
Improved convergence using optimizers.

### Day 29  
Normalized input features.

### Day 30  
Finalized deep learning baseline model.

---

## ⚙️ Phase 4: Physics Integration (PIML Core)

### Day 31  
Studied mass balance equation for NOx concentration.

### Day 32  
Defined physical constraints for the system.

### Day 33  
Designed hybrid feature space (ML + physics inputs).

### Day 34  
Integrated physical parameters into model.

### Day 35  
Developed custom loss function combining error and physics violation.

### Day 36  
Implemented Physics-Informed Neural Network (PINN).

### Day 37  
Trained model with physics constraints.

### Day 38  
Analyzed trade-off between accuracy and physical consistency.

### Day 39  
Tuned physics regularization parameter (α).

### Day 40  
Validated model against physical laws.

---

## 📊 Phase 5: Model Evaluation & Optimization

### Day 41  
Evaluated model using MSE, RMSE, and R².

### Day 42  
Compared PIML vs standard ML models.

### Day 43  
Analyzed prediction errors.

### Day 44  
Improved model robustness.

### Day 45  
Handled edge cases in predictions.

### Day 46  
Tested model on unseen data.

### Day 47  
Reduced prediction variance.

### Day 48  
Improved generalization capability.

### Day 49  
Validated model consistency.

### Day 50  
Finalized optimized model.

---

## 🔍 Phase 6: Explainability Integration

### Day 51  
Integrated SHAP for feature importance.

### Day 52  
Analyzed contribution of environmental vs physical features.

### Day 53  
Implemented LIME for local explanations.

### Day 54  
Tested explanations on sample predictions.

### Day 55  
Improved interpretability outputs.

### Day 56  
Validated explanation reliability.

### Day 57  
Connected explainability with predictions.

### Day 58  
Visualized feature impact.

### Day 59  
Documented explainability results.

### Day 60  
Final review of model transparency.

---

## 📌 Final Model Summary

- Hybrid **Physics-Informed Machine Learning (PIML) model**
- Combines:
  - Data-driven learning (ML/DL)
  - Physical constraints (mass balance)
- Uses custom loss function:
