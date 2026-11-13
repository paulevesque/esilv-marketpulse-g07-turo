# Checkpoint A - @Amd19z

## Scope

Checkpoint Phase A - TD01 to TD04.

## Evidence files

| File | Content |
|---|---|
| `01_terminal_python.png` | `python src/main.py` runs and displays the instrument (AAPL) and benchmark (SP500) summaries, including the new `Period high` and `Period low` lines |
| `02_git_status_log.png` | `git status` (clean working tree on `main`) and `git log --oneline -5` showing the feature commit at the top of `main` |
| `03_branch_merge.png` | `git branch`, `git branch --merged` and `git log --oneline --graph --decorate --all -10`, captured before deleting the merged feature branch |

## TD04 - Branches + Merge

- Feature branch: `feature/display-period-high-low`
- Feature commit: `5c036a1 feat: display period high and low`
- Feature: display the highest `high` and the lowest `low` of the period for the instrument (AAPL) and the benchmark (SP500). Two helpers, `get_period_high` and `get_period_low`, are called from the existing reusable `display_market_summary` function, so both series are covered without duplicated code. No return is calculated (planned for TD07).
- Validation: `python src/main.py` runs; values cross-checked against `data/sample/prices.csv` (AAPL 267.70 / 248.00 USD, SP500 6757.00 / 6580.00).
- Comparison: `git diff main..feature/display-period-high-low` showed only the intended change in `src/main.py`.
- Merge type: fast-forward. `main` had no new commit since the branch was created, so Git moved `main` forward to the feature commit. No merge commit was forced.
- After capture, the merged branch was deleted with `git branch -d`. The feature commit remained in the local `main` history.
- This TD04 work was a local learning exercise and was not pushed to the team `main`. Before TD05, local `main` was aligned with `origin/main` (Team Baseline Gate), and the TD04 history was preserved in the local branch `archive/td04-local`.

## Understanding

- A feature branch isolates work: the change is not part of `main` until it is merged. An abandoned branch leaves `main` unchanged.
- A merge conflict happens when two branches change the same area of a file. Git marks the competing versions with `<<<<<<<`, `=======` and `>>>>>>>`, and a human chooses the final content before `git add` and completing the merge.

## Security

No password, token, key or personal secret appears in the screenshots.
