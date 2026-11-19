import os
import csv
import sqlite3
from typing import List, Dict, Any

class CSVSink:
    """Handles streaming and batch export of flattened records to CSV files."""
    def __init__(self, filepath: str, fieldnames: list):
        self.filepath = filepath
        self.fieldnames = fieldnames
        self._file = None
        self._writer = None

    def open(self):
        file_exists = os.path.exists(self.filepath) and os.path.getsize(self.filepath) > 0
        self._file = open(self.filepath, mode="a", buffering=1, newline="", encoding="UTF-8")
        self._writer = csv.DictWriter(self._file, fieldnames=self.fieldnames)

        if not file_exists:
            self._writer.writeheader()

    def write_batch(self, records: List[dict]):
        if self._writer:
            self._writer.writerows(records)

    def close(self):
        if self._file:
            self._file.close()

class SQLSink:
    """Handles schema initialization and transactional batch persistence to SQLite databases."""
    def __init__(self, db_path: str):
        self.db_path = db_path

    def init_schema(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    product_id INTEGER,
                    title TEXT,
                    vendor TEXT,
                    price TEXT,
                    available INTEGER
                )
            """)
            conn.commit()

    def write_batch(self, records: List[Dict[str, Any]]):
        tuples = [
            (
                r.get("product_id"),
                r.get("title"),
                r.get("vendor"),
                r.get("price"),
                int(r.get("available", False)),
            )
            for r in records
        ]
        query = """
            INSERT INTO products (product_id, title, vendor, price, available)
            VALUES (?, ?, ?, ?, ?)
        """

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.executemany(query, tuples)
            conn.commit()
