from scanner.engine import run_scan
from database.storage import init_db, save
from tabulate import tabulate
from datetime import datetime
import schedule
import time
import os
from sqlalchemy import create_engine

def main():
    DB_URL = os.environ["DB_URL"]
    engine = create_engine(DB_URL)
    print("Database initialized successfully")

    def job():
        rows = run_scan()

        print("\nSCAN:", datetime.now())
        print(tabulate(rows, headers="keys"))

        payload = []
        for r in rows:
            payload.append({
                "scan_time": datetime.now().isoformat(),
                "symbol": r["symbol"],
                "score": r["score"],
                "close": r["close"],
                "dma30": r.get("dma30"),
                "rsi": r["rsi"],
                "macd": r["macd"]
            })

        save(payload)

    # run once immediately
    job()
    # schedule every 15 min
    schedule.every(15).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()