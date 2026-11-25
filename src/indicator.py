import pandas as pd

def evaluate_indicator(df: pd.DataFrame) -> bool:
    """
    Placeholder for the client's custom Python / PineScript indicator logic.
    Returns True when the indicator condition holds true on the latest closed bar.
    """
    if len(df) < 50:
        return False

    # Example vectorized condition: Fast EMA crosses above Slow EMA + RSI/Volume filter
    ema_fast = df["close"].ewm(span=9, adjust=False).mean()
    ema_slow = df["close"].ewm(span=21, adjust=False).mean()

    bullish_cross = (ema_fast.iloc[-2] <= ema_slow.iloc[-2]) and (
        ema_fast.iloc[-1] > ema_slow.iloc[-1]
    )
    return bool(bullish_cross)