# Checkpoint C - Amary Diarra

- GitHub username: Amd19z
- TD group / team: G07 - T07
- Team repository: `esilv-marketpulse-g07-turo`
- Final provider / mode: **Bloomberg stage - APPROVED_SAMPLE** (not live Bloomberg)

## Evidence

| File | What it shows |
|---|---|
| `01_final_market_data.png` | `python src/main.py` on merged `main`: `Provider : Bloomberg stage - APPROVED_SAMPLE`, access mode line, AAPL vs SP500, 1 month, Daily, 21 common dates, period returns, relative performance and base 100 |
| `02_dash_dashboard.png` | `python src/dashboard.py` in Safari: provider, instrument, benchmark, lookback, interval, the three indicators (+6.48%, +2.15%, +4.33 pts) and the base-100 chart with AAPL and SP500 |
| `03_final_pull_request.png` | My approving review on Pull Request #15 `feat: add Bloomberg provider boundary` (TD10, AlexandreMoussou), after checking out and testing the branch; #15 was then merged |
| `04_reproducible_run.png` | Clean run on macOS, Python 3.13, two terminal captures stacked: fresh `git clone` of the team repository, new virtual environment, `python -m pip install -r requirements.txt` (successful), `python src/main.py` (expected output) and `python src/dashboard.py` (`Dash is running on http://127.0.0.1:8050/`) |

## What I did (TD09-TD12)

- TD09: Pull Request #14 `docs: draw the Bloomberg provider boundary`, adding to
  `docs/BLOOMBERG_FIELD_MAPPING.md` where Bloomberg names stop (`SPX Index`, `*_value` keys)
  and canonical rows start. Reviewed by paulevesque and merged. Before that, Pull Request #13
  `refactor: resolve Yahoo symbols inside the provider` (also reviewed and merged).
- TD10-TD12: implemented the three labs on my own branches (Pull Requests #17, #18, #19:
  Bloomberg provider, Dash dashboard, final release), approved by paulevesque. The team merged
  AlexandreMoussou's equivalent PRs, so mine were closed without merge.
- Reviews: approved #15 (TD10), #16 (TD11) and #20 (TD12) by AlexandreMoussou after running
  his branch: 42 normalized rows equal to `bloomberg_reference_expected.json`, csv / yahoo /
  bloomberg paths, unmapped ticker, import safety, dashboard values equal to the terminal,
  no formula or provider call in `dashboard.py`. Non-blocking remark on `app.layout`.
- Clean reproducibility test: fresh clone + new virtual environment + install + both commands.

## Concepts

- `AAPL US Equity` and `SPX Index` exist only in `src/providers/bloomberg_provider.py`;
  rows leave the provider with the canonical tickers `AAPL` and `SP500`.
- The approved sample uses teaching wrapper keys (`observation_date`, `close_value`, ...),
  which are not Bloomberg field mnemonics.
- `build_market_snapshot()` in `src/main.py` is the single calculation path; the terminal and
  the dashboard only present it, so they show the same values.
- `src/analytics.py` did not change for Bloomberg: same `align_series()`, period return,
  base 100 and relative performance as for CSV and Yahoo.
- APPROVED_SAMPLE validates the provider boundary and normalization, not live Bloomberg
  connectivity. The sample values come from `data/sample/prices.csv`, which is why the
  results are the same as the CSV path.
