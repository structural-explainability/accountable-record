# Accountable Record

Accountable Record (AR) is a language-neutral, data-first contract for
information systems whose records must remain inspectable, contestable,
auditable, correctable, and reusable under persistent disagreement.

AR specifies exported bundles, profiles, reports, conformance semantics,
subject mappings, traits, claims, transformations, failure modes, and package
contracts.

## Start here

- [Scope](./scope.md) - what AR covers and where its boundary is
- [When to Use AR](./when-to-use-ar.md) - fit signals, readiness questions, and incremental adoption
- [Non-Goals](./non-goals.md) - what AR intentionally does not decide or provide
- [Vocabulary](./vocabulary.md) - how AR terms are defined and governed

## Core model

- [Subjects](./subjects.md) - record subjects, subject kinds, and subject structure
- [Subject Mappings](./subject-mappings.md) - mapping external or domain vocabularies into
  AR subject structure
- [Component Groups](./component-groups.md) - organization of related verifiable element types
- [Verifiable Elements](./verifiable-elements.md) - independently checkable AR building blocks
- [Traits](./traits.md) - structural commitments made by record types and profiles
- [Claims](./claims.md) - checkable requirements used by verifiers

## Conformance and verification

- [Conformance](./conformance.md) - outcomes, claim selection, achieved levels, and report semantics
- [Verification](./verification.md) - verifier contracts, evidence semantics, aggregation, and identity
- [Exports](./exports.md) - bundle, profile, report, schema, extension, and operation boundaries
- [Transformations](./transformations.md) - declared changes and their effect on subject identity
- [Failure Modes](./failure-modes.md) - structural collapses AR is designed to detect and resist

## Contracts and packages

- [Contracts](./contracts.md) - identity, package, and change contracts
- [Identity Contract](./identity-contract.md) - authority-based, version-free identifier rules
- [Package Contract](./package-contract.md) - package composition, resolution, locks, and digests
- [Change Contract](./change-contract.md) - additive, breaking, deprecated, superseded, and
  withdrawn changes
- [Packages](./packages.md) - reusable element packages and package views

## Implementation and operations

- Commands- CLI commands for checking, exporting, rendering, and scaffolding
- Configuration - project and tool configuration
- Examples - example bundles, profiles, reports, and fixtures
