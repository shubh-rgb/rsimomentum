"""
Batch data fetcher for price data using yfinance
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta


def fetch_batch(symbols, period="1y", interval="1d"):
    """
    Fetch price data for multiple symbols in batch.
    
    Args:
        symbols: List of stock symbols (e.g., ["RELIANCE.NS", "TCS.NS"])
        period: Time period for historical data (default: 1 year)
        interval: Candle interval (default: 1 day)
    
    Returns:
        Dictionary mapping symbol -> DataFrame with OHLCV data
    """
    price_data = {}
    
    for symbol in symbols:
        try:
            # Fetch data using yfinance
            df = yf.download(
                symbol,
                period=period,
                interval=interval,
                progress=False,
                timeout=10
            )
            
            if df is not None and len(df) > 0:
                # Ensure required columns exist
                df = df[["Open", "High", "Low", "Close", "Volume"]].copy()
                price_data[symbol] = df
                
        except Exception as e:
            # Log error but continue with next symbol
            print(f"Failed to fetch {symbol}: {e}")
            continue
    
    return price_data


def fetch_intraday(symbols, interval="60m"):
    """
    Fetch intraday data for symbols
    
    Args:
        symbols: List of stock symbols
        interval: Candle interval (default: 60 minutes)
    
    Returns:
        Dictionary mapping symbol -> DataFrame with intraday data
    """
    return fetch_batch(symbols, period="5d", interval=interval)


def fetch_recent(symbols, days=90):
    """
    Fetch recent N days of data for symbols
    
    Args:
        symbols: List of stock symbols
        days: Number of days to fetch (default: 90)
    
    Returns:
        Dictionary mapping symbol -> DataFrame
    """
    period = f"{days}d"
    return fetch_batch(symbols, period=period, interval="1d")
