import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")  # Or paste it directly

schema = """
CREATE TABLE IF NOT EXISTS daily_metrics (
    id SERIAL PRIMARY KEY,
    fetch_date DATE,
    metric_name TEXT,
    metric_value NUMERIC,
    metadata JSONB
);

CREATE TABLE IF NOT EXISTS daily_recommendations (
    id SERIAL PRIMARY KEY,
    for_date DATE,
    summary TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);
"""

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(schema)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ Tables created successfully.")
except Exception as e:
    print("❌ Error:", e)
