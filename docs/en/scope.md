# Scope

Accountable Record is a language-neutral contract for information systems that
must remain usable under persistent disagreement.

AR defines record structure requirements, exported artifact types,
verification artifacts, and conformance semantics.

AR does not define domain truth, domain authority, domain correctness, legal
effect, institutional legitimacy, obligation enforcement, or operational
deployment.

Authoritative scope source data lives in:

```text
data/governance/scope.toml
```

Governance boundaries live in:

```text
data/governance/boundaries.toml
data/governance/non-goals.toml
```

## Purpose

AR exists to preserve the record structure needed for:

- inspection;
- contestation;
- audit;
- correction;
- reinterpretation;
- comparison;
- reuse over time.

AR is useful when records may be questioned later and the system must preserve
what was recorded, where it came from, what it refers to, how it changed, and
what interpretation was added.

## Systems

AR applies to information systems where disagreement may persist.

Examples include systems that handle:

- legal records;
- civic and institutional records;
- scientific or technical records;
- energy and infrastructure records;
- procurement and contract records;
- public data records;
- standards and compliance records;
- audit or oversight records.

The domain does not determine whether AR applies.

The need for durable record structure under disagreement determines whether AR
applies.

## Problems addressed

AR addresses structural problems such as:

- collapsing a source into an interpretation;
- collapsing a name into an identity;
- collapsing content into current status;
- collapsing an event into a record about the event;
- collapsing provenance into authority;
- collapsing scope into meaning;
- mutating prior records instead of preserving transformations;
- losing the distinction between domain vocabulary and structural role.

AR does not eliminate these problems automatically.

It defines artifacts, structures, mappings, and checks that make them visible.

## Contract artifacts

AR defines three exported artifact types:

| Artifact | Purpose |
| --- | --- |
| Bundle | What a system exports for inspection. |
| Profile | What defines a profile-level claim set, mappings, and conformance expectations. |
| Report | What a verifier emits after checking a bundle. |

AR also defines supporting contract structures for:

- subjects;
- subject mappings;
- traits;
- claims;
- transformation behaviors;
- maturity levels;
- outcome semantics;
- field mappings;
- failure modes;
- element packages.

## Subjects and mappings

AR owns subject structure.

AR does not own a universal domain ontology.

Profiles may use local, domain, institutional, or external vocabularies and map
them into AR subject structure.

The mapping is explicit, machine-readable, and citable.

## Traits and claims

A trait is a structural commitment.

A claim is a verifier check.

Together, traits and claims make conformance inspectable.

Profiles may declare traits, adopt AR claims, define profile claims, and bind
local fields to AR structural roles through field mappings.

## Maturity levels

AR conformance is incremental.

A system may begin with bundle shape and later add source traceability, subject
structure, trait declarations, transformation-aware verification, and
domain-profile conformance.

Later levels extend earlier levels.

They do not replace them.

## Verification

AR defines how verifiers produce reports.

A verifier checks applicable claims and emits outcomes from the closed outcome
vocabulary:

- `pass`
- `fail`
- `partial`
- `cannot-verify`

Claims that are not run do not receive outcomes.

They may appear as not-run metadata.

## Standards integration

AR is designed to work with existing standards.

AR may be mapped to or used alongside:

- JSON Schema;
- RDF;
- OWL;
- SHACL;
- PROV-O;
- DCAT;
- legal citation standards;
- archival standards;
- domain-specific schemas and ontologies.

AR does not replace those standards.

It provides an accountability-oriented export, mapping, verification, and
conformance layer.

## Out of scope

AR does not define:

- domain truth;
- domain correctness;
- legal authority;
- institutional legitimacy;
- obligation enforcement;
- causal explanation;
- epistemic evaluation;
- analytics;
- optimization;
- recommendation;
- database design;
- APIs;
- authentication;
- authorization;
- access control;
- cryptographic attestation;
- operational deployment.

These capabilities may be provided by operational systems, domain profiles, or
external layers.

They are not required by the AR contract.

## Boundary rule

AR should be used when record structure must survive disagreement.

AR may be unnecessary when ordinary schema validation is enough.

The central question is:

> Does this system need records that remain inspectable, contestable,
> auditable, correctable, and reusable even when people disagree about what the
> records mean?

If yes, AR may apply.

If no, AR may be more structure than the system needs.
