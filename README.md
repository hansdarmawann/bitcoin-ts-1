# 📈 Bitcoin (BTC) Monthly Price Forecasting  
**Time-Series Forecasting Project | TDSP Framework**

## 📌 Project Overview
Bitcoin merupakan aset kripto dengan volatilitas tinggi yang dipengaruhi oleh sentimen pasar, regulasi global, dan kondisi makroekonomi. Proyek ini bertujuan membangun **baseline forecasting model** untuk memprediksi harga Bitcoin bulanan menggunakan pendekatan *time-series* klasik dan modern.

Framework yang digunakan adalah **Microsoft Team Data Science Process (TDSP)** untuk memastikan alur analisis terstruktur dari bisnis hingga evaluasi model.

---

## 🎯 Business Objective
- Memprediksi **harga penutupan Bitcoin bulanan** menggunakan data historis (2014–2025)
- Menguji efektivitas model:
  - ARIMA
  - SARIMA
  - Prophet
- Menentukan model terbaik berdasarkan **RMSE**

---

## 🗂 Dataset
- **Source:** Historical Bitcoin OHLCV Data
- **Granularity:** Harian → Bulanan
- **Target Variable:** Monthly Average Close Price
- **Period:** 2014 – 2025

---

## 🔍 Analytic Approach
1. **Data Transformation**
   - Resampling harga harian menjadi **rata-rata bulanan (Monthly Start – MS)**
2. **Exploratory Data Analysis**
   - Visualisasi tren jangka panjang
   - Uji stasioneritas (ADF Test)
3. **Modeling**
   - ARIMA (1,1,1)
   - SARIMA (1,1,1)(1,1,1,12)
   - Prophet (multiplicative seasonality)
4. **Evaluation Metric**
   - Root Mean Squared Error (RMSE)
5. **Forecast Horizon**
   - 24 bulan (2 tahun)

---

## 🧠 Modeling Results
| Model    | Description                                  |
|---------|----------------------------------------------|
| ARIMA   | Baseline time-series model                   |
| SARIMA  | ARIMA dengan komponen musiman tahunan        |
| Prophet | Model modern dengan changepoint detection   |

👉 **Model terbaik dipilih otomatis berdasarkan RMSE terendah**

---

## 📊 Key Insights
- Data bulanan memberikan tren yang lebih stabil dibandingkan data harian
- Model mampu menangkap **arah tren jangka panjang**, namun:
  - Tidak menangkap faktor eksternal seperti berita & regulasi
  - Tidak cocok untuk *short-term trading*

---

## ⚠️ Risk & Limitation
- Bitcoin sangat dipengaruhi faktor non-historis
- Forecast **tidak boleh dianggap sebagai harga pasti**
- Digunakan sebagai:
  - Strategic insight
  - Trend projection
  - Decision support

---

## ✅ Conclusion
Pendekatan *time-series forecasting* pada data bulanan Bitcoin efektif sebagai **baseline model** untuk proyeksi tren jangka panjang. Model ini dapat dikembangkan lebih lanjut dengan:
- Exogenous variables (macro indicators, sentiment index)
- AutoARIMA tuning
- Hybrid ML / Deep Learning models

---

## 🛠 Tech Stack
- Python
- Pandas, NumPy
- Statsmodels
- Prophet
- Plotly, Matplotlib, Seaborn
- Scikit-learn

---

## 📁 Project Structure
