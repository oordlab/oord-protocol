# Online semantics

This document defines the **normative behavior** of online verification in Oord v1.

Online verification exists to provide **additional consistency confidence** against a live Transparency Log (TL) / Notary service. It does **not** redefine truth.

---

## Core invariants (non-negotiable)

1. **Offline verification defines truth**

   * If offline verification fails, online checks MUST NOT change the result.
   * Online checks are never required to establish bundle validity.

2. **Online checks are strictly additive**

   * Online checks may confirm that the bundle’s assertions are consistent with a live service.
   * Online checks MUST NOT relax, reinterpret, or override offline failures.

3. **Bundles remain self-contained**

   * A bundle that passes offline verification is valid regardless of online availability.
   * Online checks only affect the verifier’s *confidence*, not the bundle’s *meaning*.

---

## When online checks apply

Online checks SHOULD only be attempted when **all** of the following are true:

* Online mode is explicitly enabled (e.g. `--online` or `--tl-url`)
* The bundle includes `tl_proof.json`
* The bundle’s manifest declares `tl_mode = "included"`

If `tl_mode = "none"` or no TL proof is present, online checks MUST be skipped and MUST NOT cause failure.

---

## What online verification is allowed to check (v1)

In protocol v1, online verification MAY perform **only** the following consistency check:

* Fetch the TL entry at the sequence number asserted in the bundle
* Confirm that:

  * `seq` matches the bundle’s asserted sequence
  * `merkle_root` matches the bundle’s asserted Merkle root

This is the **only** online contradiction check defined in v1.

---

## Explicitly out of scope (v1)

Online verification MUST NOT fail a bundle due to:

* Differences in TL signature encoding (`sth_sig`)
* Differences in TL signing format or implementation details
* Absence of additional TL metadata beyond `(seq, merkle_root)`
* Operational policy differences between Notary implementations

These MAY be standardized in a future protocol version, but are **non-normative in v1**.

---

## Contradiction definition (strict, v1)

A **cryptographic contradiction** exists **only if**:

* the live TL entry’s `seq` differs from the bundle’s asserted `seq`, **or**
* the live TL entry’s `merkle_root` differs from the bundle’s asserted Merkle root

If and only if such a contradiction is observed:

* The verifier MUST treat this as a **content failure**
* The verifier MUST exit with code **`1`**
* The verifier MUST emit a stable reason identifier (e.g. `TL_ONLINE_CONTRADICTION`)

---

## Non-contradictions (environment / infra)

The following outcomes MUST NOT be treated as content failures:

* TL / Notary unreachable
* Timeout
* Authentication or authorization failure
* HTTP errors
* Malformed or incomplete responses
* “Not found” responses without cryptographic contradiction

These cases indicate **environment or infrastructure failure**, not bundle invalidity.

For such cases:

* The verifier MUST exit with code **`2`**
* The verifier MUST emit an environment-class reason identifier (e.g. `TL_ONLINE_UNREACHABLE`)

---

## Exit code mapping (normative)

Online verification MUST follow the exit code definitions in `error-model.md`.

Additionally:

| Situation                                     | Exit code |
| --------------------------------------------- | --------- |
| Offline verification fails                    | `1`       |
| Offline passes, online skipped                | `0`       |
| Offline passes, online confirms consistency   | `0`       |
| Offline passes, online contradiction detected | `1`       |
| Online checks unavailable (infra/env)         | `2`       |

---

## Summary (one sentence)

**Online verification in v1 only answers one question:
“Does the live Transparency Log agree with the bundle’s asserted `(seq, merkle_root)`?”
Nothing more.**

