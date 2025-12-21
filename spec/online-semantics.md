# Online semantics

This document defines what an online verification mode is allowed to do.

## Core rule

Online checks MUST be additive.

- Offline verification defines truth.
- Online verification can only add consistency confidence.
- Online results MUST NOT override offline failures.

## When online checks apply

Online checks SHOULD only be attempted when `tl_proof.json` is present.

Online checks MAY query a Notary / TL service to confirm inclusion and consistency for the bundle’s Merkle root.

## Exit code mapping (normative)

Online verification MUST use the exit codes defined in `error-model.md`.

In addition:

- If online checks cannot be performed due to environment/infra issues (unreachable, timeout, auth failure),
  the process MUST exit with code `2`.

- If online checks produce a cryptographic contradiction with the bundle’s assertions, the process MUST exit with code `1`.

## Contradiction definition (strict)

A contradiction exists only when:

- the remote service provides proof material that cryptographically conflicts with the bundle’s asserted Merkle root,
  sequence, or signed statements.

Operational disagreement or “not found” responses without cryptographic proof MUST be treated as an environment/infra
result (exit `2`), not as a content failure.
