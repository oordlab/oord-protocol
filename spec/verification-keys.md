# Verification keys

This document defines how verifiers select public keys to verify signatures.

## Bundle-contained key material

All public keys required for offline verification MUST be bundle-contained.

The bundle MUST include `jwks_snapshot.json`, which is a JSON Web Key Set (JWKS).

Offline verification MUST NOT require fetching keys from a network location.

## Key selection by kid (non-negotiable)

When verifying a signature, the verifier MUST select a key by exact `kid` match.

- no fallback to “the only key”
- no selection by algorithm alone
- no selection by ordering

If the required `kid` is not present, verification MUST fail (exit `1`).

## Manifest signature key selection

To verify the manifest signature:

- the verifier MUST select the key whose `kid` equals `manifest.key_id`
- the verifier MUST verify the signature over the canonical manifest bytes (see `manifest-v1.md`)

## TL proof signature key selection

When `tl_proof.json` includes `signer_key_id`:

- the verifier MUST select the key whose `kid` equals `tl_proof.signer_key_id`
- the verifier MUST verify the TL signature over the canonical TL-signed bytes (see `tl-proof-v1.md`)

If `signer_key_id` is present but the key is missing, verification MUST fail (exit `1`).

If `signer_key_id` is absent, verifiers MAY treat TL signature verification as not-applicable for v1,
but MUST still apply schema validation and root binding checks.
