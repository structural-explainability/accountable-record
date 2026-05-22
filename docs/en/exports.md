# Exports

Accountable Records is concerned with what a system exports for inspection,
not with how the system stores, queries, or implements its data internally.

The core exported artifact types are:

- bundle
- profile
- report

Authoritative export contract semantics live in:

```text
data/export-contract/
```

Export-related element types live in:

```text
data/elements/exports/
```

Schemas live in:

```text
data/schemas/
```

Generated export artifacts live under:

```text
data/export/
```

## Exported artifact types

AR defines three exported verification artifact types.

| Artifact | Purpose |
| --- | --- |
| Bundle | What a conforming system exports for inspection. |
| Profile | What a domain, project, or package exports to define what should be loaded and checked. |
| Report | What a verifier exports after checking a bundle. |

Element packages are composition and distribution units. They are not a fourth
verification artifact type unless they are separately exported as package or
catalog artifacts.

## Bundle

A bundle is the artifact a conforming system exports for inspection,
validation, exchange, or review.

A bundle declares the AR envelope, bundle identity, version information,
conformance declarations, manifest, and records.

Required top-level fields are:

- `schema`
- `bundle_id`
- `versions`
- `conformance`
- `manifest`
- `records`

The `generated_at` field is recommended. A verifier may use it for report
context, but not for outcome decisions.

Each record has, at minimum:

- `id`
- `record_type`

At Level 1 and above, where applicable, records preserve source references and
provenance.

At Level 2 and above, records declare subject kind information. Earlier drafts
called this `entity_kind`; the enduring AR language prefers subject-kind
language.

## Profile

A profile defines the selected element packages, element types, claims, traits,
field mappings, transformations, verifier expectations, and conformance rules
for a verification run.

A profile may be published by:

- the AR contract repository;
- a domain record-system repository;
- a local or proprietary system;
- an external package or catalog.

Required top-level fields are:

- `schema`
- `profile_id`
- `ar_version`

Recommended top-level fields include:

- `extends`
- `element_packages`
- `record_types`
- `transformations`

Earlier drafts said profiles compose components. The enduring architecture
uses element packages and selected element types.

A profile may define:

- record types;
- traits;
- field mappings;
- transformations;
- claims;
- acceptance rules;
- verifier expectations.

A profile may not redefine AR outcome semantics, AR transformation behaviors,
AR element identity, or AR required envelope fields.

## Report

A report is the artifact a verifier emits after checking a bundle against the
selected claims, profile, element packages, maturity level, and verifier
configuration.

Required top-level fields are:

- `schema`
- `report_id`
- `verifier`
- `bundle`
- `declared_level`
- `achieved_level`
- `summary`
- `results`

Recommended top-level fields include:

- `generated_at`
- `profile`
- `element_packages`

Each result includes:

- `claim_id`
- `outcome`

A result may also include:

- `evidence`
- `sub_results`

A report is itself inspectable. It cites by identifier and does not summarize
away the evidence needed to understand the verifier's findings.

## Schemas

Schemas constrain exported shapes.

Current schema artifacts live under:

```text
data/schemas/
```

Schemas validate structure. They do not replace the TOML source artifacts that
define AR vocabulary, elements, packages, conformance semantics, verification
semantics, and export semantics.

Schema changes follow AR contract versioning. Breaking schema changes require a
major version change.

## Extensions

Profiles, domains, local systems, proprietary systems, and implementations may
add fields when extending exported artifacts.

Extensions may add structure. They may not replace the required AR envelope or
change AR semantics.

A valid extension may not:

- override or redefine required fields;
- redefine AR outcome semantics;
- redefine AR transformation behaviors;
- redefine AR element identity;
- use keys beginning with `_ar_`;
- omit required fields because they are outside a package concern.

Keys beginning with `_ar_` are reserved for AR contract use.

If a selected element package or profile requires evidence and that evidence is
absent, the corresponding claim result is `cannot-verify`.

## Operations

Verifier implementations may expose operations such as inspect, validate, and
compare.

### Inspect

Inspect reads a bundle and summarizes its declared conformance, record types,
subject kinds, traits, transformations, and related structure.

Inspection does not run claims and does not produce an AR report.

### Validate

Validate reads a bundle and profile, runs applicable claims, and emits an AR
report.

Only validation produces an AR report.

### Compare

Compare reads two bundles, profiles, or reports and produces an
implementation-defined diff.

Comparison is useful for implementations, but it is not an exported AR artifact
type.

## Boundary

AR exports define what systems publish for inspection.

They do not define:

- internal storage models;
- internal query systems;
- implementation-specific APIs;
- implementation-specific CLI surfaces;
- exit codes;
- local formatting conventions.

Implementations choose their own operational surface while preserving AR export
semantics.
