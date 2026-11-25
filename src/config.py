from dataclasses import dataclass, field
from typing import List

@dataclass
class ScannerConfig:
    # Target timeframes requested
    timeframes: List[str] = field(
        default_factory=lambda: ["1h", "2h", "3h", "5h", "7h", "1D", "1W"]
    )
    # Concurrency & rate-limiting controls
    max_concurrent_requests: int = 50
    scan_interval_seconds: int = 300  # Run every 5 minutes
    # Sample ticker list (replace with full 3,000+ symbol universe loader)
    tickers: List[str] = field(
        default_factory=lambda: ["AAPL", "MSFT", "NVDA", "TSLA", "AMD"]
    )