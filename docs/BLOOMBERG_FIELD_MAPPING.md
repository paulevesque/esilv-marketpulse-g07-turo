# Bloomberg Field Mapping

## Access mode

APPROVED_SAMPLE

```text
Source:
data/sample/bloomberg_reference_sample.json

Reference:
docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md

Live connectivity:
not demonstrated
```

Notes on this mode:

- No Bloomberg terminal or Bloomberg API was queried to write this document. Everything below comes from the approved sample file.
- The sample file describes itself as `"access_mode": "approved_sample"` and `"is_live_bloomberg_output": false`. Its values are illustrative teaching values reused from `data/sample/prices.csv`, not certified Bloomberg observations.
- `docs/10_BLOOMBERG_INSTRUCTOR_REFERENCE.md` is the instructor reference named by the lab. It is not present in the team repository, so the mapping below was read directly from the sample file and checked against `data/sample/bloomberg_reference_expected.json`.
- This document must not be used later as proof of LIVE Bloomberg connectivity.

## Market instruments

| Role | Canonical ticker | Bloomberg identifier |
|---|---|---|
| Instrument | AAPL | AAPL US Equity |
| Benchmark | SP500 | SPX Index |

The Bloomberg identifier is only used to ask the provider for data. MarketPulse rows and `src/analytics.py` keep using the canonical tickers `AAPL` and `SP500`.

In the sample file, each series carries both values:

| Sample key | Instrument series | Benchmark series |
|---|---|---|
| `role` | `instrument` | `benchmark` |
| `provider_identifier` | `AAPL US Equity` | `SPX Index` |
| `canonical_ticker` | `AAPL` | `SP500` |

## Inspected input

Structure of `data/sample/bloomberg_reference_sample.json`:

```text
{
  "sample_kind", "provider_stage", "access_mode",
  "is_live_bloomberg_output", "provenance", "schema_note",
  "series": [
    {
      "role": ...,
      "canonical_ticker": ...,
      "provider_identifier": ...,
      "observations": [
        {
          "observation_date": ...,
          "open_value": ...,
          "high_value": ...,
          "low_value": ...,
          "close_value": ...,
          "volume_value": ...
        },
        ...
      ]
    },
    ...
  ]
}
```

| Observation | AAPL US Equity | SPX Index |
|---|---|---|
| Number of observations | 21 | 21 |
| First date | 2026-09-01 | 2026-09-01 |
| Last date | 2026-09-30 | 2026-09-30 |
| Date representation | text, `YYYY-MM-DD` | text, `YYYY-MM-DD` |
| Price values | JSON numbers, some without decimals (`248`, `250`) | JSON numbers, all without decimals (`6600`) |
| Volume values | whole numbers (`38000000`) | always `0` |
| Missing values | none | none |

First observation of each series:

```json
{"observation_date": "2026-09-01", "open_value": 249.2, "high_value": 251.5, "low_value": 248, "close_value": 250, "volume_value": 38000000}
```

```json
{"observation_date": "2026-09-01", "open_value": 6592, "high_value": 6615, "low_value": 6580, "close_value": 6600, "volume_value": 0}
```

## Field mapping

| MarketPulse field | Source field or mapping | Status / notes |
|---|---|---|
| date | `observation_date` | Teaching wrapper key. Already `YYYY-MM-DD` text, kept as is. |
| ticker | application mapping | `AAPL` or `SP500`. Taken from the series `canonical_ticker`, never from `provider_identifier`. |
| open | `open_value` | Teaching wrapper key. Convert to `float`. |
| high | `high_value` | Teaching wrapper key. Convert to `float`. |
| low | `low_value` | Teaching wrapper key. Convert to `float`. |
| close | `close_value` | Teaching wrapper key. Convert to `float`. |
| volume | `volume_value` | Teaching wrapper key. Convert to `int`. `0` for the benchmark series. |

Important:

```text
teaching wrapper key
!=
Bloomberg LIVE field mnemonic
```

`observation_date`, `open_value`, `high_value`, `low_value`, `close_value` and `volume_value` are keys of the fallback fixture. They are not Bloomberg field names. The names of the corresponding fields in a LIVE Bloomberg response were not observed and are therefore not recorded here.

## Target canonical row

TD09 does not implement the normalization. The row TD10 has to produce is:

```python
{
    "date": "2026-09-01",
    "ticker": "SP500",
    "open": 6592.0,
    "high": 6615.0,
    "low": 6580.0,
    "close": 6600.0,
    "volume": 0,
}
```

Check done for this document: applying the field mapping above to the 42 observations of the sample file (21 per series) gives exactly the 42 rows of `data/sample/bloomberg_reference_expected.json`.

## Provider identifiers by stage

| Canonical ticker | CSV | Yahoo | Bloomberg |
|---|---|---|---|
| AAPL | AAPL | AAPL | AAPL US Equity |
| SP500 | SP500 | ^GSPC | SPX Index |

## Provider boundary

Where the Bloomberg-specific names stop, using the benchmark as the example:

```text
data/sample/bloomberg_reference_sample.json
  series: provider_identifier = "SPX Index"
          canonical_ticker    = "SP500"
          observations: observation_date, open_value, ..., volume_value
        |
        v
TD10  src/providers/bloomberg_provider.py
  - selects the series by provider_identifier "SPX Index"
  - renames observation_date -> date, open_value -> open, ..., volume_value -> volume
  - casts prices to float and volume to int
  - writes canonical_ticker "SP500" into ticker
        |
        |   <-- provider boundary: "SPX Index" and the *_value keys
        |       do not cross this line
        v
canonical rows
  {"date": "2026-09-01", "ticker": "SP500", "open": 6592.0, ..., "volume": 0}
        |
        v
src/main.py         align_series() on common dates
        |
        v
src/analytics.py    period return, base 100, relative performance
                    (only AAPL / SP500 rows, no provider identifier)
```

The Yahoo stage follows the same path: `^GSPC` exists only in `src/providers/yahoo_provider.py` (`YAHOO_SYMBOLS` and `get_yahoo_symbol()`), and the rows it returns already carry `SP500`. TD10 should give Bloomberg the same shape, so that `src/main.py` only chooses a provider and `src/analytics.py` stays unchanged.

Checked on the current `main`: no Bloomberg identifier (`US Equity`, `SPX`) appears anywhere under `src/`.

## TD10 handoff

- Access mode: APPROVED_SAMPLE. Live connectivity not demonstrated.
- Instrument identifier: `AAPL US Equity`, canonical ticker `AAPL`.
- Benchmark identifier: `SPX Index`, canonical ticker `SP500`.
- Date representation: text `YYYY-MM-DD` in `observation_date`. No conversion needed.
- Input structure: one JSON object with a `series` list. Each series has `role`, `canonical_ticker`, `provider_identifier` and an `observations` list of flat objects.
- Missing fields: none in the sample. All six keys are present in all 42 observations.
- Special normalization notes:
  - select a series by `provider_identifier` (or `role`) and write `canonical_ticker` into the row `ticker`;
  - prices arrive as JSON numbers that Python may load as `int` (for example `250`), so cast `open`, `high`, `low` and `close` to `float`;
  - cast `volume` to `int`; the benchmark volume is `0`, which is a value, not a missing field;
  - both series already share the same 21 dates, but `align_series()` from `src/analytics.py` should still be used rather than assuming it;
  - `src/analytics.py` must not change, and no Bloomberg identifier should appear in it.

Expected canonical reference:

```text
data/sample/bloomberg_reference_expected.json
```

If a LIVE session takes place later, this document has to be updated with the actual access method, the identifiers used and the field names actually observed, and the access mode changed to LIVE.
