import yfinance as yf
import pandas as pd
import os
import sys

def fetch_btc_historical(start_date, end_date, output_csv):
    print(f"📥 Ambil BTC historical {start_date} → {end_date}")

    btc = yf.Ticker("BTC-USD")
    df = btc.history(start=start_date, end=end_date, interval="1d")

    df = df.reset_index()
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

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)

    print(f"✅ Selesai → {output_csv}")
    print(f"📊 Rows: {len(df)}")

    return df


if __name__ == "__main__":
    # CLI usage:
    # python get_data.py 2014-09-17 2025-12-19 data/btc/btc_2015_2025.csv

    if len(sys.argv) != 4:
        raise ValueError(
            "Gunakan:\n"
            "python get_data.py START_DATE END_DATE OUTPUT_CSV"
        )

    start_date = sys.argv[1]
    end_date = sys.argv[2]
    output_csv = sys.argv[3]

    fetch_btc_historical(start_date, end_date, output_csv)
