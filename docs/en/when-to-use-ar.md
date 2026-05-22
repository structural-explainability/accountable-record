# When to Use AR

Use Accountable Record when a system needs records that remain inspectable,
contestable, auditable, correctable, and reusable under persistent
disagreement.

AR is not a workflow platform.

AR is not a replacement for ordinary schema validation.

AR is a contract for exported accountable records, profiles, verification
reports, mappings, and conformance semantics.

Authoritative adoption source data lives in:

```text
data/adoption/
```

Scope and boundary source data lives in:

```text
data/governance/
```

## Central question

> Does this system need records that remain inspectable, contestable,
> auditable, correctable, and reusable even when people disagree about what the
> records mean?

If yes, AR may apply.

If no, AR may be more structure than the system needs.

## Good fit signals

AR is likely to be useful when one or more of these conditions apply.

| Signal                  | Meaning                                                                                                                                               |
| ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| Persistent Disagreement | Records may be questioned later by parties who disagree about meaning, source, scope, authority, status, classification, evidence, or interpretation. |
| Inspectable Exports     | The system needs exported records that can be inspected independently of the producing application.                                                   |
| Source Traceability     | Readers need to inspect records against source material, citations, files, observations, or provenance.                                               |
| Cross-System Mapping    | The system needs to map local, domain, institutional, or external vocabulary into durable accountable structure.                                      |
| Verification Reporting  | The system needs reports showing what was checked, what passed, what failed, what was partial, what could not be verified, and what was not run.      |
| Record Evolution        | The system needs to preserve corrections, transformations, reinterpretations, successor relations, or status changes over time.                       |

## Poor fit signals

AR may be unnecessary when one or more of these conditions apply.

| Signal                               | Meaning                                                                                                                                   |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------- |
| Ordinary Schema Validation Is Enough | The system only needs to check shape and required fields, without preserving disagreement, mapping, verification, or conformance context. |
| Single Short-Lived Authority         | The records are short-lived and controlled by one trusted authority with no durable contestation burden.                                  |
| Workflow Platform Needed             | The team primarily needs forms, approvals, dashboards, APIs, authorization, or case management rather than export accountability.         |
| No Independent Inspection Needed     | No one needs to inspect exported records outside the producing system.                                                                    |

## Readiness questions

A team considering AR should ask:

- Will these records be questioned later by people or systems that may disagree?
- Does a reader need to inspect records against sources, citations, provenance,
  or evidence?
- Do content, status, interpretation, source, scope, or provenance need to
  remain separable?
- Does the system need to export records for review outside the original
  application?
- Would a verifier report showing `pass`, `fail`, `partial`,
  `cannot-verify`, and not-run information be useful?
- Does the system need a path that starts with bundle shape and grows toward
  stronger conformance?

Mostly yes answers suggest AR is worth considering.

Mostly no answers suggest ordinary schema validation, documentation, or local
export conventions may be enough.

Mixed answers suggest a limited AR maturity target may be appropriate.

## Incremental adoption

AR can be adopted incrementally.

A system does not need full profile conformance on day one.

| Level   | Name                              | Primary value                                                                                                 |
| ------- | --------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| Level 0 | Bundle Shape                      | The system can produce a recognizable artifact for inspection.                                                |
| Level 1 | Source Traceability               | Readers can inspect records against source material and understand how records came to be.                    |
| Level 2 | Subject Structure                 | Readers can understand what records are about without requiring AR to own a universal ontology.               |
| Level 3 | Trait Declarations                | Record types make explicit structural commitments that verifiers can check.                                   |
| Level 4 | Transformation-Aware Verification | Corrections, changes, successors, and no-identity-question operations become inspectable.                     |
| Level 5 | Domain Profile Conformance        | The bundle satisfies profile-specific claims, traits, mappings, evidence requirements, and conformance rules. |

Later levels extend earlier levels.

They do not replace them.

A system may target a lower maturity level without being penalized for not
satisfying higher-level claims.

## Typical use cases

AR may be useful for:

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

## Mapping instead of replacement

AR is designed to work with existing standards and local vocabularies.

A system can keep its own vocabulary and map it into AR subject structure,
field roles, traits, claims, profiles, and packages.

This makes AR an accountability layer rather than a demand to abandon existing
standards.

## What AR gives adopters

AR gives adopters a way to publish records that can answer questions such as:

- What was exported?
- What is the record about?
- What source does it rely on?
- What profile or package defines the expected structure?
- What claims were checked?
- What passed?
- What failed?
- What was partial?
- What could not be verified?
- What was not run?
- What changed over time?
- What remains open to disagreement?

## Boundary

AR should be used when the cost of losing inspectable record structure is
greater than the cost of maintaining that structure.

For systems where ordinary schema validation is enough, AR may be too much.

For systems that must remain accountable under persistent disagreement, AR
provides durable structure, incremental adoption, and machine-readable
verification.
