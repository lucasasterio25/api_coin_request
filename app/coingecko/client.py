import requests

from tenacity import retry, stop_after_attempt, wait_exponential

from app.config import get_settings
from app.logger import logger


class CoinGeckoClient:
    """
    Simple client responsible for communicating with the
    CoinGecko API and retrieving cryptocurrency data.
    """

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self):
        """
        Creates an HTTP session and loads the application
        settings required for API requests.
        """

        self.settings = get_settings()

        self.session = requests.Session()

        self.session.headers.update({"accept": "application/json"})

    @retry(
        stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    def get_history(self, coin_id: str, date_str: str) -> dict:
        """
        Retrieves historical data for a cryptocurrency on a
        specific date. Requests are automatically retried if
        a temporary failure occurs.
        """

        url = f"{self.BASE_URL}" f"/coins/{coin_id}/history"

        params = {"date": date_str}

        logger.info(f"Requesting CoinGecko " f"{coin_id} {date_str}")

        params = {
            "date": date_str,
            "x_cg_demo_api_key": self.settings.coingecko_api_key,
        }

        logger.info(f"Calling URL: {url}")

        logger.info(f"Params: {list(params.keys())}")

        response = self.session.get(url, params=params, timeout=30)

        if response.status_code == 429:

            logger.warning("Rate limit reached.")

            raise Exception("CoinGecko rate limit")

        response.raise_for_status()

        return response.json()