"""Large synthetic validation of the fail-safe full-flow policy.

This is a software/policy demonstration only. Because every device is sent
through the full test flow, no device is skipped; therefore skipped-device
escapes are zero by construction. It does NOT estimate real tester sensitivity
or qualify the semiconductor product for production.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy.stats import chi2


def upper_dppm(events: int, devices: int, confidence: float = 0.95) -> float:
    if devices <= 0:
        raise ValueError("devices must be positive")
    if events < 0 or not 0 < confidence < 1:
        raise ValueError("invalid events or confidence")
    return float(chi2.ppf(confidence, 2 * (events + 1)) / (2 * devices) * 1_000_000)


def run(config_path: str | Path, devices: int = 60000) -> Path:
    config_path = Path(config_path).resolve()
    if devices < 59915:
        raise ValueError("At least 59,915 independent devices are needed for a zero-event 95% upper bound below 50 DPPM")
    import yaml
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    confidence = float(config.get("confidence", 0.95))
    budget = float(config.get("dppm_budget", 50))

    # Synthetic device population. The fail-safe policy deliberately selects
    # RUN_FULL for every device; no model is allowed to bypass measurements.
    frame = pd.DataFrame({
        "synthetic_ecid": [f"SYN{i:07d}" for i in range(devices)],
        "decision": "RUN_FULL",
        "tests_skipped": 0,
        "synthetic_population": True,
    })
    skipped = int((frame["decision"] != "RUN_FULL").sum())
    skipped_defect_escapes = 0  # logically zero because no device is skipped
    dppm = upper_dppm(skipped_defect_escapes, devices, confidence)

    out = config_path.parent / config.get("paths", {}).get("results_dir", "results") / "10_synthetic_dppm"
    out.mkdir(parents=True, exist_ok=True)
    frame.to_csv(out / "synthetic_device_decisions.csv", index=False)
    passed = dppm <= budget
    report = [
        "# Synthetic DPPM safety demonstration", "",
        f"- Synthetic devices: {devices:,}",
        f"- Policy: fail-safe full flow (RUN every test on every device)",
        f"- Devices with tests skipped: {skipped:,}",
        f"- Skipped-device defect escapes: {skipped_defect_escapes}",
        f"- One-sided {confidence:.0%} Poisson upper bound: {dppm:.2f} DPPM",
        f"- Configured DPPM budget: {budget:.2f}",
        f"- Synthetic zero-skip DPPM gate: {'PASS' if passed else 'FAIL'}",
        "- Time-reduction gate: NOT CLAIMED; full flow provides no skip-based time reduction.",
        "", "## Important limitation", "",
        "This is a synthetic software/policy demonstration, not evidence of actual defect escape probability. "
        "The zero-event result is guaranteed by the full-flow policy (no tests are skipped). "
        "It does not measure tester sensitivity, test coverage, false negatives, process variation, or real-device DPPM. "
        "Do not use this result for production qualification or customer quality claims.", "",
    ]
    (out / "summary.md").write_text("\n".join(report), encoding="utf-8")
    print("\n".join(report))
    return out


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--devices", type=int, default=60000)
    args = parser.parse_args()
    run(args.config, args.devices)


if __name__ == "__main__":
    main()
