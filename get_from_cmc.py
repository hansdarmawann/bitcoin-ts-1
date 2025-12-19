import os
import sys
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
    start_date: str,
    end_date: str,
    output_csv: str,
    sleep_sec: float = 1.2
):
    """
    Tarik harga BTC harian dari CoinMarketCap (YEARLY SAFE)

    start_date & end_date WAJIB diisi (YYYY-MM-DD)
    """

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

    if r.status_code != 200:
        print("❌ ERROR:", r.json())
        r.raise_for_status()

    data = r.json()["data"]["quotes"]

    rows = []
    for q in data:
        rows.append({
            "date": q["timestamp"][:10],
            "open": q["quote"]["USD"]["open"],
            "high": q["quote"]["USD"]["high"],
            "low": q["quote"]["USD"]["low"],
            "close": q["quote"]["USD"]["close"],
            "volume": q["quote"]["USD"]["volume"],
            "market_cap": q["quote"]["USD"]["market_cap"]
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df.to_csv(output_csv, index=False)

    print(f"✅ Selesai | {len(df)} baris → {output_csv}")

    time.sleep(sleep_sec)
    return df


# =========================
# CLI ENTRYPOINT
# =========================
if __name__ == "__main__":

    # CLI usage:
    # python get_from_cmc.py 2024-01-01 2024-12-31

    if len(sys.argv) != 3:
        raise ValueError(
            "❌ Format salah.\n"
            "Gunakan:\n"
            "python get_from_cmc.py YYYY-MM-DD YYYY-MM-DD\n\n"
            "Contoh:\n"
            "python get_from_cmc.py 2024-01-01 2024-12-31"
        )

    start_date = sys.argv[1]
    end_date = sys.argv[2]

    year = start_date[:4]
    output_csv = f"data/btc/btc_{year}.csv"

    fetch_bitcoin_prices(
        start_date=start_date,
        end_date=end_date,
        output_csv=output_csv
    )
