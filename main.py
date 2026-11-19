import asyncio
import argparse
import logging
from sinks import CSVSink, SQLSink
from parser import parse_shopify_products
from client import StealthClient, stealth_worker
from config import config

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

async def run_pipeline(concurrency: int, db_path: str, csv_path: str):
    """
    Orchestrates the asynchronous Producer/Consumer scraping pipeline.
    """
    tasks_queue = asyncio.Queue()
    results_queue = asyncio.Queue()

    # 1. Producer: Seed the task queue with URLs to scrape
    for page in range(1, 4):
        await tasks_queue.put({
            "url": config.BASE_URL.format(page=page),
            "headers": config.DEFAULT_HEADERS,
        })

    db_sink = SQLSink(db_path)
    csv_sink = CSVSink(csv_path, fieldnames=config.CSV_FIELDNAMES)

    if db_path:
        db_sink.init_schema()

    # 2. Consumer: Spawn stealth workers to process the queue
    async with StealthClient(impersonate="chrome120", max_concurrency=concurrency) as client:
        workers = [
            asyncio.create_task(stealth_worker(i, tasks_queue, results_queue, client))
            for i in range(concurrency)
        ]

        # Wait until all initial tasks are fully processed
        await tasks_queue.join()

        # Send termination signals (None) to shut down workers cleanly
        for _ in range(concurrency):
            await tasks_queue.put(None)

        await asyncio.gather(*workers)

    # 3. Extraction & Persistence: Parse the raw JSON responses into flat records
    raw_payloads = []
    while not results_queue.empty():
        raw_payloads.append(await results_queue.get())
        results_queue.task_done()

    all_records = []
    for payload in raw_payloads:
        if isinstance(payload, dict):
            all_records.extend(parse_shopify_products(payload))

    # 4. Export: Write to SQLite and CSV
    if db_path and all_records:
        db_sink.write_batch(all_records)

    if csv_path and all_records:
        csv_sink.open()
        csv_sink.write_batch(all_records)
        csv_sink.close()

    logging.info(f"Pipeline complete. Processed {len(all_records)} records.")

def main():
    parser = argparse.ArgumentParser(description="Fast API Stealth Scraper")
    parser.add_argument("--concurrency", type=int, default=config.DEFAULT_CONCURRENCY)
    parser.add_argument("--db", type=str, default=config.DEFAULT_DB_PATH)
    parser.add_argument("--csv", type=str, default=config.DEFAULT_CSV_PATH)
    args = parser.parse_args()

    asyncio.run(run_pipeline(args.concurrency, args.db, args.csv))

if __name__ == "__main__":
    main()
