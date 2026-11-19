from typing import List, Dict, Any

def parse_shopify_products(data: dict) -> List[Dict[str, Any]]:
    """
    Normalizes complex Shopify /products.json payloads into flat product dictionaries 
    ready for database insertion and CSV export.
    """
    records = []
    for item in data.get("products", []):
        variants = item.get("variants") or []
        first_variant = variants[0] if variants else {}

        records.append({
            "product_id": item.get("id"),
            "title": item.get("title", "").strip(),
            "vendor": item.get("vendor", "").strip(),
            "price": first_variant.get("price", "0.00"),
            "available": bool(first_variant.get("available", False)),
        })

    return records
