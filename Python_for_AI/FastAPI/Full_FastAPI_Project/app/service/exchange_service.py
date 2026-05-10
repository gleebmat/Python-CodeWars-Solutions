from decimal import Decimal
from typing import Dict, Tuple
import aiohttp
from fastapi import requests

from app.enum import CurrencyEnum


FALLBACK_RATES: Dict[Tuple[str, str], Decimal] = {
    (CurrencyEnum.USD, CurrencyEnum.RUB): Decimal(str(95.0)),  # Курс обмена USD->RUB
    (CurrencyEnum.USD, CurrencyEnum.EUR): Decimal(str(0.92)),  # Курс обмена USD->EUR
    (CurrencyEnum.EUR, CurrencyEnum.RUB): Decimal(str(103.26)),  # Курс обмена EUR->RUB
    (CurrencyEnum.RUB, CurrencyEnum.USD): Decimal(str(0.0105)),  # Курс обмена RUB->USD
    (CurrencyEnum.EUR, CurrencyEnum.USD): Decimal(str(1.087)),  # Курс обмена EUR->USD
    (CurrencyEnum.RUB, CurrencyEnum.EUR): Decimal(str(0.0097)),  # Курс обмена RUB->EUR
}


async def get_exchange_rate(base: CurrencyEnum, target: CurrencyEnum) -> Decimal:
    url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base}.json"

    timeout = aiohttp.ClientTimeout(total=5.0)

    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url) as response:
                response.raise_for_status()
                data = await response.json()
                base_map = data.get(base, {})
                rate = base_map.get(target)

        if rate is not None and isinstance(rate, (int, float)):
            return Decimal(rate)
        raise KeyError("Rate not found")
    except Exception:
        return FALLBACK_RATES.get((base, target), Decimal(1))
