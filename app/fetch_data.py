from openbb import obb
import psycopg2
import os
import json
from datetime import date
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# List of tickers to fetch
tickers = ["AAPL", "MSFT", "TSLA"]
records = []

# Fetch each ticker's data
for ticker in tickers:
    try:
        result = obb.equity.price.historical(symbol=ticker, provider="yfinance", period="1d")
        df = result.to_df()

        if df is not None and not df.empty:
            last_row = df.iloc[-1]

            record = {
                "fetch_date": date.today(),
                "metric_name": f"{ticker}_price",
                "metric_value": float(last_row["close"]),
                "metadata": {
                    "open": float(last_row["open"]) if "open" in df.columns else None,
                    "high": float(last_row["high"]) if "high" in df.columns else None,
                    "low": float(last_row["low"]) if "low" in df.columns else None,
                    "volume": int(last_row["volume"]) if "volume" in df.columns else None,
                }
            }
            records.append(record)
        else:
            print(f"⚠️ No data for {ticker}")
    except Exception as e:
        print(f"⚠️ Error fetching {ticker}: {e}")

# Insert into PostgreSQL
try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    for r in records:
        cur.execute("""
            INSERT INTO daily_metrics (fetch_date, metric_name, metric_value, metadata)
            VALUES (%s, %s, %s, %s)
        """, (
            r["fetch_date"],
            r["metric_name"],
            r["metric_value"],
            json.dumps(r["metadata"]),
        ))

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Data inserted into database.")
except Exception as e:
    print("❌ Database error:", e)
