import os
import subprocess
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLES = ROOT / "bundles"
EXPECTED = ROOT / "expected"
SCHEMA = ROOT / "schemas" / "expected_vector_v1.json"
RUNNER = ROOT / "scripts" / "run_vectors.py"

def _print(s: str) -> None:
    print(s, file=sys.stderr)

def _schema_validate_expected() -> None:
    try:
        import jsonschema  # type: ignore
    except Exception:
        _print("WARN: jsonschema not installed; skipping expected/*.json schema validation")
        return

    if not SCHEMA.is_file():
        raise RuntimeError(f"schema missing: {SCHEMA}")

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    failures: list[str] = []
    for p in sorted(EXPECTED.glob("*.json")):
        obj = json.loads(p.read_text(encoding="utf-8"))
        try:
            jsonschema.validate(instance=obj, schema=schema)
        except Exception as e:
            failures.append(f"{p.name}: {e}")

    if failures:
        msg = "schema validation failed:\n" + "\n".join(f"- {x}" for x in failures)
        raise AssertionError(msg)

def _run_vectors() -> subprocess.CompletedProcess[str]:
    verify_cmd = os.environ.get("OORD_VERIFY_CMD")
    if not verify_cmd:
        raise RuntimeError(
            "OORD_VERIFY_CMD not set.\n"
            "Example:\n"
            '  export OORD_VERIFY_CMD="PYTHONPATH=$HOME/code/oord-agent python -m cli.oord_cli verify"\n'
            "Then run:\n"
            "  pytest -q\n"
            "or:\n"
            "  python scripts/test_vectors.py\n"
        )

    if not RUNNER.is_file():
        raise RuntimeError(f"runner missing: {RUNNER}")
    if not BUNDLES.is_dir():
        raise RuntimeError(f"bundles dir missing: {BUNDLES}")
    if not EXPECTED.is_dir():
        raise RuntimeError(f"expected dir missing: {EXPECTED}")

    _print(f"ROOT={ROOT}")
    _print(f"OORD_VERIFY_CMD={verify_cmd}")
    _print(f"RUNNER={RUNNER}")
    _print(f"BUNDLES={BUNDLES}")
    _print(f"EXPECTED={EXPECTED}")

    return subprocess.run(
        ["python", str(RUNNER), str(BUNDLES), str(EXPECTED)],
        capture_output=True,
        text=True,
        env=os.environ.copy(),
    )

def test_vectors():
    _schema_validate_expected()
    p = _run_vectors()
    if p.returncode != 0:
        raise AssertionError(
            "runner failed\n"
            f"exit={p.returncode}\n"
            f"stdout=\n{p.stdout}\n"
            f"stderr=\n{p.stderr}\n"
        )

def main() -> int:
    _schema_validate_expected()
    p = _run_vectors()
    if p.stdout:
        print(p.stdout, end="")
    if p.stderr:
        print(p.stderr, end="", file=sys.stderr)
    return p.returncode

if __name__ == "__main__":
    raise SystemExit(main())
