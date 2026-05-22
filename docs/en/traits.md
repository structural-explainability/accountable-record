# Traits

A trait is a declarative commitment or structural guarantee that a record type,
profile, or element package can declare.

A trait says what a record type claims to support. A claim says how a verifier
checks that guarantee.

## Source of truth

Authoritative trait element types live under:

```text
data/elements/traits/
```

The AR trait library lives in:

```text
data/traits/library.toml
```

Trait declaration semantics live in:

```text
data/traits/declarations.toml
```

## Trait declarations

Trait declarations belong to profiles, record types, or element packages.

They do not belong to individual record instances.

Records of the same record type share the same trait declarations. Per-record
trait overrides are not part of the AR contract.

A profile or record type declares traits by listing the trait identifiers it
claims to satisfy.

Example:

```toml
[[declaration_examples]]
id = "holding-record-traits"
record_type = "holding-record"
legacy_entity_kind = "AE.NOR_C"
conforms_to = [
  "se.accountable-record.traits.source-traceable",
  "se.accountable-record.traits.content-status-separated",
  "se.accountable-record.traits.authority-non-asserted",
  "se.judicial-record-us-federal-supreme.traits.holding-not-dictum",
]
```

## Traits and claims

Traits and claims are not the same thing.

A trait is a declared guarantee. A claim is a verifier check.

Trait conformance is assessed through claims, checks, field mappings, evidence,
and verifier results. The trait-conformance binding tells a verifier how to
connect a declared trait to the checks and structural roles needed to assess it.

## Field mappings

A trait check often needs to know which local fields carry which Accountable
Record structural roles.

Field mappings let domains keep their own vocabulary.

Example:

```toml
[declaration_examples.field_mappings]
source_reference = "citation"
content = "holding_text"
status = "current_status"
```

Forbidden fields are declared by the trait definition or record type
definition. They are not expressed with field-mapping sentinels.

## Partial trait conformance

Partial conformance is meaningful.

A trait-conformance result is `partial` when:

- the trait has multiple verifiable requirements;
- at least one requirement is satisfied;
- at least one requirement fails;
- the required evidence is present.

If required evidence is missing, the result is `cannot-verify`.

## Trait absence

A record type that does not declare a trait is not failing that trait.

The trait is not in scope for that record type, and the verifier does not run
trait-conformance checks for undeclared traits.

At Level 3 and above, record types must declare the traits required by the
selected AR maturity level or domain profile.

## AR trait library

The current AR trait library includes:

| Trait                         | Compact ID                                                   | Summary                                                                                        |
| ----------------------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------------------- |
| Authority Non-Asserted        | `se.accountable-record.traits.authority-non-asserted`        | Preserves the artifact, structure, source, and provenance without asserting current authority. |
| Content Status Separated      | `se.accountable-record.traits.content-status-separated`      | Keeps content separate from current status.                                                    |
| Instrument Non-Collapsing     | `se.accountable-record.traits.instrument-non-collapsing`     | Keeps an enduring instrument separate from its roles, actions, or statuses.                    |
| Interpretation Non-Mutating   | `se.accountable-record.traits.interpretation-non-mutating`   | Prevents interpretive updates from erasing or rewriting prior records.                         |
| Locus Stable                  | `se.accountable-record.traits.locus-stable`                  | Keeps place or asset identity stable across non-identity-affecting changes.                    |
| Observation Non-Authoritative | `se.accountable-record.traits.observation-non-authoritative` | Marks observed material as observation rather than authority claim.                            |
| Provenance Traceable          | `se.accountable-record.traits.provenance-traceable`          | Carries information about how the record came to be.                                           |
| Scope Declared                | `se.accountable-record.traits.scope-declared`                | Declares who, where, when, or what an obligation or rule applies to.                           |
| Source Traceable              | `se.accountable-record.traits.source-traceable`              | Preserves source references adequate for inspection against source material.                   |

## Domain traits

Profiles may define their own traits.

Domain traits compose with AR traits in the same declaration list. A domain
trait may not contradict an AR trait.

If a profile does not want to enforce an AR trait for a record type, it should
not declare that trait for that record type.

Trait declarations are commitments. They are not aspirations unless the profile
explicitly marks them as such in a separate, non-conformance field.
