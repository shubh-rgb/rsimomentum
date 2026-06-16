from sqlalchemy import create_engine, text
import os

DB_URL = os.getenv("DB_URL")

engine = create_engine(
    DB_URL,
    echo=False,
    pool_pre_ping=True
)

# ---------------- INIT ----------------
def init_db():
    with engine.begin() as c:
        c.execute(text("""
        CREATE TABLE IF NOT EXISTS scans (
            id SERIAL PRIMARY KEY,
            scan_time TIMESTAMP,
            symbol TEXT,
            score DOUBLE PRECISION,
            close DOUBLE PRECISION,
            dma30 DOUBLE PRECISION,
            rsi DOUBLE PRECISION,
            macd DOUBLE PRECISION
        )
        """))

# ---------------- SAVE ----------------
def save(rows):
    with engine.begin() as c:
        for r in rows:
            c.execute(text("""
                INSERT INTO scans (
                    scan_time,
                    symbol,
                    score,
                    close,
                    dma30,
                    rsi,
                    macd
                ) VALUES (
                    :scan_time,
                    :symbol,
                    :score,
                    :close,
                    :dma30,
                    :rsi,
                    :macd
                )
            """), r)