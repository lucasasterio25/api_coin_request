import json

from pathlib import Path
from datetime import datetime
from datetime import timedelta

from app.logger import logger

from app.coingecko.client import CoinGeckoClient

from app.coingecko.schemas import CoinHistory

from app.database.connection import get_session

from app.database.repository import CoinData


class CoinExtraction:
    """
    Handles the process of downloading cryptocurrency data,
    saving it locally, and optionally storing it in the database.
    """

    def __init__(self):
        """
        Creates a downloader instance with a configured
        CoinGecko client.
        """
        self.client = CoinGeckoClient()

    def download_day(
        self, coin_id: str, date: str, store_db: bool = False
    ) -> CoinHistory:
        """
        Downloads data for a specific coin and date, saves
        the result locally, and optionally persists it to
        the database.
        """

        self.validate_date(date)

        api_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d-%m-%Y")

        payload = self.client.get_history(coin_id, api_date)

        usd_price = payload.get("market_data", {}).get("current_price", {}).get("usd")

        coin_history = CoinHistory(
            coin_id=coin_id,
            reference_date=date,
            price_usd=usd_price,
            raw_payload=payload,
        )

        self.save_locally(coin_history)

        if store_db:
            self.persist_to_database(coin_history)

        return coin_history

    def save_locally(self, coin_history: CoinHistory):
        """
        Saves the API response JSON by coin and date.
        """

        directory = Path(f"data/{coin_history.coin_id}")

        directory.mkdir(parents=True, exist_ok=True)

        file_path = directory / f"{coin_history.reference_date}.json"

        with open(file_path, "w", encoding="utf-8") as file:

            json.dump(coin_history.raw_payload, file, indent=4, ensure_ascii=False)

        logger.info(f"Saved file {file_path}")

    def validate_date(self, date_str: str):
        """
        Checks whether the requested date is supported by
        the CoinGecko demo API.
        """

        requested_date = datetime.strptime(date_str, "%Y-%m-%d")

        oldest_allowed = datetime.now() - timedelta(days=365)

        if requested_date < oldest_allowed:

            raise ValueError(
                "Demo CoinGecko API only supports "
                "historical data up to 1 year."
            )

    def persist_to_database(self, coin_history):
        """
        Stores coin history data in the database and updates
        the corresponding monthly statistics.
        """

        session = get_session()
        try:

            repository = CoinData(session)

            repository.upsert_coin_history(
                coin_id=coin_history.coin_id,
                reference_date=coin_history.reference_date,
                price_usd=coin_history.price_usd,
                raw_payload=coin_history.raw_payload,
            )

            repository.refresh_monthly_stats(
                coin_id=coin_history.coin_id,
                year=coin_history.reference_date.year,
                month=coin_history.reference_date.month,
            )

        finally:
            session.close()