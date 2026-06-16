from datetime import date

from pydantic import BaseModel


class CoinHistory(BaseModel):
    """
    defined schema
    """

    coin_id: str

    reference_date: date

    price_usd: float | None

    raw_payload: dict
