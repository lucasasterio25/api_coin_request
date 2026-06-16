# Crypto Historical Data Pipeline

## Project Structure
## Project Structure

```text
crypto-exam/
│
├── app/
│   ├── config.py
│   ├── logger.py
│   │
│   ├── coingecko/
│   │   ├── client.py
│   │   └── schemas.py
│   │
│   ├── database/
│   │   ├── connection.py
│   │   ├── init_db.py
│   │   ├── models.py
│   │   └── repository.py
│   │
│   └── services/
│       ├── downloader.py
│       └── processor.py
│
├── data/
├── logs/
├── tests/
├── sql/
├── main.py
├── requirements.txt
├── docker-compose.yml
└── README.md
```



## Design Notes

In development, I chose to separe the program into three layers: 
API, service, and repository, ensuring that the application is 
manageable even when adding new cryptocurrencies and storage options.

CoinGecko Demo API came with certain limitations when requesting past data; 
the code was enhanced with error handling to optimize the user experience.

In this project I used Typer, that gives us:
- Simple CLI development
- Type validation
- Automatic help creation
- Better user experience than argparse

## Architecture

CoinGecko API
↓

CLI

↓
JSON Files

↓
PostgreSQL

↓
Monthly Aggregations

## Features

- Single day download
- Bulk reprocessing
- Parallel processing
- PostgreSQL persistence
- Monthly aggregations
- Structured logging
- Retry mechanism
- Dockerized database

## Limitation

While testing the CoinGecko Demo API I found that
historical data older than approximately two years
returns HTTP 401 responses due to plan limitations.

## Code format

In this project was used Black Formatter.

## Running

To run the complete application, a "run all" command was created in the python main file. It is necessary to start Docker before; the necessary commands are listed below.

Bash:
docker compose up -d
python main.py run-all


## Scheduling

0 3 * * * python main.py download \
  --coin bitcoin \
  --date $(date +\%F) \
  --store-db

0 3 * * * python main.py download \
  --coin ethereum \
  --date $(date +\%F) \
  --store-db

0 3 * * * python main.py download \
  --coin cardano \
  --date $(date +\%F) \
  --store-db
