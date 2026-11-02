# Synthetic DPPM safety demonstration

- Synthetic devices: 60,000
- Policy: fail-safe full flow (RUN every test on every device)
- Devices with tests skipped: 0
- Skipped-device defect escapes: 0
- One-sided 95% Poisson upper bound: 49.93 DPPM
- Configured DPPM budget: 50.00
- Synthetic zero-skip DPPM gate: PASS
- Time-reduction gate: NOT CLAIMED; full flow provides no skip-based time reduction.

## Important limitation

This is a synthetic software/policy demonstration, not evidence of actual defect escape probability. The zero-event result is guaranteed by the full-flow policy (no tests are skipped). It does not measure tester sensitivity, test coverage, false negatives, process variation, or real-device DPPM. Do not use this result for production qualification or customer quality claims.
