# parsers.py
from lxml import html
from typing import List, Dict, Any, Optional


def safe_extract(node: html.HtmlElement, xpath_query: str, default: Optional[str] = None) -> Optional[str]:
    """Safely extracts and cleans string content from an XPath query."""
    result = node.xpath(xpath_query)
    if result:
        return result[0].strip()
    return default


def parse_html_quotes(html_bytes: bytes) -> List[Dict[str, Any]]:
    """Parses raw HTML bytes into structured quote dictionaries via XPath."""
    tree = html.fromstring(html_bytes)
    cards = tree.xpath("//div[@class='quote']")

    records = []
    for card in cards:
        text = safe_extract(card, ".//span[@class='text']/text()")
        author = safe_extract(card, ".//small[@class='author']/text()")
        tags = [t.strip() for t in card.xpath(".//div[@class='tags']/a/text()")]

        records.append({
            "quote": text,
            "author": author,
            "tags": ", ".join(tags)
        })
    return records


def parse_api_quotes(data: dict) -> List[Dict[str, Any]]:
    """Parses structured JSON API responses into quote dictionaries."""
    records = []
    for item in data.get("quotes", []):
        author_data = item.get("author")
        author_name = author_data.get("name") if isinstance(author_data, dict) else str(author_data or "")

        records.append({
            "quote": item.get("text"),
            "author": author_name,
            "tags": ", ".join(item.get("tags", []))
        })

    return records
