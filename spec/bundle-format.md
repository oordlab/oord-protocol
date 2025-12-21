# Bundle format (v1)

This document defines the normative ZIP layout and safety rules for an Oord bundle.

## Required ZIP entries

A v1 bundle MUST contain the following files:

- `manifest.json`
- `jwks_snapshot.json`

A v1 bundle MUST contain the following directory:

- `files/` (containing one or more payload files)

A v1 bundle MAY contain:

- `tl_proof.json` (when TL proof is included; see `tl-downgrade-rules.md`)
- `receipt.txt` (human-readable, non-normative)

## Path and extraction safety

Verifiers and tools that read or extract bundles MUST apply all of the following:

- ZIP entries MUST NOT be absolute paths.
- ZIP entries MUST NOT contain `..` path segments.
- ZIP entries MUST NOT contain backslashes (`\`) as path separators.
- ZIP entries MUST NOT be symlinks (if the ZIP format exposes them).
- Extraction MUST prevent zip-slip (i.e., writing outside the chosen output directory).
- Tools MUST treat all ZIP entry names as untrusted input.

If any safety rule is violated, verification MUST fail with a content failure (exit code `1`).

## Payload file namespace

All payload files referenced by the manifest MUST live under `files/`.

- Each `files[].path` in `manifest.json` MUST begin with `files/`.
- Each referenced path MUST exist as a ZIP entry.

## Determinism requirements for canonical vectors

Protocol test vectors stored under `test-vectors/` are canonical ZIPs pinned by SHA-256.

When producing canonical vectors, the ZIP bytes MUST be stable across runs:

- file ordering in the ZIP MUST be deterministic
- per-entry timestamps MUST be deterministic (fixed or derived deterministically)
- per-entry permissions/modes (if present) MUST be deterministic
- compression settings MUST be deterministic

These determinism constraints are REQUIRED for protocol vectors and RECOMMENDED for production tooling.

## Offline verification boundary

Offline verification MUST be bundle-contained:

- verifiers MUST NOT require network access to verify a bundle
- verifiers MUST NOT require a running Notary to verify a bundle
