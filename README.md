# Fast API Stealth Scraper

A high-performance, asynchronous Python scraper using TLS fingerprinting to reliably extract e-commerce catalog data from WAF-protected Shopify endpoints. 

### Key Features
* **TLS Fingerprinting:** Uses `curl_cffi` to spoof modern browser TLS/JA3 handshakes, bypassing standard Cloudflare/anti-bot blocks.
* **Producer/Consumer Concurrency:** Async worker pool scales requests efficiently without blocking.
* **Auto-Recovery:** Built-in exponential backoff gracefully handles `curl: (28)` connection timeouts and 429 rate limits.
* **Dual Sinks:** Simultaneously persists flattened data to an automated SQLite schema (`products.db`) and a clean CSV file (`products.csv`).

### Quickstart

```bash
# Clone the repository
git clone [https://github.com/yourusername/fast-api-stealth-scraper.git](https://github.com/yourusername/fast-api-stealth-scraper.git)
cd fast-api-stealth-scraper

# Set up virtual environment and install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run the pipeline
python3 main.py
