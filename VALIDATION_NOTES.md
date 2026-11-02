# Validation and corrections

## Checks performed

- Extracted the supplied project archive and reviewed its Python modules, configuration, tests, dataset and existing result artifacts.
- Confirmed the three input CSVs load with 26,460 device rows, 16 catalog rows and 96,000 settling-sweep rows.
- Ran the automated test suite after corrections: **25 tests passed**.
- Executed the predictive, baseline, adaptive, PAT, simulator, monitoring and consolidated-report stages in the validation environment.

## Corrections made

1. `run_all.py` now uses `sys.executable`, an absolute project config path, a stable working directory, and includes all project stages in dependency order.
2. `baseline.reconstructed_group_time()` now reconstructs stop-on-first-fail time per device and reports mean time by test group instead of simply summing catalog group times.
3. Predictive RUN/SKIP logic now forces RUN for a target test if the training lots contain failures unique to that test. This prevents the observed IDDQ_V4-only holdout escapes.
4. Adaptive decisions no longer inspect neighboring devices' final `sort_pass` labels, which would be unavailable at the time of an actual die-level decision.
5. PAT reporting clarifies that each detector's flag list is capped individually; the union of multiple detector flags can exceed the individual cap.
6. Added a consolidated `PROJECT_REPORT.md` generator and Windows launcher.

## Current validation result

- Automated tests: 25 passed.
- IDDQ_V4-only holdout failures audited: 4; skipped after the safety correction: **0**.
- Latest combined scorecard: approximately **34.69%** modeled time reduction, with **0 observed skipped-test escapes** in the holdout replay.
- The one-sided 95% Poisson upper bound is approximately **339.65 DPPM**, which is **above** the configured 50 DPPM budget. Therefore the combined scenario **does not pass the escape-risk gate** and must not be presented as production-qualified.

## Limitations still requiring engineering sign-off

- Synthetic data cannot establish real-device GR&R, tester capability, true DPPM, or production escape performance.
- The scorecard is a modeled replay, not a live tester implementation; the full combined time estimate depends on simplifying assumptions about stacking the optimization levers.
- Adaptive and predictive logic require shadow-mode validation, fail-safe integration, and independent review before any real test is skipped.
- Static-removal decisions require quality/customer approval and confidence-bound review on representative production volumes.
