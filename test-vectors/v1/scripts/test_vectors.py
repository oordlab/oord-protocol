import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLES = ROOT / "bundles"
EXPECTED = ROOT / "expected"
RUNNER = ROOT / "scripts" / "run_vectors.py"


def test_vectors():
    if not os.environ.get("OORD_VERIFY_CMD"):
        raise RuntimeError(
            "set OORD_VERIFY_CMD. Example:\n"
            'OORD_VERIFY_CMD="PYTHONPATH=~/code/oordlab/oord-agent python -m cli.oord_cli verify" pytest -q'
        )
    p = subprocess.run(
        ["python", str(RUNNER), str(BUNDLES), str(EXPECTED)],
        capture_output=True,
        text=True,
    )
    assert p.returncode == 0, f"runner failed\nstdout={p.stdout}\nstderr={p.stderr}"
