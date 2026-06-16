import schedule
import time

from scanner.engine import run_scan
from database.storage import save
from tabulate import tabulate
from datetime import datetime


def job():

    rows = run_scan()

    print("\nSCAN", datetime.now())

    print(
        tabulate(
            rows,
            headers="keys"
        )
    )

    save([
        {
            "t": datetime.now().isoformat(),
            "s": r["symbol"],
            "sc": r["score"],
            "cl": r["close"],
            "r": r["rsi"],
            "m": r["macd"]
        }
        for r in rows
    ])


def start_scheduler():

    job()

    schedule.every(15).minutes.do(job)

    while True:

        schedule.run_pending()

        time.sleep(1)