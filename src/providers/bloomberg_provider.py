"""Bloomberg-stage provider for MarketPulse.

Bloomberg identifiers, the authorized raw input and the normalization to
canonical MarketPulse rows live here. Nothing Bloomberg-specific leaves
this module: the rows it returns carry the canonical tickers AAPL / SP500.

Field mapping source: docs/BLOOMBERG_FIELD_MAPPING.md (TD09).

Access mode: APPROVED_SAMPLE.
The raw input is the instructor-approved fallback fixture
data/sample/bloomberg_reference_sample.json. It validates the provider
boundary and the normalization contract. It is NOT live Bloomberg output.
"""

from pathlib import Path
import json


ACCESS_MODE = "APPROVED_SAMPLE"

SAMPLE_FILE = Path("data/sample/bloomberg_reference_sample.json")

# Canonical MarketPulse ticker -> Bloomberg identifier.
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

# APPROVED_SAMPLE teaching wrapper keys -> canonical fields.
# These keys belong to the fallback fixture. They are not Bloomberg mnemonics.
SAMPLE_FIELDS = {
    "date": "observation_date",
    "open": "open_value",
    "high": "high_value",
    "low": "low_value",
    "close": "close_value",
    "volume": "volume_value",
}


def get_bloomberg_identifier(canonical_ticker):
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(
            f"no Bloomberg identifier is mapped for {canonical_ticker} "
            "(add it to BLOOMBERG_IDENTIFIERS in "
            "src/providers/bloomberg_provider.py)"
        )

    return BLOOMBERG_IDENTIFIERS[canonical_ticker]


def fetch_raw_bloomberg_history(identifier, start_date=None, end_date=None):
    """Return the raw series for one Bloomberg identifier.

    APPROVED_SAMPLE: the series is read from the approved fixture.
    A LIVE implementation would replace only this function, using the
    instructor-approved classroom mechanism.
    """
    with open(SAMPLE_FILE, encoding="utf-8") as file:
        sample = json.load(file)

    if sample.get("is_live_bloomberg_output"):
        raise ValueError(f"{SAMPLE_FILE} is not the approved fallback fixture")

    for series in sample["series"]:
        if series["provider_identifier"] == identifier:
            observations = [
                observation
                for observation in series["observations"]
                if (start_date is None or observation["observation_date"] >= start_date)
                and (end_date is None or observation["observation_date"] <= end_date)
            ]
            return {**series, "observations": observations}

    raise ValueError(f"no Bloomberg-stage series found for {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    rows = []

    for observation in raw_data["observations"]:
        rows.append({
            "date": observation[SAMPLE_FIELDS["date"]],
            "ticker": canonical_ticker,
            "open": float(observation[SAMPLE_FIELDS["open"]]),
            "high": float(observation[SAMPLE_FIELDS["high"]]),
            "low": float(observation[SAMPLE_FIELDS["low"]]),
            "close": float(observation[SAMPLE_FIELDS["close"]]),
            "volume": int(observation[SAMPLE_FIELDS["volume"]]),
        })

    if not rows:
        raise ValueError(f"no Bloomberg-stage rows for {canonical_ticker}")

    return rows


def fetch_bloomberg_prices(canonical_ticker, start_date=None, end_date=None):
    identifier = get_bloomberg_identifier(canonical_ticker)
    raw_data = fetch_raw_bloomberg_history(identifier, start_date, end_date)

    return normalize_bloomberg_history(raw_data, canonical_ticker)
