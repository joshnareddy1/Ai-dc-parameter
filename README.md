# AI-Optimized DC Parametric Test-Time Reduction

A reproducible Python project that evaluates measurement-settling optimization, static test coverage reduction, test ordering, predictive RUN/SKIP decisions, adaptive flow, PAT, scorecard replay, and monitoring using the supplied synthetic dataset.

> **Important:** The supplied data is synthetic. Results demonstrate the workflow only; they do not qualify a real semiconductor test program for production release.

## 1. Project contents

- `data/` – supplied CSV datasets, data dictionary/README, and methodology PDF.
- `dcopt/` – implementation modules for data loading, validation, baseline, settling, static reduction, ordering, predictive, adaptive, PAT, simulation, monitoring, and reporting.
- `tests/` – automated unit tests.
- `config.yaml` – dataset paths, lot split, thresholds, and validation settings.
- `run_all.py` / `run_all.bat` – complete workflow launcher.
- `results/` – generated CSV summaries, plots, and consolidated project report from the latest completed validation run.

## 2. Run in VS Code on Windows

Open the `Devsys` folder in VS Code. Open Terminal → New Terminal and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

If PowerShell blocks activation, run this once in that terminal and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Run automated tests:

```powershell
py -m pytest -q
```

Run the complete project:

```powershell
py run_all.py
```

Or double-click `run_all.bat` after installing dependencies.

## 3. Output locations

Each stage writes its output under `results/`:

1. `io/` – input row counts and null report.
2. `phase0_data_foundation/` – data-quality and lot-split checks.
3. `01_baseline/` – yield, test failures, capability, baseline time.
4. `02_settling/` – settling curves, bias/noise metrics and recommendations.
5. `03_static/` – correlation, unique-failure risk and static-reduction decisions.
6. `04_ordering/` – original vs ranked test-order replay.
7. `05_predictive/` – prediction intervals, RUN/SKIP decisions and coverage metrics.
8. `06_adaptive/` – lot and die flow decisions.
9. `07_pat/` – PAT scores, flags and holdout metrics.
10. `08_scorecard/` – combined time-saving and escape-risk scenarios.
11. `09_monitoring/` – monitoring timeline and alarms.
12. `PROJECT_REPORT.md` – consolidated report.

## 4. Safety and validation rules

- Lots are split into training and holdout groups; do not randomly split individual dies.
- `is_latent_defect_truth` is for PAT evaluation only and must never be a model feature.
- Predictive models may recommend RUN or SKIP; measured limits remain authoritative.
- A test with unique failures in training lots is forced to RUN by the predictive safety guard.
- Adaptive decisions must not use neighboring devices' final pass/fail labels, because those labels are not available at decision time.
- Any uncertainty or execution error should fall back to full test flow in a production implementation.
- A scorecard passing the time-reduction target does not mean it passes the DPPM budget. Both gates must pass independently.

## 5. Reproducibility

The random seed, lot split, limits, and thresholds are configured in `config.yaml`. Avoid editing generated files under `results/` by hand; rerun the workflow to regenerate them.
