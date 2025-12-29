import yfinance as yf
import pandas as pd
import os
import sys
from datetime import timedelta, date


# =========================
# Resolve project paths
# =========================
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASETS_DIR = os.path.join(PROJECT_DIR, "..", "Datasets")
DEFAULT_FILENAME = "output.csv"


def resolve_output_path(arg_path=None):
    """
    Resolve output path relative to project file location:
    - None → ../Datasets/output.csv
    - filename.csv → ../Datasets/filename.csv
    - path/to/file.csv → relative to project dir
    """
    if arg_path is None:
        return os.path.abspath(os.path.join(DATASETS_DIR, DEFAULT_FILENAME))

    if not os.path.isabs(arg_path):
        return os.path.abspath(os.path.join(DATASETS_DIR, arg_path))

    return arg_path


def fetch_btc_historical(output_csv):
    print("📥 Fetching BTC-USD historical data")
    print(f"📁 Output path: {output_csv}")

    btc = yf.Ticker("BTC-USD")

    # =========================
    # Case 1: CSV exists → append
    # =========================
    if os.path.exists(output_csv):
        print("📂 Existing dataset found, appending new data...")
        existing_df = pd.read_csv(output_csv, parse_dates=["date"])

        last_date = existing_df["date"].max().date()
        start_date = last_date + timedelta(days=1)
        end_date = date.today()

        if start_date > end_date:
            print("✅ Dataset already up to date")
            return existing_df

        df = btc.history(
            start=start_date.isoformat(),
            end=(end_date + timedelta(days=1)).isoformat(),
            interval="1d"
        )

        if df.empty:
            print("⚠️ No new data returned")
            return existing_df

        df = df.reset_index()

    # =========================
    # Case 2: CSV not exists → full history
    # =========================
    else:
        print("🆕 No dataset found, downloading full history")
        df = btc.history(period="max", interval="1d")
        df = df.reset_index()

    # =========================
    # Standardize schema
    # =========================
    df["Date"] = df["Date"].dt.date

    df = df.rename(columns={
        "Date": "date",
        "Open": "open",
        "High": "high",
        "Low": "low",
        "Close": "close",
        "Volume": "volume"
    })

    df = df[["date", "open", "high", "low", "close", "volume"]]

    # =========================
    # Save
    # =========================
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    if os.path.exists(output_csv):
        final_df = pd.concat([existing_df, df], ignore_index=True)
        final_df = (
            final_df
            .drop_duplicates(subset=["date"])
            .sort_values("date")
        )
    else:
        final_df = df

    final_df.to_csv(output_csv, index=False)

    print(f"✅ Saved successfully")
    print(f"📊 Rows: {len(final_df)}")
    print(f"📅 Date range: {final_df['date'].min()} → {final_df['date'].max()}")

    return final_df


if __name__ == "__main__":
    """
    Usage:
      python get_data.py
      python get_data.py btc_daily.csv
      python get_data.py /absolute/path/btc.csv
    """

    output_arg = sys.argv[1] if len(sys.argv) > 1 else None
    output_csv = resolve_output_path(output_arg)

    fetch_btc_historical(output_csv)
