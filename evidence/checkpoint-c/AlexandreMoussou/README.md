# Checkpoint C - Alexandre Moussou

- GitHub username: AlexandreMoussou
- TD group / team: G07 - T07
- Team repository: `esilv-marketpulse-g07-turo`
- Final provider: Bloomberg stage - APPROVED_SAMPLE (instructor fallback sample, not live Bloomberg)

## Evidence

| File | What it shows |
|---|---|
| `01_final_market_data.png` | `python src/main.py` on merged `main`: provider `Bloomberg stage - APPROVED_SAMPLE`, access mode line, AAPL vs SP500, 1 month, Daily, period returns, relative performance and base 100 |
| `02_dash_dashboard.png` | `python src/dashboard.py` in the browser: provider, instrument, benchmark, lookback, interval, the three performance values and the base-100 chart with both series |
| `03_final_pull_request.png` | My Pull Request #15 `feat: add Bloomberg provider boundary` (branch `feature/bloomberg-provider`), reviewed by Amd19z and merged |
| `04_reproducible_run.png` | Fresh clone of `main` in an empty folder, new virtual environment, `python -m pip install -r requirements.txt`, then `python src/main.py` |

## What I did (TD09-TD12)

- TD10, Pull Request #15: `src/providers/bloomberg_provider.py` (identifier mapping, raw input
  boundary, normalization of the approved sample to canonical rows) and `build_market_snapshot()`
  in `src/main.py`. The 42 normalized rows are equal to
  `data/sample/bloomberg_reference_expected.json`.
- TD11, Pull Request #16: `src/dashboard.py`, a static Dash page that only displays the snapshot,
  and `dash` / `plotly` in `requirements.txt`.
- TD12, Pull Request #20: final README (provider and mode, install and run commands, environment
  constraint) and the fresh-clone test.
- Reviews: Pull Requests #21, #22 and #23 (the same three labs done by paulevesque), checked out
  and run before approving.

## Concepts

- `AAPL US Equity` and `SPX Index` are Bloomberg identifiers. They stay in
  `bloomberg_provider.py`; the rows it returns carry the canonical tickers `AAPL` and `SP500`.
- APPROVED_SAMPLE is not LIVE: the rows come from a file, no Bloomberg terminal was queried, and
  `fetch_raw_bloomberg_history()` only raises.
- CSV, Yahoo and the Bloomberg stage all return the same canonical rows, so `align_series()` and
  the three calculations of `src/analytics.py` are reused unchanged.
- `build_market_snapshot()` is the single application result. The terminal and the dashboard both
  display it, so no formula and no provider call exists in `src/dashboard.py`.
- Reproducible means: clone, install from `requirements.txt`, run the two documented commands from
  the repository root. The default provider needs no network and no credential.
