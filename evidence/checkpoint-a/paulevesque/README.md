# Checkpoint A - @paulevesque

## Scope

Checkpoint Phase A - TD01 to TD04.

## Evidence files

| File | Content |
|---|---|
| `01_terminal_python.png` | `python src/main.py` runs and displays instrument and benchmark summaries with first and last observation dates |
| `02_git_status_log.png` | `git status` (clean working tree) and `git log --oneline -5` |
| `03_branch_merge.png` | `git branch`, `git branch --merged` and `git log --oneline --graph --decorate --all`, captured before deleting the merged feature branch |

## TD04 - Branches + Merge

- Feature branch: `feature/display-observation-dates`
- Feature commit: `feat: display first and last observation dates`
- Feature: display first date, last date, first close and last close for the instrument (AAPL) and the benchmark (SP500) through a reusable `display_market_summary` function.
- Merge type: fast-forward. `main` had no new commit since the branch was created, so Git moved `main` forward to the feature commit. No merge commit was forced.
- After capture, the merged branch was deleted with `git branch -d`. The feature commit remains in the `main` history.

## Understanding

- A feature branch isolates work: the change is not part of `main` until it is merged. An abandoned branch leaves `main` unchanged.
- A merge conflict happens when two branches change the same area of a file. Git marks the competing versions with `<<<<<<<`, `=======` and `>>>>>>>`, and a human chooses the final content before `git add` and completing the merge.

## Security

No password, token, key or personal information appears in the screenshots.
