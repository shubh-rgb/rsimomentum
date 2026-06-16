import os

KITE_API_KEY = os.getenv("KITE_API_KEY")
KITE_API_SECRET = os.getenv("KITE_API_SECRET")
KITE_ACCESS_TOKEN = os.getenv("KITE_ACCESS_TOKEN")

DB_URL = os.getenv(
    "DB_URL",
    "postgresql://trader:traderpass@localhost:5432/marketdb"
)

TOP_N = int(os.getenv("TOP_N", "10"))

SCAN_INTERVAL_MIN = int(
    os.getenv("SCAN_INTERVAL_MIN", "15")
)