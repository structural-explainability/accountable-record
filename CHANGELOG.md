# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.1.0] - 2026-05-21

Initial public working-draft release of the Accountable Record contract.

This release establishes `accountable-record` as a language-neutral,
data-first contract repository for records that must remain inspectable,
contestable, auditable, correctable, and reusable under persistent
disagreement.

### Contract Scope

- Defines Accountable Record as an export-first contract for:
  - bundles,
  - profiles,
  - verification reports,
  - conformance semantics,
  - subject mappings,
  - traits,
  - claims,
  - transformations,
  - failure modes,
  - element packages.
- Establishes AR as implementation-neutral: no required database, API,
  programming language, runtime, authentication system, authorization model,
  or deployment architecture.
- Defines AR boundaries: AR preserves inspectable record structure but does
  not decide truth, legal authority, institutional legitimacy, obligation
  enforcement, causality, credibility, analytics, optimization, or
  recommendation.

### Data-First Source

- Establishes `data/` as the source of truth for the contract.
- Uses authored TOML for maintainable source declarations.
- Uses JSON for schemas, examples, generated interchange artifacts, lock files,
  and canonical exports.
- Reserves `data/export-contract/` for authored export semantics.
- Reserves `data/export/` for generated JSON export artifacts.
- Includes source areas for:
  - `adoption/`,
  - `catalog/`,
  - `claims/`,
  - `component-groups/`,
  - `conformance/`,
  - `contracts/`,
  - `elements/`,
  - `export-contract/`,
  - `failure-modes/`,
  - `governance/`,
  - `locks/`,
  - `mappings/`,
  - `namespace/`,
  - `packages/`,
  - `records/`,
  - `schemas/`,
  - `subject-mappings/`,
  - `traits/`,
  - `transformations/`,
  - `verification/`,
  - `vocabulary/`.

### Foundational Contracts

- Defines the identity contract:
  - authority-based identifiers,
  - project spaces,
  - canonical URIs,
  - persistent IDs,
  - compact IDs,
  - version-free identity,
  - package-independent element identity.
- Defines the package contract:
  - versioned element packages,
  - package composition,
  - dependency declarations,
  - resolution to exact versions,
  - lock-file semantics,
  - canonical generated JSON digests.
- Defines the change contract:
  - additive changes,
  - compatible changes,
  - breaking changes,
  - deprecation,
  - supersession,
  - withdrawal,
  - one major version per identity per resolved graph.

### Subjects and Mappings

- Defines AR subject structure without making AR a universal domain ontology.
- Defines subject-related verifiable elements:
  - record subject,
  - subject kind,
  - subject scope,
  - subject classification,
  - subject-kind declaration,
  - subject-kind mapping,
  - record-type subject binding.
- Provides subject mapping guides for:
  - identity regimes,
  - accountable entities.
- Treats external vocabularies as profile-selected mapping contexts, not
  canonical AR-owned ontology.

### Conformance and Verification

- Defines the closed conformance outcome vocabulary:
  - `pass`,
  - `fail`,
  - `partial`,
  - `cannot-verify`.
- Defines evidence sufficiency for each outcome.
- Defines mandatory-level blocking behavior for conformance outcomes.
- Defines composite-claim rollup with failure-first precedence:
  - `fail`,
  - `partial`,
  - `cannot-verify`,
  - `pass`.
- Defines report semantics, verifier errors, compatibility fixtures, expected
  reports, verifier contracts, evidence semantics, aggregation, and verifier
  identity source areas.

### Transformations

- Defines closed AR transformation behaviors:
  - identity-preserving,
  - identity-breaking,
  - identity-inheriting,
  - no-identity-question.
- Defines transformation declarations as bundle-level relationships between
  records.
- Defines subject-mapping-sensitive admissibility.
- Defines lineage requirements for identity-inheriting transformations.
- Defines profile responsibilities for domain-specific transformation kinds.

### Failure Modes

- Defines structural failure modes as collapses that make records harder to
  inspect, verify, transform, compare, or preserve under disagreement.
