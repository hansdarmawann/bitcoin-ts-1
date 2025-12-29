# 📈 Bitcoin (BTC) Price Prediction using Time-Series Forecasting
**by Hans Darmawan**

---

## 📁 Folder Description

| Path | Description |
|-----|------------|
| `.gitignore` | Konfigurasi file dan folder yang dikecualikan dari Git |
| `README.md` | Dokumentasi utama proyek |
| `lst.txt` | Catatan / log internal |
| `datasets/` | Dataset harga Bitcoin |
| `datasets/btc_2014_2025.csv` | Data harian Bitcoin (OHLCV) dari Yahoo Finance |
| `environments/` | Konfigurasi environment |
| `environments/environment.yml` | File Conda environment untuk replikasi setup |
| `models/` | Artefak model terlatih |
| `models/sarima_model_YYYYMMDD_HHMMSS.joblib` | Model SARIMA terlatih (versioned) |
| `models/sarima_metadata_YYYYMMDD_HHMMSS.json` | Metadata model (RMSE, periode training, dll) |
| `notebooks/` | Jupyter Notebook untuk analisis dan modeling |
| `notebooks/notebook.ipynb` | Notebook utama (EDA, modeling, evaluasi, visualisasi) |
| `sources/` | Script Python reusable |
| `sources/get_data.py` | Script pengambilan dan persiapan data |
| `sources/model_loader.py` | Loader model (Level 2: auto-load model + metadata) |
| `sources/clean_cache.py` | Utility untuk membersihkan cache Python |

---

## 📌 Overview

Proyek ini bertujuan untuk memprediksi **harga Bitcoin bulanan** menggunakan pendekatan *time-series forecasting*. Fokus utama proyek adalah mengevaluasi efektivitas model klasik dan modern dalam menangani data dengan **volatilitas tinggi**, seperti Bitcoin.

Pendekatan yang digunakan mengikuti kerangka kerja **Microsoft Team Data Science Process (TDSP)**, mulai dari pemahaman bisnis hingga evaluasi dan kesiapan deployment.

---

## 💼 Business Problem

Bitcoin memiliki pergerakan harga yang sangat fluktuatif dan dipengaruhi oleh berbagai faktor eksternal. Stakeholder ingin mengetahui:

- Apakah data historis harga Bitcoin dapat digunakan untuk memprediksi harga di masa depan?
- Model *time-series* mana yang paling efektif untuk menangkap tren harga Bitcoin bulanan?
- Seberapa besar tingkat kesalahan prediksi yang dihasilkan oleh masing-masing model?

---

## 🎯 Objectives

- Mengubah data harga Bitcoin harian menjadi data **bulanan** untuk mengurangi *noise*
- Memprediksi harga Bitcoin untuk **24 bulan ke depan**
- Membandingkan performa beberapa model *time-series*
- Menentukan model terbaik berdasarkan metrik evaluasi kuantitatif

---

## 📊 Dataset

- **Source**: Yahoo Finance  
- **Period**: September 2014 – Desember 2025  
- **Initial Frequency**: Daily (OHLCV)  
- **Target Variable**: `close` (harga penutupan)

Data harian di-*resample* menjadi **rata-rata bulanan** untuk meningkatkan stabilitas model dan memudahkan analisis tren jangka menengah.

---

## 🧠 Methodology (TDSP)

### 1. Business Understanding
Memahami karakteristik Bitcoin sebagai aset dengan volatilitas tinggi dan menentukan tujuan prediksi berbasis kebutuhan bisnis.

### 2. Data Acquisition & Understanding
- Validasi dataset (tidak ada missing value dan duplikasi)
- Resampling data harian ke bulanan
- Visualisasi tren harga Bitcoin
- Uji stasioneritas menggunakan **ADF Test**

### 3. Modeling

**Train–Test Split**
- Training set: September 2014 – Desember 2023  
- Test set: Januari 2024 – Desember 2025  

**Models**
- **ARIMA (1,1,1)** – baseline
- **SARIMA (1,1,1)(1,1,1,12)** – menangkap pola musiman tahunan
- **Prophet** – tren non-linear dan *changepoints*

### 4. Evaluation

Evaluasi menggunakan **RMSE (Root Mean Squared Error)**.

| Model   | RMSE (USD) |
|--------|------------|
| SARIMA | ~36,057 |
| ARIMA | ~44,018 |
| Prophet | ~47,777 |

Model **SARIMA** menunjukkan performa terbaik dan dipilih sebagai **model final**.

### 5. Deployment Readiness

- Model disimpan sebagai artefak menggunakan **joblib**
- Metadata disimpan dalam format JSON
- Model loader Level 2 memungkinkan:
  - Auto-load model terbaru
  - Auto-load metadata yang sesuai
  - Reusability di notebook, Streamlit, atau API

---

## 🔍 Key Findings

- Data Bitcoin bulanan masih menunjukkan **pola musiman tahunan**
- Model klasik (**SARIMA**) mampu mengungguli model modern (**Prophet**)
- Prediksi lebih efektif untuk **analisis arah tren**, bukan lonjakan ekstrem

---

## ⚠️ Limitations

- Model hanya menggunakan data historis harga
- Tidak mempertimbangkan faktor eksternal (sentimen, regulasi, makroekonomi)
- Prediksi bersifat halus dan tidak cocok untuk *short-term trading*
- Parameter model belum dioptimasi menggunakan AutoARIMA

---

## 💡 Recommendations

- Gunakan hasil prediksi sebagai **indikator tren**, bukan harga absolut
- Tambahkan variabel eksternal untuk meningkatkan akurasi
- Lakukan optimasi parameter model
- Eksplor pendekatan **hybrid** (time-series + ML)
- Sesuaikan horizon prediksi dengan kebutuhan bisnis

---

## 🛠 Tools & Libraries

- Python (pandas, numpy)
- statsmodels
- Prophet
- scikit-learn
- Plotly
- joblib