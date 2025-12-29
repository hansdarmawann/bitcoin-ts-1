# =========================================================
# Streamlit App - Bitcoin (BTC) Monthly Price Forecast
# =========================================================

# --- Fix import path for Streamlit Cloud ---
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

# --- Standard imports ---
import streamlit as st
import pandas as pd

# --- Local module import ---
from sources.model_loader import load_latest_model


# =========================================================
# Konfigurasi Halaman
# =========================================================
st.set_page_config(
    page_title="Prediksi Harga Bitcoin",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Prediksi Harga Bitcoin (BTC) Bulanan")


# =========================================================
# Load Model Terbaru
# =========================================================
with st.spinner("Memuat model terbaru..."):
    model, metadata, model_file = load_latest_model(
        model_dir="models",
        model_key="sarima"
    )

st.success(f"Model berhasil dimuat: `{model_file}`")


# =========================================================
# Dynamic Model Label (BERBASIS METADATA)
# =========================================================
model_name = "Time-Series Model"
model_detail = ""

if metadata:
    model_name = metadata.get("model_name", model_name)
    model_detail = metadata.get("model_order", "")

st.caption(
    f"Time-Series Forecasting menggunakan {model_name}"
    + (f" {model_detail}" if model_detail else "")
    + " | Fokus pada tren jangka menengah, bukan volatilitas jangka pendek"
)


# =========================================================
# Proses Prediksi (default 24 bulan)
# =========================================================
FORECAST_HORIZON = 24

forecast = model.forecast(steps=FORECAST_HORIZON)

forecast_df = pd.DataFrame({
    "Bulan": pd.date_range(
        start=pd.Timestamp.today().to_period("M").to_timestamp(),
        periods=FORECAST_HORIZON,
        freq="MS"
    ),
    "Harga Prediksi (USD)": forecast.values
})


# =========================================================
# Visualisasi
# =========================================================
st.subheader("📊 Hasil Prediksi Harga Bitcoin")

st.line_chart(
    forecast_df.set_index("Bulan")
)


# =========================================================
# Informasi Model
# =========================================================
st.subheader("ℹ️ Informasi Model")

st.markdown(
    f"""
    **Model**  
    {model_name} {model_detail}

    **Frekuensi Data**  
    Bulanan (Monthly Average Close Price)

    **Tujuan Model**  
    Analisis tren harga Bitcoin jangka menengah
    """
)

if metadata:
    st.markdown("**Periode Data Latih**")
    st.write(
        f"{metadata['train_period']['start']} "
        f"sampai {metadata['train_period']['end']}"
    )


# =========================================================
# Interpretasi Bisnis
# =========================================================
st.subheader("🧠 Interpretasi")

st.info(
    """
    Prediksi ini menunjukkan **arah tren harga Bitcoin dalam 24 bulan ke depan**.

    - Model difokuskan pada **tren jangka menengah**, bukan fluktuasi harian.
    - Lonjakan atau penurunan ekstrem **tidak sepenuhnya tertangkap** oleh model.
    - Cocok digunakan untuk **analisis strategis dan pengambilan keputusan jangka menengah**,
      bukan untuk trading harian.
    """
)


# =========================================================
# Footer
# =========================================================
st.markdown("---")
st.caption("Dikembangkan oleh Hans Darmawan • Proyek Time-Series Forecasting Bitcoin")
