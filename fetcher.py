import httpx
from datetime import datetime, timedelta
from typing import Optional


class MarketFetcher:
    def __init__(
        self,
        exchange_api_key: str,
        currency_cache_ttl: timedelta = timedelta(minutes=10),
        gold_cache_ttl: timedelta = timedelta(minutes=2),
    ):
        self.exchange_api_key = exchange_api_key

        # Caches
        self._currency_cache: Optional[dict] = None
        self._currency_cache_time: Optional[datetime] = None
        self._gold_cache: Optional[dict] = None
        self._gold_cache_time: Optional[datetime] = None

        self.currency_cache_ttl = currency_cache_ttl
        self.gold_cache_ttl = gold_cache_ttl

        # HTTP clients
        self._currency_client = httpx.AsyncClient(timeout=10.0)  # Increased for reliability
        self._gold_client = httpx.AsyncClient(
            timeout=10.0,
            headers={"User-Agent": "Mozilla/5.0 (compatible; MarketTrackerBot/1.0)"},
            follow_redirects=True,
        )

    # -------------------- INTERNAL --------------------

    async def _get_all_rates(self) -> dict:
        now = datetime.utcnow()

        if (
            self._currency_cache
            and self._currency_cache_time
            and (now - self._currency_cache_time) < self.currency_cache_ttl
        ):
            return self._currency_cache

        url = f"https://v6.exchangerate-api.com/v6/{self.exchange_api_key}/latest/USD"
        try:
            resp = await self._currency_client.get(url)
            resp.raise_for_status()
            data = resp.json()

            if data.get("result") != "success":
                raise ValueError("API returned error")

            self._currency_cache = data["conversion_rates"]
            self._currency_cache_time = now
            return self._currency_cache
        except Exception as e:
            print(f"Failed to fetch currency rates: {e}")
            # Return cached data if available, even if stale
            if self._currency_cache:
                return self._currency_cache
            raise

    # -------------------- CURRENCIES --------------------

    async def get_usd_rub(self) -> Optional[float]:
        return (await self._get_all_rates()).get("RUB")

    async def get_usd_jpy(self) -> Optional[float]:
        return (await self._get_all_rates()).get("JPY")

    async def get_usd_eur(self) -> Optional[float]:
        return (await self._get_all_rates()).get("EUR")

    async def get_usd_uzs(self) -> Optional[float]:
        return (await self._get_all_rates()).get("UZS")

    async def get_usd_aud(self) -> Optional[float]:
        return (await self._get_all_rates()).get("AUD")

    async def get_usd_gbp(self) -> Optional[float]:
        return (await self._get_all_rates()).get("GBP")

    async def get_custom_pair(self, base: str, target: str) -> Optional[float]:
        base = base.upper().strip()
        target = target.upper().strip()

        if base == target:
            return 1.0

        try:
            rates = await self._get_all_rates()

            # Direct: USD → XXX
            if base == "USD" and target in rates:
                rate = rates.get(target)
                return round(rate, 6) if rate is not None else None

            # Inverse: XXX → USD
            if target == "USD" and base in rates:
                rate_base = rates.get(base)
                if rate_base and rate_base != 0:
                    return round(1 / rate_base, 6)

            # Cross rate: XXX → YYY (via USD)
            if base in rates and target in rates:
                rate_base = rates[base]
                rate_target = rates[target]
                if rate_base and rate_base != 0:
                    return round(rate_target / rate_base, 6)

            # Fallback to free public API
            url = f"https://api.exchangerate.host/convert?from={base}&to={target}"
            resp = await self._currency_client.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()

            if data.get("success"):
                return round(data["result"], 6)

        except Exception as e:
            print(f"Custom pair {base}/{target} failed: {e}")

        return None

    # -------------------- METALS --------------------

    async def get_latest_gold(self) -> dict:
        now = datetime.utcnow()

        if (
            self._gold_cache
            and self._gold_cache_time
            and (now - self._gold_cache_time) < self.gold_cache_ttl
        ):
            return self._gold_cache

        url = "https://data-asg.goldprice.org/dbXRates/USD"
        try:
            resp = await self._gold_client.get(url)
            resp.raise_for_status()
            data = resp.json()

            item = data["items"][0]

            gold_data = {
                "gold_usd": item["xauPrice"],
                "silver_usd": item["xagPrice"],
                "gold_change": item["chgXau"],
                "silver_change": item["chgXag"],
                "gold_pct": item["pcXau"],
                "silver_pct": item["pcXag"],
                "timestamp": data["date"],
            }

            self._gold_cache = gold_data
            self._gold_cache_time = now
            return gold_data

        except Exception as e:
            print(f"Failed to fetch gold/silver prices: {e}")
            if self._gold_cache:
                return self._gold_cache
            raise

    async def get_gold_price(self) -> Optional[float]:
        data = await self.get_latest_gold()
        return data.get("gold_usd")

    async def get_silver_price(self) -> Optional[float]:
        data = await self.get_latest_gold()
        return data.get("silver_usd")

    # -------------------- LIFECYCLE --------------------

    async def prewarm(self):
        try:
            await self._get_all_rates()
        except Exception as error:
            print(f"Currency prewarm failed: {error}")

        try:
            await self.get_latest_gold()
        except Exception as e:
            print(f"Gold prewarm failed: {e}")

    async def close(self):
        await self._currency_client.aclose()
        await self._gold_client.aclose()