from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Float,
    Integer,
    String,
    UniqueConstraint,
    JSON,
)

from sqlalchemy.orm import declarative_base

from datetime import datetime

Base = declarative_base()


class CoinHistory(Base):
    """
    Stores daily historical price data retrieved from CoinGecko.
    Each record represents a coin on a specific date.
    """

    __tablename__ = "coin_history"

    id = Column(Integer, primary_key=True)

    coin_id = Column(String(100), nullable=False)

    reference_date = Column(Date, nullable=False)

    price_usd = Column(Float, nullable=True)

    raw_payload = Column(JSON, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("coin_id", "reference_date", name="uq_coin_date"),
    )


class CoinMonthlyStats(Base):
    """
    Stores aggregated monthly statistics for a coin,
    including the minimum and maximum prices recorded
    during the month.
    """

    __tablename__ = "coin_monthly_stats"

    id = Column(Integer, primary_key=True)

    coin_id = Column(String(100), nullable=False)

    year = Column(Integer, nullable=False)

    month = Column(Integer, nullable=False)

    min_price = Column(Float, nullable=True)

    max_price = Column(Float, nullable=True)

    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("coin_id", "year", "month", name="uq_coin_month"),
    )