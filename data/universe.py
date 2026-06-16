"""
Stock universe - list of symbols to scan
"""

def get_universe():
    """
    Returns list of NSE stock symbols to scan.
    Can be extended to load from database or external source.
    """
    # NSE Nifty 50 stocks as default universe
    universe = [
        "RELIANCE.NS", "TCS.NS", "INFY.NS", "HINDUNILVR.NS", "ICICIBANK.NS",
        "HDFC.NS", "LT.NS", "MARUTI.NS", "AXISBANK.NS", "SBIN.NS",
        "BHARTIARTL.NS", "BAJAJFINSV.NS", "ITC.NS", "ASIANPAINT.NS", "HCLTECH.NS",
        "WIPRO.NS", "JSWSTEEL.NS", "TECHM.NS", "SUNPHARMA.NS", "POWERGRID.NS",
        "NTPC.NS", "ONGC.NS", "COALINDIA.NS", "TATASTEEL.NS", "BAJAJ-AUTO.NS",
        "VOLTAS.NS", "M&M.NS", "TITAN.NS", "NESTLEIND.NS", "DRREDDY.NS",
        "CIPLA.NS", "EICHERMOT.NS", "GAIL.NS", "DLF.NS", "ADANIGREEN.NS",
        "ADANIPORTS.NS", "APOLLOHOSP.NS", "BIOCON.NS", "BRITANNIA.NS", "CUMMINSIND.NS",
        "DABUR.NS", "DIVISLAB.NS", "GODREJCP.NS", "GRASIM.NS", "HAVELLS.NS",
        "HDBANK.NS", "INDIGO.NS", "INDUSINDBK.NS", "KOTAKBANK.NS", "LUPIN.NS"
    ]
    return universe


def add_custom_universe(symbols):
    """
    Override universe with custom list of symbols
    """
    return symbols
