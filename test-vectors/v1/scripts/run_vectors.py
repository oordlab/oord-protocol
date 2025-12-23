#!/usr/bin/env python3
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Tuple


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


def _die(msg: str, code: int = 2) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def _parse_verify_cmd() -> list[str]:
    verify_cmd = os.environ.get("OORD_VERIFY_CMD")
    if not verify_cmd:
        _die(
            "OORD_VERIFY_CMD is not set.\n"
            "Example:\n"
            '  export PYTHONPATH="$HOME/code/oord-agent"\n'
            '  export OORD_VERIFY_CMD="python -m cli.oord_cli verify"\n'
        )
    try:
        parts = shlex.split(verify_cmd)
    except ValueError as e:
        _die(f"OORD_VERIFY_CMD could not be parsed: {e}\nvalue={verify_cmd!r}")
    if not parts:
        _die("OORD_VERIFY_CMD is empty after parsing")
    return parts


def run_one(bundle_path: Path, expected_path: Path, verify_parts: list[str]) -> None:
    cmd = verify_parts + [str(bundle_path), "--json"]
    p = subprocess.run(cmd, capture_output=True, text=True)

    if p.returncode not in (0, 1, 2):
        _die(
            "unexpected verifier exit.\n"
            f"  exit={p.returncode}\n"
            f"  cmd={' '.join(cmd)}\n"
            f"  stderr={p.stderr.strip()}"
        )

    if not p.stdout.strip():
        _die(
            "verifier produced empty stdout.\n"
            f"  cmd={' '.join(cmd)}\n"
            f"  stderr={p.stderr.strip()}"
        )

    try:
        actual = json.loads(p.stdout)
    except Exception as e:
        _die(
            "verifier did not emit valid JSON.\n"
            f"  err={e}\n"
            f"  cmd={' '.join(cmd)}\n"
            f"  stdout={p.stdout}\n"
            f"  stderr={p.stderr}"
        )

    expected = _load_json(expected_path)

    ok, msg = _subset(expected, actual, "")
    if not ok:
        raise AssertionError(
            "vector mismatch\n"
            f"expected={expected_path}\n"
            f"bundle={bundle_path}\n"
            f"{msg}\n\n"
            f"actual={json.dumps(actual, indent=2, sort_keys=True)}"
        )


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("usage: run_vectors.py <bundles_dir> <expected_dir>", file=sys.stderr)
        print("env:", file=sys.stderr)
        print("  OORD_VERIFY_CMD: verifier command prefix (required)", file=sys.stderr)
        return 2

    bundles_dir = Path(argv[1]).expanduser().resolve()
    expected_dir = Path(argv[2]).expanduser().resolve()

    if not bundles_dir.is_dir():
        _die(f"bundles_dir is not a directory: {bundles_dir}")
    if not expected_dir.is_dir():
        _die(f"expected_dir is not a directory: {expected_dir}")

    verify_parts = _parse_verify_cmd()

    expected_files = sorted(expected_dir.glob("*.json"))
    if not expected_files:
        _die(f"no expected vectors found in: {expected_dir}")

    ran = 0
    for exp in expected_files:
        stem = exp.stem
        bundle = bundles_dir / f"{stem}.zip"
        if not bundle.is_file():
            _die(f"missing bundle for expected vector: {bundle}")

        run_one(bundle, exp, verify_parts)
        ran += 1

    print(f"VECTORS_OK count={ran} bundles_dir={bundles_dir} expected_dir={expected_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
