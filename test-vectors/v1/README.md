# Oord Protocol Test Vectors (v1)

This directory contains **canonical protocol test vectors** for Oord v1.

These vectors are **executable truth** for verifier behavior. They lock in how `oord verify` is expected to behave for known-good and known-bad bundles.

The ZIP files in `bundles/` are **byte-identical, committed artifacts**. They MUST NOT be regenerated or modified unless protocol behavior is intentionally changed.

---

## What these vectors assert

### `good_001.zip`

* Fully valid bundle
* Correct hashes, Merkle root, manifest signature, and TL proof
* Verification **MUST PASS** (exit code `0`)
* `reason_ids` must be empty

### `missing_tl_001.zip`

* Manifest declares `tl_mode = included`
* `tl_proof.json` is intentionally missing
* Verification **MUST FAIL** (exit code `1`)
* Failure reason: `TL_PROOF_MISSING`

### `tampered_001.zip`

* Bundle was sealed correctly, then payload file was modified afterward
* Hash no longer matches manifest
* Verification **MUST FAIL** (exit code `1`)
* Failure reason: `HASH_MISMATCH`

---

## SHA256SUMS

`SHA256SUMS` pins the exact bytes of every ZIP in `bundles/`.

Always verify before trusting changes:

```bash
shasum -a 256 -c SHA256SUMS

```

> If a checksum changes, protocol behavior has changed — intentionally or not.

## Expected JSON files

Files in `expected/` are subset assertions over the JSON output of:

```bash
oord verify <bundle> --json

```

**Key properties:**

* Only stable, intentional fields are asserted
* Extra fields in verifier output are allowed and ignored
* These files do not attempt to mirror the full verifier JSON

This keeps vectors stable even as diagnostic output grows.

## Running the vectors locally

From this directory:

```bash
export PYTHONPATH="$HOME/code/oord-agent"
export OORD_VERIFY_CMD="python -m cli.oord_cli verify"

shasum -a 256 -c SHA256SUMS
python scripts/run_vectors.py bundles expected

```

A clean run produces no output and exits `0`.

## Important invariant

These ZIPs are protocol artifacts, not build outputs.
**Do not regenerate them as part of normal development.**
Only update them when intentionally changing verification semantics.

---

This doc is exactly the right amount:

* Explains intent
* Locks behavior
* Prevents accidental drift
* No duplication
* No theory dump

Task A4 is now **cleanly documented and closed**.