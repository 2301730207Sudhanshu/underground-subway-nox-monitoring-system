# 📊 Dataset Development Log  
## Underground Subway NOx Monitoring System  

---

## 🗓️ Day 1  
Created `dataset/` directory  
Added initial sample dataset (`sample_nox_data.csv`)  
Defined basic schema:  
- Timestamp  
- NOx concentration  
- Temperature  
- Humidity  
- Airflow velocity  

---

## 🗓️ Day 2  
Collected real-world air quality data from OpenAQ  
Downloaded CSV files for multiple locations  
Merged datasets into a unified format  
Handled missing values (NaN → interpolation)  

---

## 🗓️ Day 3  
Performed data cleaning:  
- Removed duplicates  
- Fixed inconsistent units  
- Standardized column names  
- Converted timestamps to uniform format  

---

## 🗓️ Day 4  
Added engineered features:  
- Traffic intensity (simulated)  
- Ventilation rate (estimated)  
- Tunnel length factor  
Applied normalization (Min-Max Scaling)  

---

## 🗓️ Day 5  
Split dataset into:  
- `train.csv`  
- `test.csv`  
- `validation.csv`  
Ensured proper time-based splitting  
Saved `processed_nox_data.csv`  

---

## 🗓️ Day 6  
Added synthetic data for subway conditions  
Simulated peak vs off-peak variations  
Generated NOx using physics assumptions  
Verified data distribution  

---

## 🗓️ Day 7  
Performed final validation checks  
Ensured no missing values  
Validated feature ranges  
Linked dataset with ML pipeline  

---

## 🗓️ Day 8  
Expanded dataset with additional OpenAQ locations  
Improved geographical diversity  

---

## 🗓️ Day 9  
Added seasonal variations (summer/winter patterns)  
Simulated temperature impact on NOx  

---

## 🗓️ Day 10  
Introduced hourly patterns (rush hour vs non-rush)  
Improved temporal realism  

---

## 🗓️ Day 11  
Added lag features (previous time-step values)  

---

## 🗓️ Day 12  
Generated rolling averages for smoothing  

---

## 🗓️ Day 13  
Performed correlation analysis between features  

---

## 🗓️ Day 14  
Removed highly correlated redundant features  

---

## 🗓️ Day 15  
Introduced noise filtering techniques  

---

## 🗓️ Day 16  
Enhanced synthetic tunnel airflow simulation  

---

## 🗓️ Day 17  
Refined passenger load estimation  

---

## 🗓️ Day 18  
Validated proxy features against realistic assumptions  

---

## 🗓️ Day 19  
Improved interpolation for missing timestamps  

---

## 🗓️ Day 20  
Created final feature list for modeling  

---

## 🗓️ Day 21  
Applied standardization (Z-score scaling)  

---

## 🗓️ Day 22  
Compared normalization vs standardization  

---

## 🗓️ Day 23  
Optimized feature scaling pipeline  

---

## 🗓️ Day 24  
Handled outliers using IQR method  

---

## 🗓️ Day 25  
Re-validated dataset consistency  

---

## 🗓️ Day 26  
Created time-based features:  
- Hour  
- Day  
- Week  

---

## 🗓️ Day 27  
Added seasonal encoding  

---

## 🗓️ Day 28  
Tested time-series resampling methods  

---

## 🗓️ Day 29  
Aligned all datasets to uniform time intervals  

---

## 🗓️ Day 30  
Finalized time-series preprocessing pipeline  

---

## 🗓️ Day 31  
Integrated dataset with model training pipeline  

---

## 🗓️ Day 32  
Tested dataset loading performance  

---

## 🗓️ Day 33  
Optimized dataset memory usage  

---

## 🗓️ Day 34  
Converted dataset to efficient formats (CSV → optimized)  

---

## 🗓️ Day 35  
Added metadata documentation  

---

## 🗓️ Day 36  
Versioned dataset (v1.0)  

---

## 🗓️ Day 37  
Performed dataset validation checks  

---

## 🗓️ Day 38  
Improved feature engineering scripts  

---

## 🗓️ Day 39  
Created reusable preprocessing functions  

---

## 🗓️ Day 40  
Automated dataset pipeline  

---

## 🗓️ Day 41  
Connected dataset pipeline with API  

---

## 🗓️ Day 42  
Tested real-time data ingestion  

---

## 🗓️ Day 43  
Simulated streaming data  

---

## 🗓️ Day 44  
Handled streaming inconsistencies  

---

## 🗓️ Day 45  
Optimized ingestion speed  

---

## 🗓️ Day 46  
Integrated database storage  

---

## 🗓️ Day 47  
Stored dataset in PostgreSQL  

---

## 🗓️ Day 48  
Tested query performance  

---

## 🗓️ Day 49  
Optimized indexing for time-series data  

---

## 🗓️ Day 50  
Finalized database schema  

---

## 🗓️ Day 51  
Improved scalability of dataset pipeline  

---

## 🗓️ Day 52  
Tested large dataset handling  

---

## 🗓️ Day 53  
Validated dataset for edge cases  

---

## 🗓️ Day 54  
Stress-tested dataset pipeline  

---

## 🗓️ Day 55  
Integrated dataset with visualization layer  

---

## 🗓️ Day 56  
Validated end-to-end data flow  

---

## 🗓️ Day 57  
Performed final cleaning  

---

## 🗓️ Day 58  
Final dataset verification  

---

## 🗓️ Day 59  
Prepared dataset documentation  

---

## 🗓️ Day 60  
Final dataset freeze and deployment-ready version  

---

## 📊 Current Status  

- **Total Records:** ~50,000+  
- **Features:** 10+  
- **Data Sources:**  
  - OpenAQ API ✅  
  - Simulated Tunnel Data ✅  

---

## 📁 Folder Structure  
dataset/
│── raw/
│ ├── openaq_data.csv
│
│── processed/
│ ├── processed_nox_data.csv
│ ├── train.csv
│ ├── test.csv
│ ├── validation.csv
│
│── scripts/
│ ├── data_cleaning.py
│ ├── feature_engineering.py
│ ├── preprocessing_pipeline.py
│
│── metadata/
│ ├── dataset_info.md
│
