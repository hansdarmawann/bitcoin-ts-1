import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta

from model_loader import load_latest_model


# =========================
# Page Configuration
# =========================
st.set_page_config(
    page_title="Bitcoin Price Prediction",
    page_icon="📈",
    layout="centered"
)

st.title("📈 Monthly Bitcoin (BTC) Price Prediction")
st.caption(
    "Time-Series Forecasting using SARIMA | "
    "Focus on medium-term trends, not short-term volatility"
)

# =========================
# Load the Latest Model
# ========================
with st.spinner("Loading latest model..."):
    model, metadata, model_file = load_latest_model(
        model_dir="models",
        model_key="sarima"
    )

st.success(f"Model successfully loaded: `{model_file}`")


# =========================
# Horizon Slider
# =========================
st.subheader("🔧 Prediction Settings")

forecast_horizon = st.slider(
    "Prediction Horizon (months)",
    min_value=6,
    max_value=36,
    value=6,
    step=6
)


# =========================
# Determine the start date of the forecast (SAFE)
# =========================
if metadata and "train_period" in metadata and "end" in metadata["train_period"]:
    last_train_date = pd.to_datetime(metadata["train_period"]["end"])
else:
    last_train_date = pd.to_datetime("today").replace(day=1)


# =========================
# Prediction Process
# ========================
forecast_values = model.forecast(steps=forecast_horizon)

forecast_dates = [
    last_train_date + relativedelta(months=i + 1)
    for i in range(forecast_horizon)
]

forecast_df = pd.DataFrame({
    "Date": forecast_dates,
    "Predicted Price (USD)": forecast_values.values
}).sort_values("Date")


# =========================
# Visualization (MAJOR FIX)
# =========================
st.subheader("📊 Prediction Results")

# ❗ Datetime MUST be index (not string)
chart_df = forecast_df.set_index("Date")[["Predicted Price (USD)"]]

st.line_chart(chart_df)


# =========================
# Model Information (MINIMAL)
# =========================
st.subheader("ℹ️ Model Information")

st.write("**Model Type:** SARIMA (auto-loaded)")
st.write(f"**Prediction Horizon:** {forecast_horizon} months")


# =========================
# Interpretation
# ========================
st.subheader("🧠 Interpretation")

st.info(
    f"""
    This forecast shows the **Bitcoin price trend direction for the next {forecast_horizon} months**.

    - The model focuses on **medium-term trends**, not daily fluctuations.
    - Longer horizons produce smoother trends, but uncertainty increases.
    - Not recommended for **short-term trading**.
    """
)


# =========================
# Footer
# =========================
st.markdown("---")
st.caption("Developed by Hans Darmawan • Time-Series Forecasting Project")