"""Yahoo Finance provider for MarketPulse.

Yahoo acquisition, Yahoo symbol handling and normalization to canonical
MarketPulse rows live here. Nothing Yahoo-specific leaves this module.

yfinance is a community library, not the official Yahoo Finance API.
"""

import yfinance as yf


# Canonical MarketPulse ticker -> Yahoo Finance symbol.
YAHOO_SYMBOLS = {
    "AAPL": "AAPL",
    "SP500": "^GSPC",
}


def get_yahoo_symbol(canonical_ticker):
    if canonical_ticker not in YAHOO_SYMBOLS:
        raise ValueError(
            f"no Yahoo symbol is mapped for {canonical_ticker} "
            "(add it to YAHOO_SYMBOLS in src/providers/yahoo_provider.py)"
        )

    return YAHOO_SYMBOLS[canonical_ticker]


def fetch_yahoo_prices(
    symbol,
    canonical_ticker,
    period="1mo",
    interval="1d",
):
    history = yf.Ticker(symbol).history(
        period=period,
        interval=interval,
        auto_adjust=False,
    )

    if history.empty:
        raise ValueError(
            f"No Yahoo Finance data returned for {symbol}"
        )

    rows = []

    for timestamp, row in history.iterrows():
        rows.append({
            "date": timestamp.strftime("%Y-%m-%d"),
            "ticker": canonical_ticker,
            "open": float(row["Open"]),
            "high": float(row["High"]),
            "low": float(row["Low"]),
            "close": float(row["Close"]),
            "volume": int(row["Volume"]),
        })

    return rows
