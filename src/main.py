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
PROVIDER = "yahoo"
LOOKBACK = "1mo"
INTERVAL = "1d"

PROVIDER_LABELS = {
    "csv": "CSV (local sample data)",
    "yahoo": "Yahoo Finance via yfinance",
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
    from providers.yahoo_provider import YAHOO_SYMBOLS, fetch_yahoo_prices

    for asset in (instrument, benchmark):
        if asset["ticker"] not in YAHOO_SYMBOLS:
            raise ValueError(
                f"no Yahoo symbol is mapped for {asset['ticker']} "
                "(add it to YAHOO_SYMBOLS in src/providers/yahoo_provider.py)"
            )

    return tuple(
        fetch_yahoo_prices(
            symbol=YAHOO_SYMBOLS[asset["ticker"]],
            canonical_ticker=asset["ticker"],
            period=LOOKBACK,
            interval=INTERVAL,
        )
        for asset in (instrument, benchmark)
    )


PRICE_LOADERS = {
    "csv": load_csv_prices,
    "yahoo": load_yahoo_prices,
}


def display_asset_summary(label, asset, period_return):
    print(label)
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Period return : {period_return:.2f}%")


def main():
    # Optional: "python src/main.py csv" runs on the local sample data.
    provider = sys.argv[1] if len(sys.argv) > 1 else PROVIDER

    if provider not in PRICE_LOADERS:
        sys.exit(f"Unknown provider: {provider} (use csv or yahoo)")

    instruments = load_instruments()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    try:
        instrument_prices, benchmark_prices = PRICE_LOADERS[provider](
            instrument,
            benchmark,
        )
    except Exception as error:
        sys.exit(f"{PROVIDER_LABELS[provider]} retrieval failed: {error}")

    aligned_instrument, aligned_benchmark = align_series(
        instrument_prices,
        benchmark_prices,
    )

    if not aligned_instrument:
        print("No common dates between instrument and benchmark.")
        return

    instrument_return = calculate_period_return(aligned_instrument)
    benchmark_return = calculate_period_return(aligned_benchmark)
    relative_performance = calculate_relative_performance(
        instrument_return,
        benchmark_return,
    )

    instrument_base_100 = calculate_base_100(aligned_instrument)
    benchmark_base_100 = calculate_base_100(aligned_benchmark)

    print("=== MarketPulse ===")
    print()
    print("Market configuration")
    print(f"Provider : {PROVIDER_LABELS[provider]}")
    print(f"Period   : {LOOKBACK_LABEL}")
    print(f"Interval : {INTERVAL_LABEL}")
    print(
        f"Common dates : {len(aligned_instrument)} "
        f"({aligned_instrument[0]['date']} -> {aligned_instrument[-1]['date']})"
    )
    print()
    display_asset_summary("Instrument", instrument, instrument_return)
    print()
    display_asset_summary("Benchmark", benchmark, benchmark_return)
    print()
    print("Relative performance")
    print(
        f"{instrument['ticker']} vs {benchmark['ticker']} : "
        f"{relative_performance:+.2f} percentage points"
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
