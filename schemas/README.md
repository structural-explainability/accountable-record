# Schemas

Machine-readable schemas for the AR contract.

The schemas under this directory are the normative machine artifacts.
Where prose in the spec documents and these schemas disagree, the
schemas govern. Where they agree, both are normative.

## Files

| File                     | Specifies                       | Spec doc                |
| ------------------------ | ------------------------------- | ----------------------- |
| `bundle-1.json`          | The AR bundle envelope.         | `EXPORT_CONTRACT.md`    |
| `profile-1.json`         | The AR profile document.        | `EXPORT_CONTRACT.md`    |
| `report-1.json`          | The verifier's report document. | `VERIFICATION_MODEL.md` |
| `comparison-1.json`      | The output of `compare`.        | `VERIFICATION_MODEL.md` |
| `claim-spec.schema.json` | The shape of a claim TOML file. | `CLAIMS.md`             |
| `trait-spec.schema.json` | The shape of a trait TOML file. | `TRAITS.md`             |
| `claims/AR.CLAIM.*.toml` | Per-claim definitions.          | `CLAIMS.md`             |
| `traits/AR.TRAIT.*.toml` | Per-trait definitions.          | `TRAITS.md`             |

## Versioning

The number in each schema's filename is the AR contract MAJOR version.
A new MAJOR version produces a new file (e.g., `bundle-2.json`); the
prior file remains in the repo until the deprecation cycle completes.

## Status

The schemas are part of the end-of-2026 finalization target. Drafts will
land here as the corresponding spec documents move from draft to
finalized.
