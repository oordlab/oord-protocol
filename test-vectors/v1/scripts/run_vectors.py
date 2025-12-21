#!/usr/bin/env python3
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, Tuple


def _load_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def _subset(expected: Any, actual: Any, path: str = "") -> Tuple[bool, str]:
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False, f"{path}: expected object, got {type(actual).__name__}"
        for k, v in expected.items():
            if k not in actual:
                return False, f"{path}/{k}: missing key"
            ok, msg = _subset(v, actual[k], f"{path}/{k}")
            if not ok:
                return False, msg
        return True, ""
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False, f"{path}: expected array, got {type(actual).__name__}"
        if expected != actual:
            return False, f"{path}: array mismatch expected={expected!r} actual={actual!r}"
        return True, ""
    if expected != actual:
        return False, f"{path}: value mismatch expected={expected!r} actual={actual!r}"
    return True, ""


def run_one(bundle_path: Path, expected_path: Path) -> None:
    verify_cmd = os.environ.get("OORD_VERIFY_CMD")
    if not verify_cmd:
        raise RuntimeError(
            "OORD_VERIFY_CMD is not set. Example: "
            'OORD_VERIFY_CMD="PYTHONPATH=~/code/oordlab/oord-agent python -m cli.oord_cli verify"'
        )

    cmd = verify_cmd.split() + [str(bundle_path), "--json"]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode not in (0, 1, 2):
        raise RuntimeError(f"unexpected verifier exit={p.returncode} stderr={p.stderr}")

    try:
        actual = json.loads(p.stdout)
    except Exception as e:
        raise RuntimeError(f"verifier did not emit valid JSON: {e}\nstdout={p.stdout}\nstderr={p.stderr}")

    expected = _load_json(expected_path)

    ok, msg = _subset(expected, actual, "")
    if not ok:
        raise AssertionError(
            f"vector mismatch\nexpected={expected_path}\nbundle={bundle_path}\n{msg}\n\nactual={json.dumps(actual, indent=2, sort_keys=True)}"
        )


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: run_vectors.py <bundles_dir> <expected_dir>", file=sys.stderr)
        return 2

    bundles_dir = Path(argv[1]).resolve()
    expected_dir = Path(argv[2]).resolve()

    for exp in sorted(expected_dir.glob("*.json")):
        stem = exp.stem
        bundle = bundles_dir / f"{stem}.zip"
        if not bundle.is_file():
            raise RuntimeError(f"missing bundle for expected vector: {bundle}")
        run_one(bundle, exp)

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
