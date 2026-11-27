"""Bloomberg-stage provider for MarketPulse.

Bloomberg identifiers, the authorized raw input boundary and the
normalization to canonical MarketPulse rows live here. Nothing
Bloomberg-specific leaves this module.

The field mapping comes from docs/BLOOMBERG_FIELD_MAPPING.md (TD09).

Access mode: APPROVED_SAMPLE. The rows are read from the instructor
fallback fixture. No Bloomberg terminal or Bloomberg API is queried, so
running this module is not proof of live Bloomberg connectivity.
"""

from pathlib import Path
import json


# Canonical MarketPulse ticker -> Bloomberg identifier.
BLOOMBERG_IDENTIFIERS = {
    "AAPL": "AAPL US Equity",
    "SP500": "SPX Index",
}

# The mode documented in TD09. LIVE was not available to the team.
ACCESS_MODE = "APPROVED_SAMPLE"

SAMPLE_FILE = Path("data/sample/bloomberg_reference_sample.json")

# Canonical field -> (teaching wrapper key of the fixture, conversion).
# These wrapper keys are not Bloomberg field mnemonics.
SAMPLE_FIELDS = {
    "open": ("open_value", float),
    "high": ("high_value", float),
    "low": ("low_value", float),
    "close": ("close_value", float),
    "volume": ("volume_value", int),
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
    """LIVE raw input boundary.

    Only the instructor-approved classroom mechanism belongs here. None
    was documented in TD09, so no connector is invented.
    """
    raise NotImplementedError(
        "LIVE Bloomberg access is not available in this environment "
        f"(requested {identifier}, {start_date} -> {end_date}); "
        "the authorized mode is APPROVED_SAMPLE"
    )


def load_approved_sample_history(identifier, sample_file=SAMPLE_FILE):
    """APPROVED_SAMPLE raw input boundary: one series of the fixture."""
    with open(sample_file, encoding="utf-8") as file:
        sample = json.load(file)

    for series in sample["series"]:
        if series["provider_identifier"] == identifier:
            return series

    raise ValueError(f"no series for {identifier} in {sample_file}")


def normalize_bloomberg_history(raw_data, canonical_ticker):
    """Turn one approved-sample series into canonical MarketPulse rows."""
    if raw_data.get("canonical_ticker") != canonical_ticker:
        raise ValueError(
            f"series {raw_data.get('provider_identifier')} is declared as "
            f"{raw_data.get('canonical_ticker')}, not {canonical_ticker}"
        )

    observations = raw_data.get("observations", [])

    if not observations:
        raise ValueError(
            f"no observation for {raw_data.get('provider_identifier')}"
        )

    rows = []

    for observation in observations:
        try:
            row = {
                "date": observation["observation_date"],
                "ticker": canonical_ticker,
            }

            for field, (source_key, convert) in SAMPLE_FIELDS.items():
                row[field] = convert(observation[source_key])
        except KeyError as error:
            raise ValueError(
                f"missing field {error} in an observation of "
                f"{raw_data.get('provider_identifier')}"
            ) from error

        rows.append(row)

    return rows


def fetch_bloomberg_prices(canonical_ticker):
    """Canonical rows for one canonical ticker, in the authorized mode."""
    identifier = get_bloomberg_identifier(canonical_ticker)
    raw_data = load_approved_sample_history(identifier)

    return normalize_bloomberg_history(raw_data, canonical_ticker)
