from sqlalchemy import create_engine, text
import os

def initialize_database():
    db_url = os.getenv("DB_URL")  # comes from docker-compose
    engine = create_engine(
        db_url,
        echo=False,
        pool_pre_ping=True
    )

    with engine.begin() as conn:

        # ---------------- UNIVERSIY ----------------
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS universe (
            symbol TEXT PRIMARY KEY,
            company_name TEXT,
            sector TEXT,
            last_updated TIMESTAMP
        )
        """))

        # ---------------- SCANS ----------------
        conn.execute(text("""
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

        # ---------------- STOCK PRICES ----------------
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS stock_prices (
            id SERIAL PRIMARY KEY,
            symbol TEXT,
            candle_time TIMESTAMP,
            open DOUBLE PRECISION,
            high DOUBLE PRECISION,
            low DOUBLE PRECISION,
            close DOUBLE PRECISION,
            volume BIGINT
        )
        """))

    return engine