# High-Throughput Multi-Timeframe Stock Scanner

A scalable, asynchronous Python scanning engine designed to evaluate custom technical indicators across **3,000+ equities** and **7 distinct timeframes** (`1h`, `2h`, `3h`, `5h`, `7h`, `1D`, `1W`) continuously with minimal API overhead.

## Architecture & Bottleneck Mitigation

Scanning 3,000+ tickers across 7 timeframes requires **21,000+ evaluations per scan cycle**. Naive sequential polling will hit broker/data-provider rate limits and suffer from severe latency. This framework solves that bottleneck through three core optimizations:

1. **Single-Fetch Multi-Timeframe Resampling:** Instead of making 7 separate API calls per ticker, the engine fetches base `1h` and `1D` OHLCV data once and locally resamples custom intervals (`2h`, `3h`, `5h`, `7h`, `1W`) in memory using vectorized Pandas operations—cutting API calls by **~70%**.
2. **Async I/O + Multiprocessing Hybrid:** Network-bound data fetching runs concurrently via `asyncio` / `aiohttp` with semaphore rate-limit control, while CPU-bound indicator math executes across worker processes.
3. **Decoupled Indicator Logic:** Your proprietary Python/PineScript indicator logic lives in an isolated module (`src/indicator.py`), making it effortless to plug in, backtest, or update without touching the ingestion or alerting pipeline.

## Project Structure

```text
├── requirements.txt      # Core dependencies
└── src/
    ├── config.py         # Tickers, timeframes, rate limits, and scan intervals
    ├── data_engine.py    # Concurrent OHLCV fetcher & custom timeframe resampler
    ├── indicator.py      # Isolated custom indicator logic (PineScript -> Python port)
    └── scanner.py        # Main orchestrator, worker pool, and signal dispatcher