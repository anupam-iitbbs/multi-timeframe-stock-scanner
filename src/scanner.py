import asyncio
import time
import logging
from typing import List, Dict
from src.config import ScannerConfig
from src.data_engine import DataEngine
from src.indicator import evaluate_indicator

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

async def scan_ticker(ticker: str, engine: DataEngine, timeframes: List[str]) -> List[Dict]:
    hits = []
    base_df = await engine.fetch_base_ohlcv(ticker)
    tf_data = engine.build_timeframes(base_df, timeframes)

    for tf, df in tf_data.items():
        if evaluate_indicator(df):
            hits.append({"ticker": ticker, "timeframe": tf, "close": round(df["close"].iloc[-1], 2)})
    return hits

async def run_scan_cycle(config: ScannerConfig) -> List[Dict]:
    start = time.perf_counter()
    semaphore = asyncio.Semaphore(config.max_concurrent_requests)
    engine = DataEngine(semaphore)

    tasks = [scan_ticker(ticker, engine, config.timeframes) for ticker in config.tickers]
    results = await asyncio.gather(*tasks)
    signals = [hit for sublist in results for hit in sublist]

    elapsed = time.perf_counter() - start
    logging.info(
        f"Scanned {len(config.tickers)} tickers across {len(config.timeframes)} timeframes "
        f"in {elapsed:.2f}s | Signals found: {len(signals)}"
    )
    return signals

if __name__ == "__main__":
    cfg = ScannerConfig()
    asyncio.run(run_scan_cycle(cfg))