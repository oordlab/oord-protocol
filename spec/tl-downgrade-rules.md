# TL downgrade rules

This document defines how bundles declare and enforce the presence of transparency log (TL) proof material.

## TL modes (v1)

In v1, TL mode is declared by the manifest field `manifest.tl_mode` and is therefore part of signed truth.

Valid modes:

- `none`: TL proof is forbidden
- `included`: TL proof is required

Verifiers MUST determine TL requirements exclusively from `manifest.tl_mode`.
Verifiers MUST NOT infer TL requirements from configuration, environment, or vector metadata.

## Mode: none

If `manifest.tl_mode` is `none`:

- the bundle MUST NOT include `tl_proof.json`
- verifiers MUST report `tl_present=false`

If `tl_proof.json` is present when `manifest.tl_mode` is `none`, verification MUST fail (exit `1`).

## Mode: included

If `manifest.tl_mode` is `included`:

- the bundle MUST include `tl_proof.json`
- verifiers MUST report `tl_present=true`

If `tl_proof.json` is missing when `manifest.tl_mode` is `included`, verification MUST fail (exit `1`).

If `tl_proof.json` is present but does not validate or does not verify, verification MUST fail (exit `1`).

## Notes

This rule prevents silent downgrades where a producer claims TL-backed evidence but omits proof material.

Because `tl_mode` is signed, the presence or absence requirements are cryptographically bound to the bundle.
