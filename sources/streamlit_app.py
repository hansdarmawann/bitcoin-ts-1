import streamlit as st
import pandas as pd
import plotly.graph_objects as go
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
# Load Model
# =========================
with st.spinner("Memuat model terbaru..."):
    model, metadata, model_file = load_latest_model(
        model_dir="models",
        model_key="sarima"
    )

st.success(f"Model dimuat: `{model_file}`")

# =========================
# Slider Horizon (DI BAWAH)
# =========================
forecast_horizon = st.slider(
    "Horizon Prediksi (bulan)",
    min_value=6,
    max_value=36,
    step=6,
    value=6
)

# =========================
# Forecast
# =========================
forecast = model.forecast(steps=forecast_horizon)

# Buat datetime index (BULANAN)
last_date = model.data.dates[-1]
forecast_index = pd.date_range(
    start=last_date + pd.offsets.MonthBegin(1),
    periods=forecast_horizon,
    freq="MS"
)

forecast_df = pd.DataFrame(
    {"Predicted Price (USD)": forecast},
    index=forecast_index
)

# =========================
# Plot (DATETIME, BUKAN STRING)
# =========================
fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=forecast_df.index,        # ⬅ datetime index
        y=forecast_df.iloc[:, 0],
        mode="lines+markers",
        name="Prediksi Harga BTC"
    )
)

fig.update_layout(
    title="Prediksi Tren Harga Bitcoin",
    xaxis_title="Month – Year",
    yaxis_title="Harga (USD)",
    template="plotly_white",
    hovermode="x unified",
    xaxis=dict(
        type="date",                # ⬅ penting
        tickformat="%b %y"          # Jan 26
    )
)

st.plotly_chart(fig, use_container_width=True)

# =========================
# Interpretasi
# =========================
st.subheader("🧠 Interpretasi")
st.info(
    f"""
    Prediksi ini menunjukkan **arah tren harga Bitcoin untuk {forecast_horizon} bulan ke depan**.

    • Model difokuskan pada **tren jangka menengah**, bukan fluktuasi harian  
    • Horizon lebih panjang → tren lebih halus, ketidakpastian meningkat  
    • **Tidak disarankan untuk short-term trading**
    """
)

st.markdown("---")
st.caption("Dikembangkan oleh Hans Darmawan • Time-Series Forecasting Project")
