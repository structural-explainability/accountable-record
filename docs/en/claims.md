# Claims

A claim is a verifier check preserved within an Accountable Record contract.

Claims have stable identifiers, declared shapes, applicability rules, maturity
or profile assignments, mandatory or optional status, and machine-readable
definitions.

## Claim Shapes

AR defines these claim shapes:

| Shape | Purpose |
| --- | --- |
| `bundle_field_predicate` | Checks bundle-level fields. |
| `record_field_predicate` | Checks fields on records or record types. |
| `cross_reference_predicate` | Checks references between records or sources. |
| `trait_conformance` | Checks declared record-type and trait conformance. |
| `custom` | Reserved for domain, local, proprietary, or profile-defined check logic. |

The AR core uses the first four declarative shapes.

## Claims and Traits

Traits and claims are not the same thing.

A trait is a declarative property of a record type. A claim is a verifier check.
The trait-conformance claim checks declared record-type and trait pairs.

## Claims and Profiles

Profiles may select AR packages, domain packages, local packages, or
proprietary packages. A profile may add requirements on top of AR claim
outcomes, but it does not redefine AR claims.