- Defines core collapse patterns:
  - source vs. interpretation,
  - name vs. identity,
  - content vs. status,
  - event vs. record,
  - provenance vs. authority,
  - context vs. claim.
- Defines detection and remediation source structures.
- Allows profiles to define additional domain-specific failure modes.

### Governance and Adoption

- Defines governance source data for:
  - scope,
  - non-goals,
  - boundaries.
- Defines adoption source data for:
  - when to use AR,
  - readiness questions,
  - maturity path.
- Defines incremental maturity levels from Level 0 through Level 5.

### Documentation

- Provides documentation under `docs/en/`.
- Includes entry points for:
  - scope,
  - when to use AR,
  - non-goals,
  - vocabulary,
  - subjects,
  - subject mappings,
  - component groups,
  - verifiable elements,
  - traits,
  - claims,
  - conformance,
  - verification,
  - exports,
  - transformations,
  - failure modes,
  - contracts,
  - packages.

### Tooling

- Provides Python package surface under `src/accountable_record/`.
- Provides the public CLI entry point `accountable-record`.
- Provides initial package areas for:
  - loaders,
  - validators,
  - checks,
  - exporters,
  - renderers,
  - generators,
  - resolvers,
  - locks,
  - catalog,
  - schemas,
  - source-area modules.
- Provides scaffold tooling for creating missing repository source files.
- Provides initial tests for:
  - conformance outcome semantics,
  - data source coverage,
  - export metadata,
  - namespace and identifier discipline,
  - package import behavior.
- Provides a real check engine validating the `data/` and `docs/en/` layout.
- Wires `accountable-record` CLI to the real contract-check engine:
  - `check` and `check --strict` validate the repository layout and pass
    against the current contract data.
  - `check` runs 15 base checks.
  - `check --strict` runs 18 checks, including strict repository hygiene checks.
  - `validate-source` is available as an alias for `check`.
  - `verify-lock` is implemented.
- Registers generation commands with explicit not-yet-implemented exits:
  - `export`,
  - `render-docs`,
  - `build-catalog`,
  - `resolve-packages`,
  - `write-lock`,
  - `digest`,
  - `validate-generated`,
  - `scaffold-missing`.
- Adds lock-file validation coverage in `tests/test_element_lock_valid.py`.
- Adds positive and negative test coverage for the check engine, check command,
  root command dispatch, and implemented check modules.

## Notes on Versioning and Releases

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- **MAJOR** versions indicate breaking changes.
- **MINOR** versions indicate backward-compatible additions or clarifications.
- **PATCH** versions indicate editorial fixes, documentation updates, or
  non-normative changes.

Versions are defined by git tags of the form `vX.Y.Z`.
Tagged releases are the authoritative source of version state.

## Release Procedure (Required)

Follow these steps exactly when creating a new release.

### Task 1. Update release metadata (manual edits)

1.1. `CITATION.cff` - update `version` and `date-released`
1.2. CHANGELOG.md: add section, move unreleased entries, update links
1.3. `MANIFEST.toml` - update contract_version

### Task 2. Validate

```shell
uv sync --extra dev --extra docs --upgrade
git add -A
uvx pre-commit run --all-files
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# run AR checks
uv run accountable-record check --strict

# generate derived artifacts as implemented
uv run accountable-record export
uv run accountable-record render-docs
```

### Task 3. Commit, tag, push

```shell
git add -A
git commit -m "Prep X.Y.Z"
git push -u origin main
```

Verify actions run on GitHub. After success:

```shell
git tag vX.Y.Z -m "X.Y.Z"
git push origin vX.Y.Z
```

### Task 4. Verify tag consistency

```shell
uv run python -m se_manifest_schema validate --strict --require-tag
```

Confirms CITATION.cff version matches the pushed git tag.
Run this after `git push origin vX.Y.Z`; it will fail before that point.

## Only As Needed (delete a tag)

```shell
git tag -d vX.Z.Y
git push origin :refs/tags/vX.Z.Y
```

## Links

[Unreleased]: https://github.com/structural-explainability/accountable-record/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/structural-explainability/accountable-record/releases/tag/v0.1.0

<!-- markdownlint-enable MD024 -->
