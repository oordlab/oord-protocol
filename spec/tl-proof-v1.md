# TL Proof v1

This document defines the normative semantics of `tl_proof.json` for v1 bundles.

## Schema

The JSON structure is defined by `schemas/tl_proof_v1.json`.

## Required fields (summary)

When present, `tl_proof.json` MUST include:

- `proof_version` (MUST equal `1.0`)
- `tl_seq` (integer >= 1)
- `merkle_root` (CID-style SHA-256 root)
- `sth_sig` (signature bytes; encoding is implementation-defined but MUST be stable)
- `t_log_ms` (integer >= 0)

It MAY include:

- `signer_key_id` (the `kid` used to verify `sth_sig`)

## Binding to the manifest

When `tl_proof.json` is present, `tl_proof.merkle_root` MUST equal `manifest.merkle.root_cid`.

If they do not match, verification MUST fail (exit code `1`).

## TL signature verification (offline)

When `tl_proof.json` is present and includes `signer_key_id`, the verifier MUST:

- locate the public key whose `kid` equals `tl_proof.signer_key_id` inside `jwks_snapshot.json`
- verify `sth_sig` using that key over the canonical TL-signed bytes defined below

If `signer_key_id` is missing, verifiers MAY treat TL signature verification as not-applicable for v1,
but MUST still apply all other consistency checks (schema, root binding, downgrade rules).

If `signer_key_id` is present but the key is missing or verification fails, verification MUST fail (exit code `1`).

## Canonical TL-signed bytes (normative)

The TL signed payload MUST be the UTF-8 bytes of the following ASCII string:

`"oord-tl-sth-v1:" + merkle_root + ":" + tl_seq + ":" + t_log_ms`

Where:

- `merkle_root` is the exact `tl_proof.merkle_root` string
- `tl_seq` and `t_log_ms` are base-10 integers with no leading plus sign

This is a minimal deterministic definition. Implementations MUST sign/verify these exact bytes for offline checks.

## Notes on time semantics

`t_log_ms` is an asserted log timestamp. Offline verification only checks it is syntactically valid and included
in the signed payload (when signature verification is applicable). Online semantics define additional consistency checks.