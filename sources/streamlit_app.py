import streamlit as st
import pandas as pd
from pathlib import Path

# =========================================================
# Import model loader (robust for local & cloud)
# =========================================================
try:
    from sources.model_loader import load_latest_model
except ModuleNotFoundError:
    from model_loader import load_latest_model


# =========================================================
# Page configuration
# =========================================================
st.set_page_config(
    page_title="Prediksi Harga Bitcoin",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Prediksi Harga Bitcoin (BTC) Bulanan")

# =========================================================
# Resolve project paths
# =========================================================
BASE_DIR = Path(__file__).resolve().parents[1]
MODEL_DIR = BASE_DIR / "models"

# =========================================================
# Load latest model
# =========================================================
with st.spinner("Memuat model terbaru..."):
    model, metadata, model_file = load_latest_model(
        model_dir=str(MODEL_DIR),
        model_key="sarima"
    )

st.success(f"Model berhasil dimuat: `{model_file}`")

# =========================================================
# Dynamic model caption (from metadata)
# =========================================================
model_name = metadata.get("model_name", "Time-Series Model") if metadata else "Time-Series Model"
model_order = metadata.get("model_order", "") if metadata else ""

st.caption(
    f"Time-Series Forecasting menggunakan {model_name}"
    + (f" {model_order}" if model_order else "")
    + " | Fokus pada tren jangka menengah, bukan volatilitas jangka pendek"
)

# =========================================================
# Forecast horizon control (slider BELOW chart requirement)
# =========================================================
forecast_horizon = st.slider(
    "Horizon Prediksi (bulan)",
    min_value=6,
    max_value=36,
    value=24,
    step=6
)

# =========================================================
# Forecasting
# =========================================================
forecast = model.forecast(steps=forecast_horizon)

# Generate Month-Year labels (Jan 26, Feb 26, ...)
start_date = pd.Timestamp.today().to_period("M").to_timestamp()
forecast_dates = pd.date_range(
    start=start_date,
    periods=forecast_horizon,
    freq="MS"
)

forecast_df = pd.DataFrame({
    "Bulan": forecast_dates.strftime("%b %y"),
    "Harga Prediksi (USD)": forecast.values
})

# =========================================================
# Visualization
# =========================================================
st.subheader("📊 Hasil Prediksi")

st.line_chart(
    forecast_df.set_index("Bulan")
)

# =========================================================
# Model information (NO RMSE exposed)
# =========================================================
st.subheader("ℹ️ Informasi Model")

st.write(f"**Model:** {model_name}")
if model_order:
    st.write(f"**Parameter:** {model_order}")

if metadata and "train_period" in metadata:
    st.write(
        f"**Periode Data Latih:** "
        f"{metadata['train_period']['start']} "
        f"sampai {metadata['train_period']['end']}"
    )

# =========================================================
# Business interpretation
# =========================================================
st.subheader("🧠 Interpretasi")

st.info(
    f"""
    Prediksi ini menunjukkan **arah tren harga Bitcoin untuk {forecast_horizon} bulan ke depan**.

    - Model difokuskan pada **tren jangka menengah**
    - Fluktuasi ekstrem harian **tidak sepenuhnya tertangkap**
    - Cocok untuk **analisis strategis**, bukan trading jangka pendek
    """
)

# =========================================================
# Footer
# =========================================================
st.markdown("---")
st.caption("Dikembangkan oleh Hans Darmawan • Proyek Time-Series Forecasting")
