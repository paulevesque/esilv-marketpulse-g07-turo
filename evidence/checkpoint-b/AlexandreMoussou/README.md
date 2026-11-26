# Checkpoint B - Alexandre Moussou

- GitHub username: AlexandreMoussou
- TD group / team: G07 - T07
- Team repository: `esilv-marketpulse-g07-turo`

## Evidence

| File | What it shows |
|---|---|
| `01_pull_request.png` | My Pull Request #9 `fix: report unmapped Yahoo symbol clearly` (branch `fix/unmapped-yahoo-symbol`) |
| `02_code_review.png` | My review of Pull Request #7 `feat: add Yahoo Finance provider` |
| `03_yahoo_market_data.png` | Successful remote retrieval through `yfinance`: canonical rows for AAPL and SP500 (Yahoo symbol `^GSPC`) |
| `04_instrument_benchmark.png` | `python src/main.py`: AAPL vs SP500, 1 month, Daily, period returns, relative performance and base 100 |

## What I did (TD05-TD08)

- TD06 / TD08: reviewed Pull Request #7 (Yahoo provider). I checked the branch out and ran it:
  live Yahoo retrieval works, `python src/main.py csv` still gives the TD07 values,
  `src/analytics.py` is unchanged and `^GSPC` appears only in `src/providers/yahoo_provider.py`.
- TD08: the review found that a ticker missing from `YAHOO_SYMBOLS` was reported as a bare
  `KeyError` (`retrieval failed: 'MSFT'`), which read like a network failure. I fixed it in my own
  Pull Request #9: the mapping is checked before fetching and the message names the ticker and the
  file to edit.

## Concepts

- `yfinance` is a community library, not the official Yahoo Finance API.
- `SP500` is the MarketPulse canonical ticker; `^GSPC` is the Yahoo provider symbol and stays at
  the provider boundary.
- The provider returns canonical rows (`date`, `ticker`, `open`, `high`, `low`, `close`, `volume`),
  so `align_series()`, `calculate_period_return()`, `calculate_base_100()` and
  `calculate_relative_performance()` from TD07 are reused unchanged.
- Relative performance is instrument return minus benchmark return, in percentage points.
- Yahoo values depend on the retrieval date; nothing is hard-coded.
