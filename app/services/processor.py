from datetime import datetime
from datetime import timedelta

from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

from app.logger import logger

from app.services.downloader import CoinExtraction


class CoinETL:
    """
    Orchestrates the bulk processing of cryptocurrency data,
    handling both sequential and parallel downloads over a date range.
    """

    def __init__(self):
        """
        Initializes the processor with a CoinExtraction instance.
        """
        self.downloader = CoinExtraction()

    def generate_dates(self, start_date: str, end_date: str):
        """
        Generates all dates between a start and end date (inclusive)
        in YYYY-MM-DD format.
        """

        current = datetime.strptime(start_date, "%Y-%m-%d")

        end = datetime.strptime(end_date, "%Y-%m-%d")

        while current <= end:

            yield current.strftime("%Y-%m-%d")

            current += timedelta(days=1)

    def process_range(
        self, coin_id: str, start_date: str, end_date: str, store_db: bool = False
    ):
        """
        Processes a range of dates sequentially
        """

        dates = list(self.generate_dates(start_date, end_date))

        logger.info(f"Processing {len(dates)} days")

        for date in tqdm(dates, desc=f"{coin_id}"):

            try:

                self.downloader.download_day(
                    coin_id=coin_id, date=date, store_db=store_db
                )

            except Exception as ex:

                logger.error(f"Failed {date}: {ex}")

    def process_range_parallel(
        self,
        coin_id: str,
        start_date: str,
        end_date: str,
        workers: int = 5,
        store_db: bool = False,
    ):
        """
        Processes a range of dates in parallel using multiple threads,
        speeding up data collection for large date intervals.
        """

        dates = list(self.generate_dates(start_date, end_date))

        logger.info(
            f"Parallel processing " f"{len(dates)} days " f"with {workers} workers"
        )

        with ThreadPoolExecutor(max_workers=workers) as executor:

            futures = {
                executor.submit(
                    self.downloader.download_day, coin_id, date, store_db
                ): date
                for date in dates
            }

            for future in tqdm(
                as_completed(futures), total=len(futures), desc=f"{coin_id}"
            ):

                date = futures[future]

                try:

                    future.result()

                except Exception as ex:

                    logger.error(f"Failed {date}: {ex}")
