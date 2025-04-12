import psycopg2
import os
from dotenv import load_dotenv
load_dotenv()

def insert_metrics(metrics):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    for metric in metrics:
        cur.execute(
            "INSERT INTO daily_metrics (fetch_date, metric_name, metric_value, metadata) VALUES (CURRENT_DATE, %s, %s, %s)",
            (metric["name"], metric["value"], {})
        )
    conn.commit()
    cur.close()
    conn.close()

def get_latest_metrics():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    cur.execute("SELECT metric_name, metric_value FROM daily_metrics WHERE fetch_date = CURRENT_DATE")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

def save_llm_output(summary, recs):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO daily_recommendations (for_date, summary, recommendations) VALUES (CURRENT_DATE, %s, %s)",
        (summary, recs)
    )
    conn.commit()
    cur.close()
    conn.close()

def metrics_exist_for_today():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM daily_metrics WHERE fetch_date = CURRENT_DATE LIMIT 1")
    exists = cur.fetchone() is not None
    cur.close()
    conn.close()
    return exists
