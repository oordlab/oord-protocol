# oord-protocol

This repository is the **truth** for the Oord protocol.

It contains:

- the protocol specification (`spec/`)
- JSON Schemas (`schemas/`)
- canonical test vectors (`test-vectors/`)

It does **not** contain:

- service code
- agent code
- verifier code
- operational runbooks or deployment logic

## What “truth” means here

Truth is defined by (in order):

1. Spec text (normative semantics; MUST/SHOULD rules)
2. JSON Schemas (structural contract)
3. Canonical ZIP vectors (executable contract, pinned by SHA-256)

If Oord disappears, a third party must still be able to:

- read the spec
- validate artifacts against schemas
- replay vectors to verify tool behavior

## Directory layout

'''
spec/                 # normative semantics (MUST/SHOULD)
schemas/              # manifest, TL proof, expected vector schema
test-vectors/v1/
  bundles/            # canonical ZIP bundles (byte-for-byte)
  expected/           # expected verification results (machine-readable)
  SHA256SUMS          # pins bundle bytes
'''

## Versioning

Protocol versions are tagged and treated as immutable contracts.
See `VERSIONING.md`.
