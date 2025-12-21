# Error model (protocol v1)

This document defines the normative meaning of verifier exit codes and reason identifiers.

## Exit codes (normative)

Verification tools MUST use these exit codes:

- `0`: PASS
  - all required checks succeeded

- `1`: FAIL (content / cryptographic)
  - the bundle is malformed, unsafe, tampered, or cryptographically invalid
  - examples:
    - schema invalid
    - unsafe ZIP layout
    - hash mismatch
    - Merkle root mismatch
    - signature invalid
    - required proof missing


- `2`: FAIL (environment/infra)
  - verification could not complete due to the environment
  - examples:
    - I/O error reading the bundle
    - verifier internal error
    - network required for an online check is unavailable
    - notary unreachable
    - authentication failure
    - timeout


Offline verification SHOULD NOT produce exit code `2` except for local environment failures
(e.g., I/O errors reading the bundle).

## Command-specific semantics

### `verify`

`verify` MAY emit exit codes `0`, `1`, or `2` as defined above.

Exit code `1` indicates a definitive content or cryptographic failure.

Exit code `2` indicates an environmental failure where retry MAY succeed once the environment is corrected.

### `seal`

In protocol v1:

- `seal` MUST NOT emit exit code `1`
- `seal` MAY emit:
  - `0` on success
  - `2` on environment or infrastructure failure

## Reason IDs

Tools SHOULD emit a set of `reason_ids` that explain failures at a stable identifier level.

Rules:

- checks reflect verifier-observable facts (e.g., `hashes_ok`, `manifest_sig_ok`)
- checks are machine-facing and protocol-visible
- tools MAY add new checks
- tools MUST NOT change the meaning of existing checks without a protocol version bump

The presence or absence of checks MUST NOT affect exit code semantics.

- `reason_ids` MUST be stable identifiers, not prose
- order MUST NOT be significant
- implementations MAY add new reason IDs over time, but MUST NOT repurpose existing IDs

## Boolean checks

Tools SHOULD emit a boolean map of checks.

Rules:

- check keys are stable machine identifiers (e.g., `hashes_ok`, `manifest_sig_ok`)
- tools MAY add new checks, but MUST NOT change the meaning of existing ones without a protocol version bump

## Human-readable output

Human-readable output (stdout/stderr text) is non-normative.

Vectors and protocol enforcement MUST rely on exit codes, reason IDs, and checks, not on stdout strings.
