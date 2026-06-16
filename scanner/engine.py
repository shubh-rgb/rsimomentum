from indicators.technicals import add
from ranking.scorer import score
from config import TOP_N
from data.universe import get_universe
from data.fetcher import fetch_batch
from datetime import datetime
from logger_config import get_logger

logger = get_logger(__name__)

def run_scan():
    universe = get_universe()   # now from DB (not CSV)
    results = []
    # 🔥 FETCH IN BATCH (NOT LOOP PER SYMBOL)
    price_data = fetch_batch(universe)

    for symbol, df in price_data.items():
        try:
            df = add(df)

            results.append({
                "scan_time": datetime.now().isoformat(),
                "symbol": symbol,
                "score": score(df),
                "close": float(df["Close"].iloc[-1]),
                "rsi": float(df["RSI"].iloc[-1]),
                "macd": float(df["MACD"].iloc[-1]),
                "dma30": float(df.get("DMA30", [0]).iloc[-1]) if "DMA30" in df else None
            })
        except Exception as e:
            logger.warning(f"Failed to process {symbol}: {e}", exc_info=True)
            continue

    return sorted(results, key=lambda x: x["score"], reverse=True)[:TOP_N]