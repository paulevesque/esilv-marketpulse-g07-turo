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

All four captures were taken on 2026-11-27, after Pull Requests #15, #16 and #20 were merged. `main` was at commit `d91d530` (`Merge pull request #20`).

| File | Content |
|---|---|
| `01_final_market_data.png` | `python src/main.py` on the merged `main` (`git status -sb` and `git log --oneline -1` are shown first): `Provider : Bloomberg stage - APPROVED_SAMPLE`, `Access mode : APPROVED_SAMPLE (fallback sample, not live Bloomberg)`, 1 month, Daily, 21 common dates, period returns 6.48% and 2.15%, relative performance +4.33 percentage points, base 100 |
| `02_dash_dashboard.png` | `python src/dashboard.py` on the same commit, page `http://127.0.0.1:8050/`: provider `Bloomberg stage - APPROVED_SAMPLE`, instrument, benchmark, lookback, interval, the three performance values and the base-100 chart with the AAPL and SP500 series |
| `03_final_pull_request.png` | My Pull Request #21 `feat: add Bloomberg provider boundary` (branch `feature/bloomberg-provider-paulevesque`, three commits), approved by @AlexandreMoussou and then closed without merging. See below |
| `04_reproducible_run.png` | Fresh clone of the team repository in a new folder `marketpulse-repro` (commit `d91d530`), new virtual environment `.venv`, `python -m pip install -r requirements.txt`, `python src/main.py`, then `python src/dashboard.py` answering `GET / 200`. Run on Windows |

About `03_final_pull_request.png`: the three of us each opened a TD10-TD12 series (#15/#16/#20, #17/#18/#19 and #21/#22/#23). They change the same files, so only one could be merged. The team chose the series of @AlexandreMoussou. Mine was reviewed and approved, then closed. The code that runs in `01`, `02` and `04` is therefore the merged code of #15, #16 and #20, not the code of #21.

## What I did (TD09-TD12)

- TD09: wrote `docs/BLOOMBERG_FIELD_MAPPING.md` (commit `271ad92`, `docs: map Bloomberg stage to MarketPulse`): access mode, the two Bloomberg identifiers, the structure of the approved sample and the field mapping to canonical rows. Reviewed and approved Pull Request #13 (`refactor: resolve Yahoo symbols inside the provider`) and Pull Request #14 (`docs: draw the Bloomberg provider boundary`).
- TD10: Pull Request #21 (three commits: provider module, snapshot in `main.py`, Bloomberg stage as default provider). Approved, not merged.
- TD11: Pull Request #22 (`dash` and `plotly` in `requirements.txt`, `src/dashboard.py`). Approved, not merged.
- TD12: Pull Request #23 (README "How to run" section). Approved, not merged.
- Reviews: I checked out and ran the three Pull Requests of @Amd19z, then approved them as code reviews.
  - #17 (TD10): compared the 42 normalized rows with `bloomberg_reference_expected.json`, ran the three providers and an unknown provider. Three non-blocking remarks: `ACCESS_MODE` defined but not used, the name of `fetch_raw_bloomberg_history()`, and `start_date` / `end_date` never passed by `main.py`.
  - #18 (TD11): compared the dashboard values with the terminal and checked that `dashboard.py` has no provider call and no formula.
  - #19 (TD12): ran both commands against the README. One remark on the name of the instructor repository.
- Merged into `main`: #15, #16 and #20 by @AlexandreMoussou, reviewed by @Amd19z. After the merge I ran `python src/main.py` and `python src/dashboard.py` on `main` and did the fresh clone of `04`.

## Understanding

- `AAPL US Equity` and `SPX Index` are Bloomberg identifiers. They are only used inside `src/providers/bloomberg_provider.py`. The rows that leave the provider carry the canonical tickers `AAPL` and `SP500`.
- The keys of the approved sample (`observation_date`, `open_value`, ..., `volume_value`) are teaching wrapper keys, not Bloomberg field names. The field names of a LIVE response were never observed, so they are not used anywhere.
- `fetch_raw_bloomberg_history()` is the LIVE boundary. It only raises `NotImplementedError`. The sample is read by `load_approved_sample_history()`.
- CSV, Yahoo and the Bloomberg stage all return rows with the same shape (`date`, `ticker`, `open`, `high`, `low`, `close`, `volume`). This is why `align_series()` and the three TD07 calculations are reused unchanged.
- `build_market_snapshot()` is the only place where the result is assembled. The terminal and the dashboard both read it, so they cannot show different values.
- `src/main.py` keeps `if __name__ == "__main__":`, so `dashboard.py` can import the snapshot builder without running the terminal program.
- `dashboard.py` does not call a provider and contains no formula. It only formats the snapshot values.
- Base 100 puts both series on the same scale (AAPL is around 250, the S&P 500 around 6 600). Both start at 100 because the series are aligned on common dates before the calculation.
- The approved sample and the CSV sample hold the same teaching values, which is why both give 6.48%, 2.15% and +4.33 percentage points.
- Reproducible means: repository + `requirements.txt` + documented commands give a working application on a clean setup. The default provider needs no credential and no internet access once the dependencies are installed.

## Security

No password, token, key or personal information appears in the screenshots.
