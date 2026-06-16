import os
import sys

# NOTE: KITE_API_KEY, KITE_API_SECRET, and KITE_ACCESS_TOKEN are not currently used.
# The application uses yfinance for market data instead of Kite API.
# If you need to integrate Kite API in the future, add these back:
# KITE_API_KEY = os.getenv("KITE_API_KEY")
# KITE_API_SECRET = os.getenv("KITE_API_SECRET")
# KITE_ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError(
        "DATABASE ERROR: DB_URL environment variable not set. "
        "Please configure your .env file with database credentials."
    )

TOP_N = int(os.getenv("TOP_N", "10"))

SCAN_INTERVAL_MIN = int(
    os.getenv("SCAN_INTERVAL_MIN", "15")
)