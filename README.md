# 📈 Bitcoin (BTC) Price Prediction using Time-Series Forecasting  
**by Hans Darmawan**

---

## 📁 Project Structure

```
bitcoin-ts-1/
├─ datasets/
│  └─ btc_2014_2025.csv
├─ environments/
│  └─ environment.yml
├─ models/
│  ├─ sarima_model_YYYYMMDD_HHMMSS.joblib
│  └─ sarima_metadata_YYYYMMDD_HHMMSS.json
├─ notebooks/
│  └─ notebook.ipynb
├─ sources/
│  ├─ get_data.py
│  ├─ model_loader.py
│  ├─ streamlit_app.py
│  └─ clean_cache.py
├─ run_streamlit.bat
└─ README.md
```

---

## 📌 Overview

Proyek ini bertujuan untuk memprediksi **harga Bitcoin bulanan** menggunakan pendekatan *time-series forecasting*. Fokus utama proyek adalah mengevaluasi seberapa efektif model *time-series* dalam menangani **aset dengan volatilitas tinggi**, seperti Bitcoin.

Proyek ini dibangun secara **end-to-end**, mulai dari eksplorasi data, pemodelan, evaluasi, hingga kesiapan deployment ringan melalui **Streamlit**.  
Pendekatan kerja mengikuti kerangka **Microsoft Team Data Science Process (TDSP)**.

---

## 💼 Business Problem

Bitcoin memiliki karakteristik harga yang sangat fluktuatif dan dipengaruhi oleh banyak faktor eksternal. Stakeholder ingin memahami:

- Apakah data historis harga Bitcoin cukup informatif untuk memprediksi harga di masa depan?
- Model *time-series* mana yang paling efektif untuk menangkap **tren harga bulanan** Bitcoin?
- Seberapa besar tingkat kesalahan prediksi yang dihasilkan oleh masing-masing model?

---

## 🎯 Objectives

- Mengubah data harga Bitcoin **harian → bulanan** untuk mengurangi *noise*
- Memprediksi harga Bitcoin untuk **24 bulan ke depan**
- Membandingkan performa beberapa model *time-series*
- Menentukan model terbaik berdasarkan evaluasi kuantitatif

---

## 📊 Dataset

- **Source**: Yahoo Finance  
- **Period**: September 2014 – Desember 2025  
- **Initial Frequency**: Daily (OHLCV)  
- **Target Variable**: `close` (harga penutupan)

Data harian di-*resample* menjadi **rata-rata bulanan** untuk:
- mengurangi fluktuasi ekstrem
- meningkatkan stabilitas model
- mempermudah analisis tren jangka menengah

---

## 🧠 Methodology (TDSP)

### 1. Business Understanding
Memahami karakteristik Bitcoin sebagai aset berisiko tinggi dan menentukan tujuan prediksi berbasis kebutuhan analisis tren.

### 2. Data Acquisition & Understanding
- Validasi data (tidak ada *missing value* dan duplikasi)
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

---

## 🚀 Streamlit App (Demo)

Proyek ini menyediakan **aplikasi Streamlit** untuk menampilkan hasil prediksi secara interaktif.

### Fitur Utama
- Auto-load **model SARIMA terbaru**
- Pengaturan **horizon prediksi (6–36 bulan)**
- Visualisasi tren harga Bitcoin bulanan
- Fokus pada **analisis tren jangka menengah**

### Menjalankan Aplikasi (Windows)

```bash
conda env create -f environments/environment.yml
conda activate bitcoin-ts-1
run_streamlit.bat
````

Aplikasi akan berjalan di:

```
http://localhost:8501
```

> Catatan: Aplikasi ini ditujukan untuk **analisis arah tren**, bukan prediksi harga harian atau keputusan trading jangka pendek.

---

## 🔍 Key Findings

* Data Bitcoin bulanan masih menunjukkan **pola musiman tahunan**
* Model klasik (**SARIMA**) mampu mengungguli model modern (**Prophet**)
* Prediksi lebih cocok digunakan sebagai **indikator arah tren**, bukan nilai harga absolut

---

## ⚠️ Limitations

* Model hanya menggunakan data historis harga
* Tidak mempertimbangkan faktor eksternal (sentimen, regulasi, makroekonomi)
* Prediksi bersifat halus dan kurang cocok untuk *short-term trading*
* Parameter model belum dioptimasi menggunakan AutoARIMA

---

## 💡 Recommendations

* Gunakan hasil prediksi sebagai **indikator tren**
* Tambahkan variabel eksternal untuk meningkatkan akurasi
* Lakukan optimasi parameter model
* Eksplor pendekatan **hybrid** (time-series + ML)
* Sesuaikan horizon prediksi dengan kebutuhan bisnis

---

## 🛠 Tools & Libraries

* Python (pandas, numpy)
* statsmodels
* Prophet
* scikit-learn
* Plotly
* joblib
* Streamlit