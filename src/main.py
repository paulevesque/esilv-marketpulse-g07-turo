from pathlib import Path
import csv
import json
import sys

from analytics import (
    align_series,
    calculate_base_100,
    calculate_period_return,
    calculate_relative_performance,
)


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
PROVIDER = "bloomberg"
LOOKBACK = "1mo"
INTERVAL = "1d"

PROVIDER_LABELS = {
    "csv": "CSV (local sample data)",
    "yahoo": "Yahoo Finance via yfinance",
    "bloomberg": "Bloomberg stage",
}
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def normalize_price_row(row):
    return {
        "date": row["date"],
        "ticker": row["ticker"],
        "open": float(row["open"]),
        "high": float(row["high"]),
        "low": float(row["low"]),
        "close": float(row["close"]),
        "volume": int(row["volume"]),
    }


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def load_csv_prices(instrument, benchmark):
    prices = [normalize_price_row(row) for row in load_prices()]

    return (
        filter_prices(prices, instrument["ticker"]),
        filter_prices(prices, benchmark["ticker"]),
    )


def load_yahoo_prices(instrument, benchmark):
    # Imported here so the local CSV path keeps working without yfinance.
    from providers.yahoo_provider import fetch_yahoo_prices, get_yahoo_symbol

    # Resolve both symbols first, so a missing mapping fails before any download.
    symbols = [get_yahoo_symbol(asset["ticker"]) for asset in (instrument, benchmark)]

    return tuple(
        fetch_yahoo_prices(
            symbol=symbol,
            canonical_ticker=asset["ticker"],
            period=LOOKBACK,
            interval=INTERVAL,
        )
        for symbol, asset in zip(symbols, (instrument, benchmark))
    )


def load_bloomberg_prices(instrument, benchmark):
    from providers.bloomberg_provider import fetch_bloomberg_prices

    return (
        fetch_bloomberg_prices(instrument["ticker"]),
        fetch_bloomberg_prices(benchmark["ticker"]),
    )


PRICE_LOADERS = {
    "csv": load_csv_prices,
    "yahoo": load_yahoo_prices,
    "bloomberg": load_bloomberg_prices,
}


def get_access_mode(provider):
    # Only the Bloomberg stage has an access mode: LIVE or APPROVED_SAMPLE.
    if provider != "bloomberg":
        return None

    from providers.bloomberg_provider import ACCESS_MODE

    return ACCESS_MODE


def build_market_snapshot(provider=PROVIDER):
    """Build the application result shared by the terminal and the dashboard.

    Raises ValueError when the provider is unknown, when retrieval fails
    or when the two series have no common date.
    """
    if provider not in PRICE_LOADERS:
        raise ValueError(
            f"Unknown provider: {provider} "
            f"(use {', '.join(PRICE_LOADERS)})"
        )

    provider_label = PROVIDER_LABELS[provider]
    access_mode = get_access_mode(provider)

    if access_mode:
        provider_label = f"{provider_label} - {access_mode}"

    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    try:
        instrument_prices, benchmark_prices = PRICE_LOADERS[provider](
            instrument,
            benchmark,
        )
    except Exception as error:
        raise ValueError(
            f"{provider_label} retrieval failed: {error}"
        ) from error

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument:
        raise ValueError("No common dates between instrument and benchmark.")

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)

    return {
        "provider": provider_label,
        "access_mode": access_mode,
        "lookback": LOOKBACK_LABEL,
        "interval": INTERVAL_LABEL,
        "instrument": instrument,
        "benchmark": benchmark,
        "instrument_return": instrument_return,
        "benchmark_return": benchmark_return,
        "relative_performance": calculate_relative_performance(
            instrument_return,
            benchmark_return,
        ),
        "instrument_base_100": calculate_base_100(aligned_instrument),
        "benchmark_base_100": calculate_base_100(aligned_benchmark),
    }


def display_asset_summary(label, asset, period_return):
    print(label)
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Period return : {period_return:.2f}%")


def main():
    # Optional: "python src/main.py yahoo" or "python src/main.py csv".
    provider = sys.argv[1] if len(sys.argv) > 1 else PROVIDER

    try:
        snapshot = build_market_snapshot(provider)
    except ValueError as error:
        sys.exit(str(error))

    instrument = snapshot["instrument"]
    benchmark = snapshot["benchmark"]
    instrument_base_100 = snapshot["instrument_base_100"]
    benchmark_base_100 = snapshot["benchmark_base_100"]

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Provider : {snapshot['provider']}")
    if snapshot["access_mode"] == "APPROVED_SAMPLE":
        print("Access mode : APPROVED_SAMPLE (fallback sample, not live Bloomberg)")
    elif snapshot["access_mode"]:
        print(f"Access mode : {snapshot['access_mode']}")
    print(f"Period   : {snapshot['lookback']}")
    print(f"Interval : {snapshot['interval']}")
    print(
        f"Common dates : {len(instrument_base_100)} "
        f"({instrument_base_100[0]['date']} -> {instrument_base_100[-1]['date']})"
    )
    print()
    display_asset_summary("Instrument", instrument, snapshot["instrument_return"])
    print()
    display_asset_summary("Benchmark", benchmark, snapshot["benchmark_return"])
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{snapshot['relative_performance']:+.2f} percentage points"
    )
    print()
    print("Base 100")
    width = max(len(instrument["ticker"]), len(benchmark["ticker"]))
    for series in (instrument_base_100, benchmark_base_100):
        print(
            f"{series[0]['ticker']:<{width}} : "
            f"{series[0]['value']:.2f} -> {series[-1]['value']:.2f}"
        )


if __name__ == "__main__":
    main()
