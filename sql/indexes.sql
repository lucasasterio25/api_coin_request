-- date select
CREATE INDEX idx_coin_history_reference_date
    ON coin_history (reference_date);

CREATE INDEX idx_coin_history_coin_date_desc
    ON coin_history (coin_id, reference_date DESC);

CREATE INDEX idx_coin_monthly_stats_year_month
    ON coin_monthly_stats (year, month);

-- coin select
CREATE INDEX idx_coin_monthly_stats_coin_id
    ON coin_monthly_stats (coin_id);