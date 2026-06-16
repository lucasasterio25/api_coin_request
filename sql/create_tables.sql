--- SQL command to create tables
CREATE TABLE IF NOT EXISTS coin_history
(
    id SERIAL PRIMARY KEY,

    coin_id VARCHAR(100) NOT NULL,

    reference_date DATE NOT NULL,

    price_usd DOUBLE PRECISION,

    raw_payload JSONB NOT NULL,

    created_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT uq_coin_date
        UNIQUE (
            coin_id,
            reference_date
        )
);

CREATE TABLE IF NOT EXISTS coin_monthly_stats
(
    id SERIAL PRIMARY KEY,

    coin_id VARCHAR(100) NOT NULL,

    year INTEGER NOT NULL,

    month INTEGER NOT NULL,

    min_price DOUBLE PRECISION,

    max_price DOUBLE PRECISION,

    updated_at TIMESTAMP DEFAULT NOW(),

    CONSTRAINT uq_coin_month
        UNIQUE (
            coin_id,
            year,
            month
        )
);