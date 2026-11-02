"""Run the complete DC test-time optimization workflow in dependency order."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONFIG = ROOT / "config.yaml"
MODULES = (
    "dcopt.io",
    "dcopt.phase0_data_foundation",
    "dcopt.baseline",
    "dcopt.settling",
    "dcopt.static_reduction",
    "dcopt.ordering",
    "dcopt.predictive",
    "dcopt.adaptive",
    "dcopt.pat",
    "dcopt.simulator",
    "dcopt.monitoring",
    "dcopt.report",
    "dcopt.synthetic_dppm_validation",
)


def main() -> None:
    if not CONFIG.exists():
        raise FileNotFoundError(f"Project config not found: {CONFIG}")
    for index, module in enumerate(MODULES, start=1):
        print(f"\n[{index}/{len(MODULES)}] Running {module}...", flush=True)
        subprocess.run(
            [sys.executable, "-m", module, "--config", str(CONFIG)],
            cwd=ROOT,
            check=True,
        )
    print("\nAll project stages completed successfully.", flush=True)


if __name__ == "__main__":
    main()
