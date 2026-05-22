# Overview

Accountable Records is a data-first specification for information systems that
must remain usable under persistent disagreement.

An Accountable Record is composed of verifiable elements: independently
identifiable parts of a record that can be claimed about, sourced, related,
verified, exported, and reviewed.

AR preserves the structure needed for disagreement to remain inspectable. It
does not decide truth, correctness, authority, legitimacy, obligation,
enforcement, or domain meaning.

## Source of truth

AR is defined by machine-readable source artifacts.

Authoritative source artifacts live under `data/`.

Human-readable documentation under `docs/en/` is generated from those source
artifacts or maintained as explanatory orientation.

The root repository files provide orientation, rationale, governance, and
workflow guidance. They do not replace the data artifacts as the source of
truth.

## Core architecture

AR separates these concepts:

| Concept | Meaning |
| --- | --- |
| Accountable Record | A structured record composed of verifiable elements. |
| Verifiable Element | An independently identifiable part of an Accountable Record that can be checked, traced, related, exported, and reviewed. |
| Element Type | A declared kind of verifiable element. |
| Element Instance | A concrete occurrence of an element type in a record. |
| Component Group | A stable architectural category that organizes related element types. |
| Element Package | A reusable distribution unit that packages related element types, schemas, checks, examples, mappings, fixtures, expected reports, dependencies, and rationale. |

## Component groups

AR organizes verifiable element types into stable component groups:

- identity
- subjects
- claims
- traits
- sources
- references
- relations
- provenance
- verification
- status
- disagreement
- conformance
- maturity
- mappings
- exports
- governance

These groups are declared in `data/component-groups/`.

## Verifiable elements

Verifiable element types are declared under `data/elements/`.

Each element type may define:

- identity metadata
- namespace authority
- component group
- definition and plain-language explanation
- schema
- checks
- examples
- compatibility requirements
- deprecation metadata
- stewardship metadata

A domain system such as JR or CIR may define its own element types while
depending on AR core element types.

## Element packages

Element packages are declared under `data/packages/`.

An element package composes related element types and supporting artifacts into
a reusable distribution unit. Packages may include schemas, checks, mappings,
fixtures, expected reports, verifier expectations, dependencies, and rationale.

Packages make it possible for profiles and downstream systems to reuse a
coherent set of AR elements without redefining their lifecycle.

## Namespaces and identifiers

AR uses authority-based identifiers.

A verifiable element type has:

- a canonical URI
- an optional persistent ID
- a compact ID
- a local name
- a version

Canonical identity is separate from hosting location. A project may be hosted
on GitHub, GitLab, a private registry, an institutional repository, or another
system without changing the element identity.

Identifier rules are declared in `data/namespace/identifier-rules.toml`.

## Maturity and adoption

AR adoption is incremental.

Systems may begin with basic exported record structure and progress toward
richer support for identifiers, verifiable elements, sources, references,
relations, provenance, verification, conformance, disagreement, mappings, and
governance.

Maturity and adoption structures are declared under `data/elements/maturity/`
and demonstrated through progressive examples under `data/records/progressive/`.

## Verification and conformance

A verifier loads the applicable bundle, profile, element packages, element
types, mappings, checks, and fixtures. It runs the selected checks and emits a
report.

Conformance artifacts include requirements, rules, checks, profiles, outcomes,
reports, and expected reports.

Verification artifacts include verification events, methods, evidence, checks,
reviews, reviewers, results, confidence, reproducibility, and verifier
expectations.

## Mappings

AR supports adoption by helping existing systems map their own terms and
fields into AR structure.

Mapping artifacts are machine-readable and human-readable. They may include
external standards, mapping guides, mapping questions, mapping answers,
candidate targets, field roles, field mappings, warnings, rules, and examples.

Mappings are declared under `data/mappings/` and `data/elements/mappings/`.

## Exports

AR exports machine-readable artifacts for downstream tools, validators, docs,
Python implementations, Rust implementations, catalogs, and external systems.

Generated exports live under `data/export/`.

Schemas live under `data/schemas/`.

Generated documentation lives under `docs/en/`.

## Boundary

AR preserves accountable record structure.

AR does not resolve disagreement.

AR does not decide truth, correctness, authority, legitimacy, obligation,
enforcement, or domain meaning.
