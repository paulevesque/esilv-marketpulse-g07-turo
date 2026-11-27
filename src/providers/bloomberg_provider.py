"""Bloomberg-stage provider for MarketPulse.

Bloomberg identifiers, the raw input boundary and the normalization to
canonical MarketPulse rows live here. Nothing Bloomberg-specific leaves
this module.

The field mapping comes from docs/BLOOMBERG_FIELD_MAPPING.md (TD09).

Access mode: APPROVED_SAMPLE. The rows come from the instructor fallback
fixture, not from a Bloomberg terminal. This is not live connectivity.
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

# Canonical field -> key of the approved sample (teaching wrapper keys,
# not Bloomberg field mnemonics).
SAMPLE_PRICE_KEYS = {
    "open": "open_value",
    "high": "high_value",
    "low": "low_value",
    "close": "close_value",
}


def get_bloomberg_identifier(canonical_ticker):
    if canonical_ticker not in BLOOMBERG_IDENTIFIERS:
        raise ValueError(
            f"no Bloomberg identifier is mapped for {canonical_ticker} "
            "(add it to BLOOMBERG_IDENTIFIERS in "
            "src/providers/bloomberg_provider.py)"
        )

    return BLOOMBERG_IDENTIFIERS[canonical_ticker]


def fetch_raw_bloomberg_history(identifier, start_date, end_date):
    # LIVE boundary. Only the instructor-approved classroom mechanism
    # belongs here, and no LIVE session took place for this team.
    raise NotImplementedError(
        "LIVE Bloomberg access is not available in this environment "
        f"(access mode is {ACCESS_MODE})"
    )


def load_sample_bloomberg_history(identifier):
    with open(SAMPLE_FILE, encoding="utf-8") as file:
        sample = json.load(file)

    for series in sample["series"]:
        if series["provider_identifier"] == identifier:
            return series

    raise ValueError(f"No approved sample series for {identifier}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    observations = raw_data["observations"]

    if not observations:
        raise ValueError(
            f"No Bloomberg-stage observation for {canonical_ticker}"
        )

    rows = []

    for observation in observations:
        row = {
            "date": observation["observation_date"],
            "ticker": canonical_ticker,
        }

        for field, sample_key in SAMPLE_PRICE_KEYS.items():
            row[field] = float(observation[sample_key])

        row["volume"] = int(observation["volume_value"])
        rows.append(row)

    return rows


def fetch_bloomberg_prices(canonical_ticker):
    identifier = get_bloomberg_identifier(canonical_ticker)
    raw_data = load_sample_bloomberg_history(identifier)

    return normalize_bloomberg_history(raw_data, canonical_ticker)
