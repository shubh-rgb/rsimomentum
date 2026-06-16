import pandas as pd
from sqlalchemy import create_engine, text
import os

engine = create_engine(
    os.getenv("DB_URL")
)

def load_stock_history(symbol):

    query = text("""
        SELECT *
        FROM scans
        WHERE symbol = :symbol
        ORDER BY scan_time
    """)

    return pd.read_sql(
        query,
        engine,
        params={"symbol": symbol}
    )