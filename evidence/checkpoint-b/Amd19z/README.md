# Checkpoint B - Amary Diarra

- GitHub username: Amd19z
- TD group / team: G07 - T07
- Team repository: `esilv-marketpulse-g07-turo`

## Evidence

| File | What it shows |
|---|---|
| `01_pull_request.png` | My Pull Request #6 `feat: add reusable market comparison analytics` (branch `feature/market-comparison`), reviewed and merged into `main` |
| `02_code_review.png` | My review approving Pull Request #9 `fix: report unmapped Yahoo symbol clearly`, with what I verified and two non-blocking remarks |
| `03_yahoo_market_data.png` | Successful remote retrieval through `yfinance`: 23 canonical rows for AAPL and 23 for SP500 (Yahoo symbol `^GSPC`), first and last row of each |
| `04_instrument_benchmark.png` | `python src/main.py` with the Yahoo provider: AAPL vs SP500, 1 month, Daily, period returns, relative performance and base 100 |

## What I did (TD05-TD08)

- TD05: Pull Request #4 `docs: add How to run section to README` (branch
  `docs/improve-how-to-run`) and Pull Request #5 `docs: add Checkpoint A evidence and TEAM.md row
  for Amd19z`, both reviewed by AlexandreMoussou before merge.
- TD06: review comment on Pull Request #2 `feat: display data provider label`. I checked out the
  branch, ran `python3 src/main.py`, checked the label against `config/settings.yml` and noted that
  the hard-coded label would have to change with the Yahoo provider in TD08.
- TD07: Pull Request #6 adds `src/analytics.py` (`index_by_date`, `align_series`,
  `calculate_period_return`, `calculate_base_100`, `calculate_relative_performance`) and
  updates `src/main.py` to normalize CSV rows (`float` / `int`) and reuse the analytics.
  On the sample data: AAPL 6.48%, SP500 2.15%, +4.33 percentage points.
- TD08: reviewed Pull Request #9. I checked the branch out, tested an unmapped ticker (`MSFT`),
  the Yahoo path and the CSV path, and suggested moving the `YAHOO_SYMBOLS` lookup into the
  provider module.

## Concepts

- `yfinance` is a community library, not the official Yahoo Finance API.
- `SP500` is the MarketPulse canonical ticker; `^GSPC` is the Yahoo symbol and stays in
  `src/providers/yahoo_provider.py`.
- Both providers produce canonical rows (`date`, `ticker`, `open`, `high`, `low`, `close`,
  `volume`), so the TD07 analytics are reused unchanged.
- Instrument and benchmark are aligned on common dates before any calculation.
- Relative performance is instrument return minus benchmark return, in percentage points.
- Yahoo values depend on the retrieval date (here 2026-10-26 -> 2026-11-25); nothing is hard-coded.
