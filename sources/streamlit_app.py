import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

# ✅ Local import (SAFE for Streamlit Cloud)
from model_loader import load_latest_model


# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Prediksi Harga Bitcoin",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Prediksi Harga Bitcoin (BTC) Bulanan")


# =========================
# Load Latest Model
# =========================
with st.spinner("Memuat model terbaru..."):
    model, metadata, model_file = load_latest_model(
        model_dir="models",
        model_key="sarima"
    )

st.success(f"Model berhasil dimuat: `{model_file}`")


# =========================
# Model Info (Dynamic)
# =========================
model_name = metadata.get("model_name", "SARIMA") if metadata else "SARIMA"
model_order = metadata.get("order") if metadata else None
seasonal_order = metadata.get("seasonal_order") if metadata else None

model_desc = model_name
if model_order and seasonal_order:
    model_desc += f" {model_order}{seasonal_order}"

st.caption(
    f"Time-Series Forecasting menggunakan **{model_desc}** | "
    "Fokus pada tren jangka menengah, bukan volatilitas jangka pendek"
)


# =========================
# Forecast Horizon Slider
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
# Generate Forecast
# =========================
forecast = model.forecast(steps=forecast_horizon)

# Tentukan start date (bulan setelah data terakhir)
last_train_date = pd.to_datetime(metadata["train_period"]["end"])
dates = [
    last_train_date + relativedelta(months=i)
    for i in range(1, forecast_horizon + 1)
]

forecast_df = pd.DataFrame({
    "date": dates,
    "Predicted Price (USD)": forecast.values
})

# ✅ Month-Year label (chronological)
forecast_df["Month-Year"] = forecast_df["date"].dt.strftime("%b %y")
forecast_df = forecast_df.sort_values("date").set_index("Month-Year")


# =========================
# Visualization
# =========================
st.subheader("📊 Hasil Prediksi Harga Bitcoin")

st.line_chart(forecast_df[["Predicted Price (USD)"]])


# =========================
# Business Interpretation
# =========================
st.subheader("🧠 Interpretasi")

st.info(
    f"""
    Prediksi ini menunjukkan **arah tren harga Bitcoin untuk {forecast_horizon} bulan ke depan**.

    - Model difokuskan pada **tren jangka menengah**, bukan fluktuasi harian
    - Horizon lebih panjang menghasilkan **tren lebih halus**, namun ketidakpastian meningkat
    - **Tidak disarankan untuk short-term trading**
    """
)


# =========================
# Footer
# =========================
st.markdown("---")
st.caption("Dikembangkan oleh Hans Darmawan • Proyek Time-Series Forecasting Bitcoin")
