# Repo Context Index

## Directory Tree (trimmed)
.
├── context
│   └── prtcl-context-index.md
├── LICENSE
├── schemas
│   ├── expected_vector_v1.json
│   ├── manifest_v1.json
│   └── tl_proof_v1.json
├── scripts
│   └── ctx.sh
├── spec
│   ├── bundle-format.md
│   ├── canonicalization-jcs.md
│   ├── error-model.md
│   ├── manifest-v1.md
│   ├── online-semantics.md
│   ├── tl-downgrade-rules.md
│   ├── tl-proof-v1.md
│   ├── verification-keys.md
│   └── verify-semantics.md
└── test-vectors
    └── v1

7 directories, 15 files

## Grep (router/models/merkle/signature)
scripts/ctx.sh:13:echo "## Grep (router/models/merkle/signature)" >> "$OUT"
scripts/ctx.sh:16:  -e '@router\.|FastAPI\(|Pydantic|Schema|type ' \
scripts/ctx.sh:17:  -e 'Merkle|verify|sign|ed25519|sha256' | head -n 300 >> "$OUT"
schemas/tl_proof_v1.json:16:        "pattern": "^cid:sha256:[0-9a-f]{64}$"
schemas/tl_proof_v1.json:25:      "signer_key_id": {
schemas/manifest_v1.json:14:      "signature"
schemas/manifest_v1.json:28:        "description": "Hash algorithm used for per-file digests and Merkle leaves",
schemas/manifest_v1.json:29:        "enum": ["sha256"]
schemas/manifest_v1.json:37:            "pattern": "^cid:sha256:[0-9a-f]{64}$"
schemas/manifest_v1.json:41:            "enum": ["binary_merkle_sha256"]
schemas/manifest_v1.json:51:          "required": ["path", "sha256", "size_bytes"],
schemas/manifest_v1.json:58:            "sha256": {
schemas/manifest_v1.json:67:      "signature": { "type": "string", "minLength": 1 },
LICENSE:60:      designated in writing by the copyright owner as "Not a Contribution."
context/prtcl-context-index.md:23:│   └── verify-semantics.md
context/prtcl-context-index.md:29:## Grep (router/models/merkle/signature)

## Recent Commits
- d5c5aa9 Initial commit
