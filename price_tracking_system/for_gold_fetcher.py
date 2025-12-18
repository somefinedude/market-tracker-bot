import httpx
from datetime import datetime
from bs4 import BeautifulSoup

async def get_latest_gold():
    global _gold_cache, _gold_cache_time

    now = datetime.utcnow()
    if _gold_cache and _gold_cache_time and (now - _gold_cache_time) < CACHE_TTL:
        return _gold_cache
    resp = await _client.get("https://www.goldprice.org/")
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")
    price_span = soup.select_one("span.gpoticker-price")
    if not price_span:
        raise RuntimeError("Gold price element not found")
    price_oz = float(price_span.text.replace(",", ""))

    _gold_cache = {
        "price_oz_usd": price_oz,
        "price_g_usd": round(price_oz / 31.1035, 2),
        "updated": now.strftime("%H:%M:%S UTC")
    }
    _gold_cache_time = now
    return _gold_cache