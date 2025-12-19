import os
import time
import requests
import pandas as pd
from datetime import datetime, timezone
from dotenv import load_dotenv

# =========================
# Load secret (AMAN)
# =========================
load_dotenv()

CMC_API_KEY = os.getenv("CMC_API_KEY")
if not CMC_API_KEY:
    raise RuntimeError("CMC_API_KEY tidak ditemukan. Pastikan ada di .env atau env var.")

# =========================
# Config
# =========================
URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/ohlcv/historical"
HEADERS = {
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": CMC_API_KEY
}

# =========================
# Function
# =========================
def fetch_bitcoin_prices(
    start_date: str | None = None,
    end_date: str | None = None,
    output_csv: str = "btc_price.csv",
    sleep_sec: float = 1.1
):
    """
    Tarik harga BTC harian dari CoinMarketCap (AMAN)
    - start_date None → dari 2010-01-01
    - end_date None → sampai hari ini
    """

    if not start_date:
        start_date = "2010-01-01"

    if not end_date:
        end_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"📥 Tarik BTC dari {start_date} sampai {end_date}")

    params = {
        "symbol": "BTC",
        "time_start": start_date,
        "time_end": end_date,
        "interval": "daily",
        "convert": "USD"
    }

    r = requests.get(
        URL,
        headers=HEADERS,
        params=params,
        timeout=30
    )
    r.raise_for_status()

    data = r.json()["data"]["quotes"]

    rows = []
    for q in data:
        rows.append({
            "date": q["timestamp"][:10],
            "price_usd": q["quote"]["USD"]["close"],
            "market_cap": q["quote"]["USD"]["market_cap"],
            "volume": q["quote"]["USD"]["volume"]
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    df.to_csv(output_csv, index=False)

    print(f"✅ Selesai | {len(df)} baris")
    print(f"📄 File  : {output_csv}")
    print(f"📅 Range : {df['date'].min().date()} → {df['date'].max().date()}")

    time.sleep(sleep_sec)
    return df


# =========================
# CLI
# =========================
if __name__ == "__main__":
    fetch_bitcoin_prices(
        start_date=None,
        end_date=None,
        output_csv="data/btc_price.csv"
    )
