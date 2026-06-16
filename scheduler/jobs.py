import schedule
import time

from scanner.engine import run_scan
from database.storage import save
from tabulate import tabulate
from datetime import datetime
from logger_config import get_logger

logger = get_logger(__name__)


def job():

    rows = run_scan()

    logger.info(f"Completed scan at {datetime.now()} - found {len(rows)} opportunities")

    save([
        {
            "scan_time": datetime.now().isoformat(),
            "symbol": r["symbol"],
            "score": r["score"],
            "close": r["close"],
            "dma30": r.get("dma30", None),
            "rsi": r["rsi"],
            "macd": r["macd"]
        }
        for r in rows
    ])


def start_scheduler():

    job()

    schedule.every(15).minutes.do(job)

    while True:

        schedule.run_pending()

        time.sleep(1)