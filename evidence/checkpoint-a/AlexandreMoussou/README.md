# Checkpoint A - Alexandre Moussou

- GitHub username: AlexandreMoussou
- TD group / team: G07 - T07
- Team repository: `esilv-marketpulse-g07-turo`

## Evidence

| File | What it shows |
|---|---|
| `01_terminal_python.png` | `python src/main.py` running: AAPL and SP500 summary with observation dates |
| `02_git_status_log.png` | `git status` (clean tree) and `git log --oneline -5` with my commits |
| `03_branch_merge.png` | `git branch`, `git branch --merged` and the graph after merging `feature/display-observation-dates` into `main` (fast-forward) |

## What I did (TD01-TD04)

- TD02: reusable helpers `filter_prices`, `get_first_close`, `get_last_close`, `display_market_summary`.
- TD04: created `feature/display-observation-dates`, added `get_first_date` / `get_last_date`,
  committed `feat: display first and last observation dates`, compared it with `main`
  (`git diff main..feature/display-observation-dates`) and merged it into `main`.
  Git performed a fast-forward, so the graph stays linear; the feature branch is listed by `git branch --merged`.

## Merge conflict (concept)

A conflict happens when two branches change the same lines. Git stops, marks both versions
with `<<<<<<<`, `=======`, `>>>>>>>`, and a human chooses the final content, removes the markers,
runs `git add` and completes the merge.
