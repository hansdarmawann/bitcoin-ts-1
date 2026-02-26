# 📈 Bitcoin (BTC) Price Prediction with Time-Series Forecasting
**by Hans Darmawan**

## 📁 Project Structure

```
bitcoin-ts-1/
├─ datasets/ # Input datasets
│ └─ btc_2014_2025.csv # Bitcoin historical data (Daily OHLCV)
│
├─ environments/ # Environment reproducibility
│ └─ environment.yml # Conda environment (local development)
│
├─ models/ # Trained model artifacts
│ ├─ sarima_model_YYYYMMDD_HHMMSS.joblib # Serialized SARIMA model
│ └─ sarima_metadata_YYYYMMDD_HHMMSS.json # Metadata model (training period, metrics)
│
├─ notebooks/ # Research & experimentation
│ └─ notebook.ipynb # EDA, modeling, evaluation (TDSP workflow)
│
├─ sources/ # Reusable application code
│ ├─ get_data.py # Data fetching & preprocessing
│ ├─ model_loader.py # Auto-load latest model + metadata
│ ├─ streamlit_app.py # Streamlit dashboard (visualization & inference)
│ ├─ clean_cache.py # Utility: clean Python cache
│ └─ __init__.py
│
├─ requirements.txt # Minimal dependencies for Streamlit Cloud
├─ run_streamlit.bat # Local Streamlit launcher (Windows)
├─ README.md # Project documentation
└─ .gitignore # Git rules ignore
```

## 📌 Overview

This project aims to predict the monthly Bitcoin price using a time-series forecasting approach. The project's primary focus is to evaluate the effectiveness of time-series models in handling highly volatile assets, such as Bitcoin.

This project is built end-to-end, from data exploration and modeling to evaluation and lightweight deployment readiness via Streamlit.
The working approach follows the Microsoft Team Data Science Process (TDSP) framework.

## 💼 Business Problem

Bitcoin has a highly volatile price and is influenced by many external factors. Stakeholders want to understand:

- Is historical Bitcoin price data informative enough to predict future prices?
- Which time-series model is most effective in capturing Bitcoin's monthly price trend?
- What is the level of prediction error produced by each model?

## 🎯 Objectives

- Transform Bitcoin price data from daily to monthly to reduce noise
- Predict Bitcoin prices for the next 24 months
- Compare the performance of several time-series models
- Determine the best model based on quantitative evaluation

## 📊 Dataset

- **Source**: Yahoo Finance
- **Period**: September 2014 – December 2025
- **Initial Frequency**: Daily (OHLCV)
- **Target Variable**: `close` (closing price)

Daily data is resampled to a monthly average to:
- reduce extreme fluctuations
- improve model stability
- facilitate medium-term trend analysis

## 🧠 Methodology (TDSP)

### 1. Business Understanding
Understand the characteristics of Bitcoin as a high-risk asset and determine prediction objectives based on trend analysis needs.

### 2. Data Acquisition & Understanding
- Data validation (no missing values ​​and duplication)
- Daily to monthly data resampling
- Bitcoin price trend visualization
- Stationarity test using the ADF Test

### 3. Modeling

Train–Test Split
- Training: September 2014 – December 2023
- Testing: January 2024 – December 2025

Models used
- ARIMA (1,1,1) – baseline
- SARIMA (1,1,1)(1,1,1,12) – captures annual seasonal patterns
- Prophet – non-linear trends and changepoints

### 4. Evaluation

Evaluation was conducted using RMSE (Root Mean Squared Error).

| Model | RMSE (USD) |
|--------|------------|
| SARIMA | ~36.057 |
| ARIMA | ~44.018 |
| Prophet | ~47.777 |

The SARIMA model performed the best and was selected as the final model.

### 5. Deployment Readiness

- Models are stored as artifacts using **joblib**
- Model metadata is stored in JSON format
- Model Loader (Level 2)** is provided for:
- auto-loading the latest model
- auto-loading appropriate metadata
- reusable in notebooks, Streamlit, or API

## 🚀 Streamlit App (Demo)
Link: https://bitcoin-ts-1.streamlit.app/

### Key Features
- Auto-loading the latest SARIMA model
- Prediction horizon setting (6–36 months)
- Monthly Bitcoin price trend visualization
- Focus on medium-term trend analysis

## 🔍 Key Findings

- Monthly Bitcoin data still shows annual seasonal patterns
- Classical models (SARIMA) outperform modern models (Prophet)
- Predictions are better suited as trend direction indicators, rather than absolute price values

## ⚠️ Limitations

- The model only uses historical price data
- Does not consider external factors (sentiment, regulations, macroeconomics)
- Predictions are smooth and less suitable for short-term trading
- Model parameters have not been optimized using AutoARIMA

## 💡 Recommendations

- Use prediction results as a trend indicator
- Add external variables to improve accuracy
- Optimize model parameters
- Explore a hybrid approach (time-series + ML)
- Adjust the prediction horizon to business needs

## 🛠 Tools & Libraries

- Python (pandas, numpy)
- statsmodels
- Prophet
- scikit-learn
- Plotly
- joblib
- Streamlit