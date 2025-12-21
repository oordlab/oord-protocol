# Manifest v1

This document defines the normative semantics of `manifest.json` for v1 bundles.

## Schema

The JSON structure of the manifest is defined by `schemas/manifest_v1.json`.

## Required fields (summary)

`manifest.json` MUST include:

- `manifest_version` (MUST equal `1.0`)
- `org_id`
- `batch_id`
- `created_at_ms`
- `key_id` (public key identifier used to verify the manifest signature)
- `hash_alg` (MUST be `sha256`)
- `tl_mode` (declares whether TL proof is forbidden or required; see below)
- `merkle.root_cid` (CID-style SHA-256 root)
- `merkle.tree_alg` (MUST be `binary_merkle_sha256`)
- `files[]` (one or more entries)
- `signature` (Ed25519 signature over canonical bytes; see below)

## TL mode semantics (normative)

`tl_mode` declares the required TL proof behavior for the bundle and is part of the signed manifest.

Valid values:

- `none`:
  - the bundle MUST NOT include `tl_proof.json`
- `included`:
  - the bundle MUST include `tl_proof.json`
  - the TL proof MUST verify against the bundle (see verifier semantics and TL proof rules)

## File list semantics

For each element in `files[]`:

- `path` MUST be a relative path beginning with `files/`
- `path` MUST NOT contain `..` or `\`
- `sha256` MUST be the SHA-256 digest (lowercase hex) of the referenced payload bytes
- `size_bytes` MUST equal the size in bytes of the referenced payload bytes

The list of files in `files[]` MUST be sufficient to recompute the Merkle root claimed in `merkle.root_cid`.

## Merkle root semantics

The `merkle.root_cid` value MUST be recomputable from the payload file set and digest values.

The Merkle computation rules (leaf construction, ordering, and parent hashing) are specified in the verifier semantics.

## Manifest signature (normative)

The manifest signature exists to bind the manifest fields to a signing key.

### Canonical bytes

The bytes to be signed/verified are the JSON Canonicalization Scheme (JCS) canonical form (RFC 8785) of the manifest
object with the following rule:

- For signing and verification, the `signature` field MUST be treated as the empty string (`""`).

Equivalently:

1. Take the manifest JSON object.
2. Set `signature` to `""`.
3. Canonicalize using JCS to obtain bytes.
4. Sign/verify those exact bytes.

This rule prevents ambiguity about whether the `signature` field is included in the signed payload.

### Verification key selection

To verify `manifest.signature`, the verifier MUST:

- locate the public key whose `kid` equals `manifest.key_id` inside `jwks_snapshot.json` in the bundle
- verify the Ed25519 signature over the canonical bytes defined above

If the key is missing, verification MUST fail (exit code `1`).

## Deprecated fields

The `tl_proof` field inside the manifest is deprecated in v1 bundles.

- if present, it MUST be ignored for verification
- TL proof (when included) is carried in a separate `tl_proof.json`
