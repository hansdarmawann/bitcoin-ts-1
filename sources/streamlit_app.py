import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from model_loader import load_latest_model


# =========================
# Konfigurasi Halaman
# =========================
st.set_page_config(
    page_title="Prediksi Harga Bitcoin",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Prediksi Harga Bitcoin (BTC) Bulanan")
st.caption(
    "Time-Series Forecasting menggunakan SARIMA | "
    "Fokus pada tren jangka menengah, bukan volatilitas jangka pendek"
)


# =========================
# Load Model Terbaru
# =========================
with st.spinner("Memuat model terbaru..."):
    model, metadata, model_file = load_latest_model(
        model_dir="models",
        model_key="sarima"
    )

st.success(f"Model berhasil dimuat: `{model_file}`")


# =========================
# Slider Horizon
# =========================
st.subheader("🔧 Pengaturan Prediksi")

forecast_horizon = st.slider(
    "Horizon Prediksi (bulan)",
    min_value=6,
    max_value=36,
    value=6,
    step=6
)


# =========================
# Tentukan tanggal awal forecast (AMAN)
# =========================
if metadata and "train_period" in metadata and "end" in metadata["train_period"]:
    last_train_date = pd.to_datetime(metadata["train_period"]["end"])
else:
    last_train_date = pd.to_datetime("today").replace(day=1)


# =========================
# Proses Prediksi
# =========================
forecast_values = model.forecast(steps=forecast_horizon)

forecast_dates = [
    last_train_date + relativedelta(months=i + 1)
    for i in range(forecast_horizon)
]

forecast_df = pd.DataFrame({
    "Tanggal": forecast_dates,
    "Harga Prediksi (USD)": forecast_values.values
}).sort_values("Tanggal")


# =========================
# Visualisasi (FIX UTAMA)
# =========================
st.subheader("📊 Hasil Prediksi")

# ❗ Datetime HARUS jadi index (bukan string)
chart_df = forecast_df.set_index("Tanggal")[["Harga Prediksi (USD)"]]

st.line_chart(chart_df)


# =========================
# Informasi Model (MINIMAL)
# =========================
st.subheader("ℹ️ Informasi Model")

st.write("**Tipe Model:** SARIMA (auto-loaded)")
st.write(f"**Horizon Prediksi:** {forecast_horizon} bulan")


# =========================
# Interpretasi
# =========================
st.subheader("🧠 Interpretasi")

st.info(
    f"""
    Prediksi ini menunjukkan **arah tren harga Bitcoin untuk {forecast_horizon} bulan ke depan**.

    - Model difokuskan pada **tren jangka menengah**, bukan fluktuasi harian.
    - Horizon lebih panjang menghasilkan tren lebih halus, namun ketidakpastian meningkat.
    - Tidak disarankan untuk **short-term trading**.
    """
)


# =========================
# Footer
# =========================
st.markdown("---")
st.caption("Dikembangkan oleh Hans Darmawan • Proyek Time-Series Forecasting")
