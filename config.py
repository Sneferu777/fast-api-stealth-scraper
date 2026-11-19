from dataclasses import dataclass, field
from typing import Dict, List

@dataclass
class EngineConfig:
    """Centralized configuration for scraper behavior, target URLs, and I/O settings."""
    DEFAULT_CONCURRENCY: int = 3
    DEFAULT_DB_PATH: str = "products.db"
    DEFAULT_CSV_PATH: str = "products.csv"
    REQUEST_TIMEOUT: float = 10.0
    MAX_RETRIES: int = 3
    
    DEFAULT_HEADERS: Dict[str, str] = field(
        default_factory=lambda: {
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
        }
    )
    
    CSV_FIELDNAMES: List[str] = field(
        default_factory=lambda: ["product_id", "title", "vendor", "price", "available"]
    )
    
    # Target: Real-world Shopify JSON endpoint
    BASE_URL: str = "https://www.allbirds.com/products.json?limit=5&page={page}"

config = EngineConfig()
