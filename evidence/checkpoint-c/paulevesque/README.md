# Checkpoint C - @paulevesque

## Scope

Checkpoint Phase C - TD09 to TD12.

- GitHub username: paulevesque
- TD group / team: G07 - T07
- Team repository: `esilv-marketpulse-g07-turo`

## Final provider

```text
Bloomberg stage - APPROVED_SAMPLE
```

The rows come from the instructor fallback fixture `data/sample/bloomberg_reference_sample.json`. No Bloomberg terminal or Bloomberg API was queried. Nothing in this folder is evidence of LIVE Bloomberg connectivity.

## Evidence files

| File | Content |
|---|---|
| `01_final_market_data.png` | `python src/main.py` on branch `feature/final-integration-paulevesque` (TD10 to TD12, not merged into `main` when the capture was taken): `Provider : Bloomberg stage`, `Access mode : APPROVED_SAMPLE`, AAPL - Apple Inc. vs S&P 500, 1 month, Daily, 21 common dates, period returns 6.48% and 2.15%, relative performance +4.33 percentage points, base 100 |
| `02_dash_dashboard.png` | `python src/dashboard.py` on the same branch, page `http://127.0.0.1:8050/`: provider `Bloomberg stage - APPROVED_SAMPLE`, instrument, benchmark, lookback, interval, the three performance values and the base-100 chart with the AAPL and SP500 series |
| `03_final_pull_request.png` | My Pull Request #21 `feat: add Bloomberg provider boundary` (branch `feature/bloomberg-provider-paulevesque`), three commits, opened on 2026-11-27. The capture shows it open and not reviewed yet. TO COMPLETE: retake or update once it is reviewed |
| `04_reproducible_run.png` | Run on 2026-11-27 on Windows: fresh clone of branch `feature/final-integration-paulevesque` in a new folder `marketpulse-repro`, new virtual environment `.venv`, `python -m pip install -r requirements.txt`, `python src/main.py`, then `python src/dashboard.py` answering `GET / 200` |

The four captures were taken on 2026-11-27, before any TD10-TD12 Pull Request was merged. TO COMPLETE: retake `01`, `02` and `04` from `main` after the merge.

## What I did (TD09-TD12)

- TD09: wrote `docs/BLOOMBERG_FIELD_MAPPING.md` (commit `271ad92`, `docs: map Bloomberg stage to MarketPulse`): access mode, the two Bloomberg identifiers, the structure of the approved sample and the field mapping to canonical rows. Reviewed and approved Pull Request #13 (`refactor: resolve Yahoo symbols inside the provider`) and Pull Request #14 (`docs: draw the Bloomberg provider boundary`).
- TD10: Pull Request #21, three commits.
  - `src/providers/bloomberg_provider.py` holds the identifiers (`AAPL US Equity`, `SPX Index`), reads the approved sample and normalizes it to canonical rows. The 42 rows are equal to `data/sample/bloomberg_reference_expected.json`.
  - `build_market_snapshot()` in `src/main.py` returns the result shared by the terminal and the dashboard. `main()` only prints it.
  - The terminal shows `Access mode : APPROVED_SAMPLE`. `python src/main.py yahoo` and `python src/main.py csv` still work.
  - `src/analytics.py` is not modified.
- TD11: Pull Request #22. `src/dashboard.py` is a static Dash page built on `build_market_snapshot()`. `dash` and `plotly` are recorded in `requirements.txt`.
- TD12: Pull Request #23. README "How to run" section rewritten for the final provider, the three dependencies and the two commands. Fresh clone tested with a new virtual environment.
- TO COMPLETE: reviews I did on TD10-TD12 Pull Requests of my teammates (number, what I checked).
- TO COMPLETE: which Pull Requests were finally merged into `main` (the team opened three series for TD10-TD12: #15/#16/#20, #17/#18/#19 and #21/#22/#23).

## Understanding

- `AAPL US Equity` and `SPX Index` are Bloomberg identifiers. They are only used inside `src/providers/bloomberg_provider.py`. The rows that leave the provider carry the canonical tickers `AAPL` and `SP500`.
- The keys of the approved sample (`observation_date`, `open_value`, ..., `volume_value`) are teaching wrapper keys, not Bloomberg field names. The field names of a LIVE response were never observed, so they are not used anywhere.
- CSV, Yahoo and the Bloomberg stage all return rows with the same shape (`date`, `ticker`, `open`, `high`, `low`, `close`, `volume`). This is why `align_series()` and the three TD07 calculations are reused unchanged.
- `build_market_snapshot()` is the only place where the result is assembled. The terminal and the dashboard both read it, so they cannot show different values.
- `src/main.py` keeps `if __name__ == "__main__":`, so `dashboard.py` can import the snapshot builder without running the terminal program.
- `dashboard.py` does not call a provider and contains no formula. It only formats the snapshot values.
- Base 100 puts both series on the same scale (AAPL is around 250, the S&P 500 around 6 600). Both start at 100 because the series are aligned on common dates before the calculation.
- The approved sample and the CSV sample hold the same teaching values, which is why both give 6.48%, 2.15% and +4.33 percentage points.
- Reproducible means: repository + `requirements.txt` + documented commands give a working application on a clean setup. The default provider needs no credential and no internet access once the dependencies are installed.

## Security

No password, token, key or personal information appears in the screenshots.
