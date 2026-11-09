from dataclasses import dataclass, field
from typing import Dict, List 

@dataclass
class EngineConfig:

    DEFAULT_CONCURRENCY: int = 3
    DEFAULT_DB_PATH: str = "output.db"
    DEFAULT_CSV_PATH: str = "output.csv"
    REQUEST_TIMEOUT: float = 5.0
    MAX_RETRIES: int = 3
    DEFAULT_HEADERS: Dict[str, str] = field(
        default_factory=lambda: {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
    )
    CSV_FIELDNAMES: List[str] = field(
        default_factory=lambda: ["quote", "author", "tags"]
    )
    BASE_URL: str = "https://quotes.toscrape.com/page/{page}/"


config = EngineConfig()
