from pathlib import Path
import csv
import json


DATA_DIR = Path("data/sample")

# These starter values mirror config/settings.yml.
# settings.yml is a human-readable configuration contract in the CORE.
# Parsing YAML is optional and is not required by the 18-hour lab sequence.
PROVIDER_LABEL = "CSV (local sample data)"
LOOKBACK_LABEL = "1 month"
INTERVAL_LABEL = "Daily"


def load_instruments():
    with open(DATA_DIR / "instruments.json", encoding="utf-8") as file:
        return json.load(file)


def load_prices():
    with open(DATA_DIR / "prices.csv", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def filter_prices(prices, ticker):
    return [row for row in prices if row["ticker"] == ticker]


def get_first_date(prices):
    return prices[0]["date"]


def get_last_date(prices):
    return prices[-1]["date"]


def get_first_close(prices):
    return float(prices[0]["close"])


def get_last_close(prices):
    return float(prices[-1]["close"])


def display_market_summary(label, asset, prices, unit=""):
    print(label)
    print(f"{asset['ticker']} - {asset['name']}")
    print(f"Market       : {asset['market']} | Currency: {asset['currency']}")
    print(f"Observations : {len(prices)}")
    print(f"First date   : {get_first_date(prices)}")
    print(f"Last date    : {get_last_date(prices)}")
    print(f"First close  : {get_first_close(prices):.2f}{unit}")
    print(f"Last close   : {get_last_close(prices):.2f}{unit}")


def main():
    instruments = load_instruments()
    prices = load_prices()

    instrument = instruments["instrument"]
    benchmark = instruments["benchmark"]

    instrument_prices = filter_prices(prices, instrument["ticker"])
    benchmark_prices = filter_prices(prices, benchmark["ticker"])

    print("=== MarketPulse ===")
    print()
    display_market_summary(
        "Instrument", instrument, instrument_prices, f" {instrument['currency']}"
    )
    print()
    display_market_summary("Benchmark", benchmark, benchmark_prices)
    print()
    print(f"Provider: {PROVIDER_LABEL}")
    print(f"Period: {LOOKBACK_LABEL}")
    print(f"Interval: {INTERVAL_LABEL}")


if __name__ == "__main__":
    main()
