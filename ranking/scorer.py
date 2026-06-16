from logger_config import get_logger

logger = get_logger(__name__)


def score(df):
    # \"\"\"Calculate composite score based on technical indicators.\"\"\"
    try:
        r = df.iloc[-1]

        # Validate required columns
        required_columns = ['Close', 'DMA30', 'MACD', 'MACD_SIG', 'RSI', 'BB_UP', 'BB_DN']
        for col in required_columns:
            if col not in df.columns:
                raise KeyError(f"Required column '{col}' not found in data")

        s = 0

        if r['Close'] > r['DMA30']:
            s += 30

        if r['MACD'] > r['MACD_SIG']:
            s += 25

        if r['RSI'] > 55:
            s += 20

        if r['Close'] > (r['BB_UP'] + r['BB_DN']) / 2:
            s += 15

        return float(s)

    except KeyError as e:
        logger.error(f"Missing required technical indicator: {e}")
        return 0.0
    except Exception as e:
        logger.error(f"Error calculating score: {e}\", exc_info=True)
        return 0.0