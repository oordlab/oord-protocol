# Protocol versioning

This repository versions the **protocol contract**, not an implementation.

## What is versioned

A protocol version includes:

- spec text under `spec/`
- schemas under `schemas/`
- test vectors under `test-vectors/`

## Immutability rule

Once a protocol version is tagged (e.g. `v1.0.0`):

- its contents are treated as immutable
- changes require a new protocol version tag

This is non-negotiable. Tooling can evolve, but protocol truth must remain stable.

## Semantic versioning

We use SemVer for protocol tags:

- **MAJOR**: incompatible format/semantic change
- **MINOR**: backward-compatible extension (new optional fields, new vectors)
- **PATCH**: clarifications and corrections that do not change verifier outcomes for existing vectors
