import asyncio
import numpy as np
import pandas as pd
from typing import Dict

RESAMPLE_MAP = {
    "1h": "1h",
    "2h": "2h",
    "3h": "3h",
    "5h": "5h",
    "7h": "7h",
    "1D": "1D",
    "1W": "1W",
}

class DataEngine:
    def __init__(self, semaphore: asyncio.Semaphore):
        self.semaphore = semaphore

    async def fetch_base_ohlcv(self, ticker: str) -> pd.DataFrame:
        """
        Fetches base 1h OHLCV bars asynchronously.
        Replace mock generator with Polygon.io / Alpaca / Yahoo async client.
        """
        async with self.semaphore:
            await asyncio.sleep(0.01)  # Simulates non-blocking network I/O
            idx = pd.date_range(end=pd.Timestamp.utcnow(), periods=500, freq="1h")
            prices = 100 + np.cumsum(np.random.randn(len(idx)))
            return pd.DataFrame(
                {
                    "open": prices,
                    "high": prices + np.random.uniform(0.1, 1.5, len(idx)),
                    "low": prices - np.random.uniform(0.1, 1.5, len(idx)),
                    "close": prices + np.random.randn(len(idx)) * 0.5,
                    "volume": np.random.randint(10_000, 500_000, len(idx)),
                },
                index=idx,
            )

    @staticmethod
    def build_timeframes(base_df: pd.DataFrame, timeframes: list[str]) -> Dict[str, pd.DataFrame]:
        """Resamples base 1h OHLCV data into all target timeframes in memory."""
        resampled = {}
        ohlc_rules = {
            "open": "first",
            "high": "max",
            "low": "min",
            "close": "last",
            "volume": "sum",
        }
        for tf in timeframes:
            if tf == "1h":
                resampled[tf] = base_df
            else:
                resampled[tf] = (
                    base_df.resample(RESAMPLE_MAP[tf])
                    .agg(ohlc_rules)
                    .dropna()
                )
        return resampled