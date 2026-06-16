from sqlalchemy import func

from app.database.models import CoinHistory, CoinMonthlyStats

from app.logger import logger


class CoinData:
    """
    Handles database operations related to coin history
    and aggregated monthly statistics.
    """

    def __init__(self, session):
        """
        Creates a repository instance using the provided
        database session.
        """
        self.session = session

    def upsert_coin_history(self, coin_id, reference_date, price_usd, raw_payload):
        """
        Inserts a new coin history record or updates an
        existing one when the same coin and date are found.
        """

        existing = (
            self.session.query(CoinHistory)
            .filter(
                CoinHistory.coin_id == coin_id,
                CoinHistory.reference_date == reference_date,
            )
            .first()
        )

        if existing:

            existing.price_usd = price_usd
            existing.raw_payload = raw_payload

            logger.info(f"Updated {coin_id} " f"{reference_date}")

        else:

            history = CoinHistory(
                coin_id=coin_id,
                reference_date=reference_date,
                price_usd=price_usd,
                raw_payload=raw_payload,
            )

            self.session.add(history)

            logger.info(f"Inserted {coin_id} " f"{reference_date}")

        self.session.commit()

    def refresh_monthly_stats(self, coin_id, year, month):
        """
        Recalculates and stores the minimum and maximum prices
        for a specific coin and month.
        """

        result = (
            self.session.query(
                func.min(CoinHistory.price_usd), func.max(CoinHistory.price_usd)
            )
            .filter(
                CoinHistory.coin_id == coin_id,
                func.extract("year", CoinHistory.reference_date) == year,
                func.extract("month", CoinHistory.reference_date) == month,
            )
            .first()
        )

        min_price, max_price = result

        existing = (
            self.session.query(CoinMonthlyStats)
            .filter(
                CoinMonthlyStats.coin_id == coin_id,
                CoinMonthlyStats.year == year,
                CoinMonthlyStats.month == month,
            )
            .first()
        )

        if existing:

            existing.min_price = min_price
            existing.max_price = max_price

        else:

            monthly = CoinMonthlyStats(
                coin_id=coin_id,
                year=year,
                month=month,
                min_price=min_price,
                max_price=max_price,
            )

            self.session.add(monthly)

        self.session.commit()

        logger.info(f"Monthly stats refreshed " f"{coin_id}-{year}-{month}")

    def get_monthly_stats(self, coin_id: str):
        """
        Returns all monthly statistics available for a coin,
        ordered from the most recent period to the oldest.
        """

        return (
            self.session.query(CoinMonthlyStats)
            .filter(CoinMonthlyStats.coin_id == coin_id)
            .order_by(CoinMonthlyStats.year.desc(), CoinMonthlyStats.month.desc())
            .all()
        )