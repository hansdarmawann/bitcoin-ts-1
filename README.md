# 📈 Prediksi Harga Bitcoin (BTC) dengan Time-Series Forecasting  
**by Hans Darmawan**

## 📁 Project Structure

```
bitcoin-ts-1/
├─ datasets/                     # Dataset input
│  └─ btc_2014_2025.csv           # Data historis Bitcoin (Daily OHLCV)
│
├─ environments/                 # Environment reproducibility
│  └─ environment.yml            # Conda environment (local development)
│
├─ models/                       # Trained model artifacts
│  ├─ sarima_model_YYYYMMDD_HHMMSS.joblib     # Serialized SARIMA model
│  └─ sarima_metadata_YYYYMMDD_HHMMSS.json    # Model metadata (training period, metrics)
│
├─ notebooks/                    # Research & experimentation
│  └─ notebook.ipynb             # EDA, modeling, evaluation (TDSP workflow)
│
├─ sources/                      # Reusable application code
│  ├─ get_data.py                # Data fetching & preprocessing
│  ├─ model_loader.py            # Auto-load latest model + metadata
│  ├─ streamlit_app.py           # Streamlit dashboard (visualization & inference)
│  ├─ clean_cache.py             # Utility: clean Python cache
│  └─ __init__.py
│
├─ requirements.txt              # Minimal dependencies for Streamlit Cloud
├─ run_streamlit.bat             # Local Streamlit launcher (Windows)
├─ README.md                     # Project documentation
└─ .gitignore                    # Git ignore rules
```

## 📌 Overview

Proyek ini bertujuan untuk memprediksi **harga Bitcoin bulanan** menggunakan pendekatan *time-series forecasting*. Fokus utama proyek adalah mengevaluasi seberapa efektif model *time-series* dalam menangani **aset dengan volatilitas tinggi**, seperti Bitcoin.

Proyek ini dibangun secara **end-to-end**, mulai dari eksplorasi data, pemodelan, evaluasi, hingga kesiapan deployment ringan melalui **Streamlit**.  
Pendekatan kerja mengikuti kerangka **Microsoft Team Data Science Process (TDSP)**.

## 💼 Business Problem

Bitcoin memiliki karakteristik harga yang sangat fluktuatif dan dipengaruhi oleh banyak faktor eksternal. Stakeholder ingin memahami:

- Apakah data historis harga Bitcoin cukup informatif untuk memprediksi harga di masa depan?
- Model *time-series- mana yang paling efektif untuk menangkap **tren harga bulanan** Bitcoin?
- Seberapa besar tingkat kesalahan prediksi yang dihasilkan oleh masing-masing model?

## 🎯 Objectives

- Mengubah data harga Bitcoin **harian → bulanan** untuk mengurangi *noise*
- Memprediksi harga Bitcoin untuk **24 bulan ke depan**
- Membandingkan performa beberapa model *time-series*
- Menentukan model terbaik berdasarkan evaluasi kuantitatif

## 📊 Dataset

- **Source**: Yahoo Finance  
- **Period**: September 2014 – Desember 2025  
- **Initial Frequency**: Daily (OHLCV)  
- **Target Variable**: `close` (harga penutupan)

Data harian di-*resample* menjadi **rata-rata bulanan** untuk:
- mengurangi fluktuasi ekstrem
- meningkatkan stabilitas model
- mempermudah analisis tren jangka menengah

## 🧠 Methodology (TDSP)

### 1. Business Understanding
Memahami karakteristik Bitcoin sebagai aset berisiko tinggi dan menentukan tujuan prediksi berbasis kebutuhan analisis tren.

### 2. Data Acquisition & Understanding
- Validasi data (tidak ada *missing value- dan duplikasi)
- Resampling data harian ke bulanan
- Visualisasi tren harga Bitcoin
- Uji stasioneritas menggunakan **ADF Test**

### 3. Modeling

**Train–Test Split**
- Training: September 2014 – Desember 2023  
- Testing: Januari 2024 – Desember 2025  

**Model yang digunakan**
- **ARIMA (1,1,1)** – baseline
- **SARIMA (1,1,1)(1,1,1,12)** – menangkap pola musiman tahunan
- **Prophet** – tren non-linear dan *changepoints*

### 4. Evaluation

Evaluasi dilakukan menggunakan **RMSE (Root Mean Squared Error)**.

| Model   | RMSE (USD) |
|--------|------------|
| SARIMA | ~36,057 |
| ARIMA  | ~44,018 |
| Prophet| ~47,777 |

Model **SARIMA** memberikan performa terbaik dan dipilih sebagai **model final**.

### 5. Deployment Readiness

- Model disimpan sebagai artefak menggunakan **joblib**
- Metadata model disimpan dalam format JSON
- Disediakan **Model Loader (Level 2)** untuk:
  - auto-load model terbaru
  - auto-load metadata yang sesuai
  - reusable di notebook, Streamlit, atau API

## 🚀 Streamlit App (Demo)
Link: https://bitcoin-ts-1.streamlit.app/

### Fitur Utama
- Auto-load **model SARIMA terbaru**
- Pengaturan **horizon prediksi (6–36 bulan)**
- Visualisasi tren harga Bitcoin bulanan
- Fokus pada **analisis tren jangka menengah**

## 🔍 Key Findings

- Data Bitcoin bulanan masih menunjukkan **pola musiman tahunan**
- Model klasik (**SARIMA**) mampu mengungguli model modern (**Prophet**)
- Prediksi lebih cocok digunakan sebagai **indikator arah tren**, bukan nilai harga absolut

## ⚠️ Limitations

- Model hanya menggunakan data historis harga
- Tidak mempertimbangkan faktor eksternal (sentimen, regulasi, makroekonomi)
- Prediksi bersifat halus dan kurang cocok untuk *short-term trading*
- Parameter model belum dioptimasi menggunakan AutoARIMA

## 💡 Recommendations

- Gunakan hasil prediksi sebagai **indikator tren**
- Tambahkan variabel eksternal untuk meningkatkan akurasi
- Lakukan optimasi parameter model
- Eksplor pendekatan **hybrid** (time-series + ML)
- Sesuaikan horizon prediksi dengan kebutuhan bisnis

## 🛠 Tools & Libraries

- Python (pandas, numpy)
- statsmodels
- Prophet
- scikit-learn
- Plotly
- joblib
- Streamlit