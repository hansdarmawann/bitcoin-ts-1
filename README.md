# 📈 Bitcoin (BTC) Price Prediction using Time-Series Forecasting
by Hans Darmawan

## Project Structure

| Path | Description |
|------|-------------|
| `.gitignore` | Konfigurasi file dan folder yang dikecualikan dari Git |
| `README.md` | Dokumentasi utama proyek |
| `Codes/` | Script Python pendukung |
| `Codes/get_data.py` | Script untuk pengambilan / persiapan data Bitcoin |
| `Datasets/` | Folder penyimpanan dataset |
| `Datasets/btc_2014_2025.csv` | Dataset harga Bitcoin harian (OHLCV) dari Yahoo Finance |
| `Notebooks/` | Jupyter Notebook untuk analisis dan modeling |
| `Notebooks/notebook.ipynb` | Notebook utama: EDA, modeling, evaluasi, dan visualisasi |
| `Environments/` | Konfigurasi environment |
| `Environments/environment.yml` | File environment Conda untuk replikasi setup |
| `lst.txt` | File tambahan (log / catatan internal) |



## Overview
Proyek ini bertujuan untuk memprediksi **harga Bitcoin bulanan** menggunakan pendekatan *time-series forecasting*. Fokus utama proyek adalah mengevaluasi efektivitas model klasik dan modern dalam menangani data dengan **volatilitas tinggi**, seperti Bitcoin.

Pendekatan yang digunakan mengikuti kerangka kerja **Microsoft Team Data Science Process (TDSP)**, mulai dari pemahaman bisnis hingga evaluasi model.

## Business Problem
Bitcoin memiliki pergerakan harga yang sangat fluktuatif dan dipengaruhi oleh banyak faktor eksternal. Stakeholder ingin mengetahui:
- Apakah data historis harga Bitcoin dapat digunakan untuk memprediksi harga di masa depan?
- Model *time-series* mana yang paling efektif untuk menangkap tren harga Bitcoin bulanan?
- Seberapa besar tingkat kesalahan prediksi yang dihasilkan oleh masing-masing model?

## Objectives
- Mengubah data harga Bitcoin harian menjadi data **bulanan** untuk mengurangi *noise*.
- Memprediksi harga Bitcoin untuk **24 bulan ke depan**.
- Membandingkan performa beberapa model *time-series*.
- Menentukan model terbaik berdasarkan metrik evaluasi kuantitatif.

## Dataset
- **Sumber**: Yahoo Finance  
- **Periode**: September 2014 – Desember 2025  
- **Frekuensi awal**: Harian (OHLCV)  
- **Kolom utama yang digunakan**: `close` (harga penutupan)

Data harian di-*resample* menjadi **rata-rata bulanan** untuk meningkatkan stabilitas model dan memudahkan analisis tren jangka menengah.

## Methodology (TDSP)

### 1. Business Understanding
Memahami karakteristik Bitcoin sebagai aset dengan volatilitas tinggi dan menentukan tujuan prediksi berbasis kebutuhan bisnis.

### 2. Data Acquisition & Understanding
- Memuat dan memvalidasi dataset (tidak ada missing value dan duplikasi).
- Resampling data harian menjadi bulanan.
- Visualisasi tren harga Bitcoin.
- Uji stasioneritas menggunakan **ADF Test**.

### 3. Modeling
Data dibagi menjadi:
- **Training set**: September 2014 – Desember 2023  
- **Test set**: Januari 2024 – Desember 2025  

Model yang digunakan:
- **ARIMA (1,1,1)** – sebagai *baseline*
- **SARIMA (1,1,1)(1,1,1,12)** – menambahkan pola musiman tahunan
- **Prophet** – model modern yang menangani tren non-linear dan *changepoints*

### 4. Evaluation
Evaluasi dilakukan menggunakan **RMSE (Root Mean Squared Error)**.

| Model   | RMSE (USD) |
|--------|------------|
| SARIMA | ~36,071 |
| ARIMA | ~44,035 |
| Prophet | ~47,793 |

Model **SARIMA** menunjukkan performa terbaik dan dipilih sebagai model final.

### 5. Deployment & Acceptance
Hasil prediksi divisualisasikan dengan membandingkan harga aktual dan hasil prediksi SARIMA pada periode uji untuk mendukung interpretasi bisnis.

## Key Findings
- Data Bitcoin bulanan masih menunjukkan **pola musiman tahunan**.
- Model klasik (SARIMA) mampu mengungguli model modern (Prophet) pada kasus ini.
- Prediksi lebih efektif untuk **melihat arah tren**, bukan untuk memprediksi lonjakan harga ekstrem.

## Limitations
- Model hanya menggunakan data historis harga tanpa faktor eksternal (berita, regulasi, sentimen).
- Prediksi bersifat halus dan tidak menangkap volatilitas ekstrem.
- Tidak cocok untuk *trading* jangka pendek atau harian.
- Parameter model belum dioptimalkan sepenuhnya (belum menggunakan AutoARIMA).

## Recommendations
- Gunakan hasil prediksi sebagai **indikator tren**, bukan harga pasti.
- Tambahkan variabel eksternal untuk meningkatkan akurasi.
- Lakukan optimasi parameter model.
- Eksplor pendekatan **hybrid** (time-series + machine learning).
- Sesuaikan horizon prediksi dengan kebutuhan analisis strategis.

## Tools & Libraries
- Python (pandas, numpy)
- statsmodels
- Prophet
- scikit-learn
- Plotly