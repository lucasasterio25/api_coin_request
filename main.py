from app.services.main_imports import *
app = typer.Typer(help="API Request Lucas")

@app.command()
def health():
    """
    Checks if the application is up and running.
    """

    typer.echo("Application running successfully.")


@app.command()
def init_db():
    """
    Creates the database objects required to run the application.
    """

    create_tables()

    typer.echo("Database initialized.")


@app.command()
def download(
    coin: str = typer.Option(..., "--coin", help="Coin identifier"),
    date: str = typer.Option(..., "--date", help="Reference date YYYY-MM-DD"),
    store_db: bool = typer.Option(
        False, "--store-db", help="Persist data into PostgreSQL"
    ),
    overwrite: bool = typer.Option(False, help="Overwrite existing data"),
):
    """
    Downloads cryptocurrency data for a specific day
    and displays the returned information.
    """

    downloader = CoinExtraction()

    result = downloader.download_day(coin, date, store_db=store_db)

    typer.echo(f"""
        Coin: {result.coin_id}
        Date: {result.reference_date}
        USD Price: {result.price_usd}
        """)


@app.command()
def reprocess(coin: str, start_date: str, end_date: str):
    """
    Runs a simple reprocessing task for the given date range.
    """

    typer.echo(f"Reprocessing {coin}")

    typer.echo(f"Start: {start_date}")

    typer.echo(f"End: {end_date}")


@app.command()
def stats():
    """
    Shows the total number of records stored
    in the coin history table.
    """

    session = get_session()

    try:

        repository = CoinData(session)

        count = session.query(CoinHistory).count()

        typer.echo(f"Rows in coin_history: {count}")

    finally:

        session.close()


@app.command()
def reprocess(
    coin: str = typer.Option(...),
    start_date: str = typer.Option(...),
    end_date: str = typer.Option(...),
    store_db: bool = typer.Option(False),
):
    """
    Reprocesses coin data for the selected date range.
    Results can optionally be saved to the database.
    """

    processor = CoinETL()

    processor.process_range(
        coin_id=coin, start_date=start_date, end_date=end_date, store_db=store_db
    )

    typer.echo("Processing completed.")


@app.command()
def reprocess_parallel(
    coin: str = typer.Option(...),
    start_date: str = typer.Option(...),
    end_date: str = typer.Option(...),
    workers: int = typer.Option(5),
    store_db: bool = typer.Option(False),
):
    """
    Reprocesses coin data using multiple workers
    to speed up larger workloads.
    """

    processor = CoinETL()

    processor.process_range_parallel(
        coin_id=coin,
        start_date=start_date,
        end_date=end_date,
        workers=workers,
        store_db=store_db,
    )

    typer.echo("Parallel processing completed.")


from sqlalchemy import text


@app.command()
def db_health():
    """
    Performs a quick database connectivity check.
    """

    session = get_session()
    try:
        session.execute(text("SELECT 1"))
        typer.echo("Database healthy")
    finally:
        session.close()


@app.command()
def show_monthly_stats(coin: str = typer.Option(..., "--coin", help="Coin identifier")):
    """
    Displays monthly minimum and maximum prices for the selected cryptocurrency.
    """

    session = get_session()

    try:

        repository = CoinData(session)

        stats = repository.get_monthly_stats(coin)

        if not stats:

            typer.echo(f"No statistics found for {coin}")
            return

        typer.echo("\nMonthly Statistics\n")

        typer.echo(
            f"{'Year':<8}" f"{'Month':<8}" f"{'Min Price':<15}" f"{'Max Price':<15}"
        )

        typer.echo("-" * 50)

        for row in stats:

            typer.echo(
                f"{row.year:<8}"
                f"{row.month:<8}"
                f"{row.min_price:<15.2f}"
                f"{row.max_price:<15.2f}"
            )

    finally:

        session.close()


@app.command()
def run_all(
    coin: str = typer.Option("bitcoin"),
    store_db: bool = typer.Option(True),
):
    """
    run all project in sequence... makes it easier to validate and show the solution
    """

    typer.echo("===================================")
    typer.echo("STEP 1 - Initializing database")
    typer.echo("===================================")
    db_health()

    create_tables()

    typer.echo("Database initialized.")

    typer.echo("\n===================================")
    typer.echo("STEP 2 - Downloading single day")
    typer.echo("===================================")

    downloader = CoinExtraction()

    downloader.download_day(
        coin_id=coin,
        date="2026-06-01",
        store_db=store_db,
    )

    typer.echo("Single day download completed.")

    typer.echo("\n===================================")
    typer.echo("STEP 3 - Reprocessing date range")
    typer.echo("===================================")

    processor = CoinETL()

    processor.process_range(
        coin_id=coin,
        start_date="2026-05-01",
        end_date="2026-05-31",
        store_db=store_db,
    )

    typer.echo("Range processing completed.")

    typer.echo("\n===================================")
    typer.echo("PROJECT EXECUTION FINISHED")
    typer.echo("===================================")


if __name__ == "__main__":
    app()
