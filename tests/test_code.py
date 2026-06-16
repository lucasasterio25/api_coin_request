from app.services.downloader import *
from datetime import date

def test_date_coin():
    date = '2026-01-01'
    downloader = CoinExtraction()
    result = downloader.download_day('bitcoin', date, store_db=False)
    assert result.reference_date.isoformat() == date