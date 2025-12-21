# Canonicalization (JCS)

This document defines canonical JSON bytes used for signing and verification.

## Normative reference

Canonicalization MUST follow JSON Canonicalization Scheme (JCS), RFC 8785.

Implementations MUST:

- produce UTF-8 encoded bytes
- sort object keys as defined by JCS
- use JCS number formatting rules
- avoid whitespace not permitted by JCS canonical form

## Manifest bytes

The canonical bytes for `manifest.json` signature verification are defined in `manifest-v1.md`:

- the manifest object is canonicalized via JCS
- for signing and verification, `signature` is treated as the empty string (`""`)

The Notary (when used for signing) MUST sign the exact canonical bytes supplied by the client and MUST NOT
reserialize or recompute them.

## TL bytes

The canonical TL signed payload bytes are defined in `tl-proof-v1.md`.

## Implementation requirement

If two independent implementations process the same logical manifest content, they MUST converge on identical
canonical bytes prior to signing and verification.
