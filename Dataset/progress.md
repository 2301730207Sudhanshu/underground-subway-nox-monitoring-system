# 📊 Dataset Folder Progress Log

## 🗓️ Day 1
- Created `dataset/` directory
- Added initial sample dataset (`sample_nox_data.csv`)
- Defined basic schema:
  - Timestamp
  - NOx concentration
  - Temperature
  - Humidity
  - Airflow velocity

## 🗓️ Day 2
- Collected real-world air quality data from OpenAQ
- Downloaded CSV files for multiple locations
- Merged datasets into a unified format
- Handled missing values (NaN → interpolation)

## 🗓️ Day 3
- Performed data cleaning:
  - Removed duplicates
  - Fixed inconsistent units
- Standardized column names
- Converted timestamps to uniform format

## 🗓️ Day 4
- Added engineered features:
  - Traffic intensity (simulated)
  - Ventilation rate (estimated)
  - Tunnel length factor
- Normalized numerical features (Min-Max Scaling)

## 🗓️ Day 5
- Split dataset into:
  - `train.csv`
  - `test.csv`
  - `validation.csv`
- Ensured proper time-based splitting
- Saved processed dataset (`processed_nox_data.csv`)

## 🗓️ Day 6
- Added synthetic data for:
  - Subway tunnel conditions
  - Peak vs off-peak variations
- Simulated NOx emission using physics-based assumptions
- Verified distribution consistency

## 🗓️ Day 7
- Final validation checks:
  - No missing values
  - Correct feature ranges
- Documented dataset metadata
- Linked dataset with ML pipeline

---

## 📊 Current Status
- Total Records: ~50,000+
- Features: 10+
- Data Sources:
  - OpenAQ API ✅
  - Simulated Tunnel Data ✅

---

## 📁 Folder Structure
