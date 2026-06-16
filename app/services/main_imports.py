# file used to import modules and make code clear
import typer

from datetime import datetime

from app.services.downloader import CoinExtraction

from app.database.init_db import create_tables

from app.services.processor import CoinETL

from app.services.downloader import CoinExtraction

from app.database.connection import get_session

from app.database.models import CoinHistory

from app.database.repository import CoinData

from app.database.connection import get_session
