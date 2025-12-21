# Verification semantics

This document defines the normative verification steps for v1 bundles.

## Offline boundary

Offline verification MUST be fully bundle-contained:

- no network access is required
- no Notary service is required
- all public keys required for signature checks MUST be available in `jwks_snapshot.json` inside the bundle

Offline verification defines truth. Online checks may add confidence but MUST NOT redefine outcomes.

## Offline verification steps (normative order)

Given a bundle ZIP, the verifier MUST perform the following steps in order.

### 1. ZIP safety + layout

- enforce all safety rules in `bundle-format.md`
- require the presence of:
  - `manifest.json`
  - `jwks_snapshot.json`
  - `files/` directory

If ZIP safety or layout validation fails, verification MUST fail (exit `1`).

### 2. Manifest schema validation

- validate `manifest.json` against `schemas/manifest_v1.json`

If schema validation fails, verification MUST fail (exit `1`).

### 3. Manifest signature verification

- select the public key whose `kid` equals `manifest.key_id` from `jwks_snapshot.json`
- verify the Ed25519 signature over the canonical bytes defined in `manifest-v1.md`

If the key is missing or signature verification fails, verification MUST fail (exit `1`).

### 4. Payload hash verification

For each entry in `manifest.files[]`:

- read the payload bytes at `path`
- compute the SHA-256 digest
- require the digest matches `sha256`
- require the byte length matches `size_bytes`

If any payload hash or size check fails, verification MUST fail (exit `1`).

### 5. Merkle root verification

- recompute the Merkle root using the protocol-defined Merkle algorithm and leaf ordering
- require the recomputed root matches `manifest.merkle.root_cid`

If the Merkle root does not match, verification MUST fail (exit `1`).

### 6. TL downgrade rules (manifest-driven)

- read `manifest.tl_mode`
- apply the rules defined in `tl-downgrade-rules.md` to determine:
  - whether `tl_proof.json` is required
  - whether `tl_proof.json` is forbidden

If TL presence or absence violates `manifest.tl_mode`, verification MUST fail (exit `1`).

### 7. TL proof verification (when present)

If `tl_proof.json` is present:

- validate `tl_proof.json` against `schemas/tl_proof_v1.json`
- require `tl_proof.merkle_root == manifest.merkle.root_cid`
- if `tl_proof.signer_key_id` is present:
  - select the public key whose `kid` equals `tl_proof.signer_key_id` from `jwks_snapshot.json`
  - verify `tl_proof.sth_sig` over the canonical TL-signed bytes defined in `tl-proof-v1.md`

If any TL proof validation or verification step fails, verification MUST fail (exit `1`).

## Verification output surface

Verification tools SHOULD expose:

- an exit code (`0`, `1`, or `2`) as defined in `error-model.md`
- a set of `reason_ids` (stable identifiers)
- a map of boolean checks (machine-facing, protocol-visible)

Human-readable output is non-normative and MUST NOT be relied upon for correctness.
