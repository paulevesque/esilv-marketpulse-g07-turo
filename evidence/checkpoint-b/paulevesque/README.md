# Checkpoint B - @paulevesque

## Scope

Checkpoint Phase B - TD05 to TD08.

- GitHub username: paulevesque
- TD group / team: G07 - T07
- Team repository: `esilv-marketpulse-g07-turo`

## Evidence files

| File | Content |
|---|---|
| `01_pull_request.png` | My Pull Request #7 `feat: add Yahoo Finance provider` (branch `feature/yahoo-provider`), merged into `main` after review by @AlexandreMoussou |
| `02_code_review.png` | My review of Pull Request #6 `feat: add reusable market comparison analytics`, with what I verified and three non-blocking remarks |
| `03_yahoo_market_data.png` | Successful remote retrieval through `yfinance` on 2026-11-26: 23 canonical rows for AAPL and 23 for SP500 (Yahoo symbol `^GSPC`), first and last row of each |
| `04_instrument_benchmark.png` | `python src/main.py` with the Yahoo provider: `Provider : Yahoo Finance via yfinance`, 1 month, Daily, 23 common dates, AAPL and SP500 period returns, relative performance in percentage points and base 100 |

The command in `03_yahoo_market_data.png` calls `fetch_yahoo_prices()` from `src/providers/yahoo_provider.py` for each entry of `YAHOO_SYMBOLS` and prints the number of rows, the first row and the last row. The `ticker` of the benchmark rows is `SP500`, not `^GSPC`.

## What I did (TD05-TD08)

- TD05: Pull Request #2 `feat: display data provider label` and Pull Request #3 `docs: add Paul Evesque to TEAM.md`, both reviewed and merged.
- TD06: reviewed Pull Request #1. I first requested changes because the branch conflicted with `main`, then approved after the conflict was resolved.
- TD07: reviewed Pull Request #6 (analytics). I checked the branch out, ran it and tested `align_series()` with two series that do not share all their dates.
- TD08: Pull Request #7. In that Pull Request the TD08 commit is mine; the other commit is the TD07 commit of #6, because my branch was built on top of it.
  - `src/providers/yahoo_provider.py` retrieves a 1-month daily series through `yfinance` and returns canonical rows.
  - `src/main.py` reads Yahoo Finance by default; `python src/main.py csv` still runs on the local sample data.
  - `yfinance` is recorded in `requirements.txt`.
  - `src/analytics.py` is not modified.

## Understanding

- `yfinance` is a community library, not the official Yahoo Finance API.
- `SP500` is the MarketPulse canonical ticker. `^GSPC` is the Yahoo symbol and is only used inside the provider module.
- The provider converts the Yahoo table to canonical rows (`date`, `ticker`, `open`, `high`, `low`, `close`, `volume`). Because the rows have the same shape as the CSV rows, the TD07 functions are reused unchanged.
- The two series are aligned on common dates with `align_series()` before any calculation; rows are never compared by list position.
- Relative performance is instrument return minus benchmark return, expressed in percentage points.
- The Yahoo values depend on the retrieval date. Nothing is hard-coded.
- If Yahoo is unavailable, the CSV path still validates the analytics, but CSV output is not Yahoo evidence.

## Security

No password, token, key or personal information appears in the screenshots.
