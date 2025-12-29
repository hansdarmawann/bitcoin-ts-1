import os
import sys
import streamlit as st
import pandas as pd

# =====================================================
# Setup project root & import path
# =====================================================
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from sources.model_loader import load_latest_model

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
        model_dir=os.path.join(PROJECT_ROOT, "models"),
        model_key="sarima"
    )

st.success(f"Model berhasil dimuat: `{model_file}`")

# =========================
# Tentukan tanggal awal forecast
# =========================
if metadata and "train_period" in metadata:
    last_train_date = pd.to_datetime(metadata["train_period"]["end"])
else:
    last_train_date = pd.Timestamp.today()

# =========================
# Slider Horizon (KONTROL UTAMA)
# =========================
st.subheader("📊 Hasil Prediksi")

forecast_horizon = st.slider(
    "⏳ Horizon Prediksi (bulan ke depan)",
    min_value=6,
    max_value=36,
    value=24,
    step=6
)

# =========================
# Generate Forecast
# =========================
forecast_index = pd.date_range(
    start=last_train_date + pd.offsets.MonthBegin(1),
    periods=forecast_horizon,
    freq="MS"
)

forecast = model.forecast(steps=forecast_horizon)

forecast_df = pd.DataFrame({
    "Tanggal": forecast_index,
    "Harga Prediksi (USD)": forecast.values
})

# =========================
# Visualisasi (SATU KALI)
# =========================
st.line_chart(
    forecast_df.set_index("Tanggal")
)

# =========================
# Informasi Model (TANPA RMSE)
# =========================
st.subheader("ℹ️ Informasi Model")

st.markdown("**Tipe Model**")
st.write("SARIMA (1,1,1)(1,1,1,12)")

if metadata and "train_period" in metadata:
    st.markdown("**Periode Data Latih**")
    st.write(
        f"{metadata['train_period']['start']} "
        f"sampai {metadata['train_period']['end']}"
    )

# =========================
# Interpretasi Bisnis
# =========================
st.subheader("🧠 Interpretasi")

st.info(
    f"""
    Prediksi ini menunjukkan **arah tren harga Bitcoin** untuk periode  
    **{forecast_df['Tanggal'].iloc[0].strftime('%B %Y')} sampai {forecast_df['Tanggal'].iloc[-1].strftime('%B %Y')}**.
    
    - Model difokuskan untuk menangkap **tren jangka menengah**, bukan fluktuasi harga harian.
    - Lonjakan atau penurunan harga ekstrem **tidak sepenuhnya tertangkap** oleh model SARIMA.
    - Hasil prediksi lebih sesuai digunakan untuk **analisis strategis**, bukan keputusan trading jangka pendek.
    """
)

# =========================
# Footer
# =========================
st.markdown("---")
st.caption("Dikembangkan oleh Hans Darmawan • Proyek Time-Series Forecasting")
