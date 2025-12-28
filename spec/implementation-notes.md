# Implementation Notes (Non-Normative)

This document provides **practical guidance for implementers** of the Oord Protocol.
It does **not** define protocol semantics. Normative truth lives in the protocol specs,
schemas, and canonical test vectors.

---

## 1. Source of Truth Hierarchy

Implementations MUST treat protocol truth as ordered:

1. **Specification text** (`spec/*.md`)
2. **JSON Schemas** (`schemas/*.json`)
3. **Canonical ZIP vectors** (`test-vectors/` + `SHA256SUMS`)

If an implementation’s behavior disagrees with canonical vectors, the implementation is wrong.

---

## 2. Bundles Are the Unit of Truth

An Oord bundle is a **self-contained verification artifact**.

Offline verification MUST rely only on bundle contents:

- `manifest.json`
- payload files
- Merkle root
- `jwks_snapshot.json`
- optional `tl_proof.json`

Network access is never required to determine cryptographic validity.

---

## 3. Offline vs Online Verification

### Offline verification

Offline verification establishes **cryptographic truth**:

- structural safety
- hash integrity
- Merkle correctness
- signature validity
- optional Transparency Log proof verification

Offline verification MUST be deterministic and reproducible.

### Online verification

Online verification provides **additive consistency checks only**:

- TL inclusion / consistency confirmation
- freshness or anchoring confidence

Online verification MUST NOT redefine truth or override offline results.

Network failures, authorization failures, or service unavailability are **environmental failures**, not content failures.

---

## 4. Transparency Log (TL) Semantics

### TL inclusion

If a bundle declares `tl_mode = "included"`:

- `tl_proof.json` MUST be present
- missing proof is a verification failure

If `tl_mode = "none"`:

- `tl_proof.json` MUST NOT be present

### TL key selection

TL proof verification MUST:

- select the verification key explicitly referenced by `tl_key_id`
- verify against keys present in `jwks_snapshot.json`

Implicit key selection or fallback is forbidden.

---

## 5. Verifier Independence

The protocol is designed to support **multiple independent verifiers**.

No verifier is authoritative.
No verifier is required to be network-connected.
No verifier is required to trust a specific Notary operator.

Implementations should avoid embedding assumptions about:
- specific service endpoints
- operational policies
- organizational identity

---

## 6. Exit Codes and Error Classification

Verifiers SHOULD distinguish between:

- **Content / cryptographic failures** (bundle is invalid)
- **Environment / infrastructure failures** (verification could not complete)

Exact exit codes and reason identifiers are defined in verifier-specific contracts,
but protocol vectors assert expected outcomes where applicable.

---

## 7. Versioning and Evolution

Protocol versions are immutable once released.

Backward-compatible changes may:
- add optional fields
- add new reason identifiers
- add new canonical vectors

Backward-incompatible changes require a new protocol major version.

Implementers should pin to a specific protocol version and surface compatibility explicitly.

---

## 8. Non-Goals of the Protocol

The protocol does not define:

- Notary operations or SLAs
- key governance policy
- business rules or workflows
- enforcement or adjudication

Those belong to implementations and operating entities.

---

## 9. Reference Implementations

The reference verifier for this protocol lives in:

- `oord-verify`

Reference implementations are provided for clarity and testing, not authority.

