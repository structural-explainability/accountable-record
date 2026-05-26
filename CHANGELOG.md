# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.2.0] - 2026-05-25

Second public working-draft release of the Accountable Record contract.

This release strengthens the repository's validation architecture and prepares
the codebase for a clearer staged source-to-artifact pipeline. It keeps the
contract source and generated artifact workflow intact while moving check
execution onto the shared `se-contract-kit` validation model.

### Validation Architecture

- Migrates Accountable Record checks from the legacy local check-engine shape
  to the `se-contract-kit` validation model.
- Converts AR-specific checks to kit-compatible `Check` records.
- Updates AR checks to operate against resolved contract context rather than
  directly against repository paths.
- Adds an Accountable Record check registry that extends the kit's default
  validation registry with AR-specific domain checks.
- Keeps check execution owned by `se-contract-kit` while AR owns its ordered
  domain-specific check set.
- Preserves AR's stricter release hygiene policy through AR-owned strict checks,
  including release-sensitive TODO handling.

### Package Organization

- Moves operational implementation layers under `src/accountable_record/ops/`.
- Groups behind-the-scenes implementation work into:
  - `ops/checks/`,
  - `ops/exporters/`,
  - `ops/generators/`,
  - `ops/resolvers/`,
  - `ops/validators/`.
- Keeps command modules focused on CLI dispatch and command adaptation.
- Keeps `ops/__init__.py` intentionally quiet so concrete operation imports
  remain explicit and searchable.

### CLI and Source Checks

- Updates `accountable-record check` to use the kit-style validation report.
- Reports failures using check ids, optional artifact ids, failure messages,
  result counts, and overall status.
- Keeps `validate-source` as an alias for `check`.
- Keeps generation commands available for:
  - `export`,
  - `validate-generated`,
  - `build-catalog`,
  - `resolve-packages`,
  - `write-lock`,
  - `verify-lock`,
  - `digest`,
  - `render-docs`.

### Tests and Type Checking

- Updates check-engine tests to match the new kit-compatible check API.
- Replaces legacy `(root: Path) -> list[str]` test assumptions with
  `ResolutionContext` and `CheckResult`-based validation.
- Confirms the current test suite passes with 38 tests.
- Confirms `pyright` passes with zero errors.

---

## [0.1.0] - 2026-05-22

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
- Provides implemented package areas for:
  - checks,
  - commands,
  - exporters,
  - generators,
  - resolvers,
  - validators.
- Provides scaffold tooling for initial repository construction.
- Provides a real check engine validating the `data/` and `docs/en/` layout.
- Wires `accountable-record` CLI to the contract-check engine:
  - `check` validates authored source artifacts.
  - `check --strict` validates authored source artifacts plus strict repository
    hygiene checks.
  - `validate-source` is available as an alias for `check`.
- Implements the generated artifact chain:
  - `export` converts authored TOML source artifacts to canonical JSON exports.
  - `validate-generated` regenerates canonical JSON in memory and compares it
    against committed generated output.
  - `build-catalog` generates the flat element catalog.
  - `resolve-packages` resolves package composition to a unique element graph.
  - `write-lock` writes the resolved package and element lock with canonical
    JSON digests.
  - `verify-lock` verifies the committed lock against a fresh resolution.
  - `digest` prints canonical JSON SHA-256 digests for package and element
    sources.
  - `render-docs` generates reference Markdown from contract data.
- Establishes canonical JSON serialization for stable export, digest, lock, and
  generated-output comparison behavior.
- Generates 300 canonical JSON export artifacts from authored source data.
- Generates a catalog of 142 verifiable elements.
- Resolves 3 packages to 33 unique package-included elements.
- Provides generated reference documentation under `docs/en/reference/`.
- Provides tests for:
  - conformance outcome semantics,
  - data source coverage,
  - export metadata,
  - namespace and identifier discipline,
  - generated artifact validation,
  - package resolution,
  - catalog generation,
  - lock generation and verification,
  - CLI dispatch,
  - package import behavior.
- Current release validation passes with 63 tests.

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
1.3. `SE_MANIFEST.toml` - update contract_version

### Task 2. Validate

```shell
uv sync --extra dev --extra docs --upgrade
git add -A
uvx pre-commit run --all-files

# validate authored source artifacts
uv run accountable-record check --strict

# generate derived artifacts
uv run accountable-record export
uv run accountable-record build-catalog
uv run accountable-record resolve-packages
uv run accountable-record write-lock
uv run accountable-record digest
uv run accountable-record render-docs

# validate generated artifacts and lock
uv run accountable-record validate-generated
uv run accountable-record verify-lock

# do chores
uv run python -m pytest
uv run python -m pyright
uvx pre-commit run --all-files
uv run python -m zensical build
```

### Task 3. Commit, tag, push

```shell
git add -A
git commit -m "Prepare X.Y.Z"
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

[Unreleased]: https://github.com/structural-explainability/accountable-record/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/structural-explainability/accountable-record/releases/tag/v0.2.0
[0.1.0]: https://github.com/structural-explainability/accountable-record/releases/tag/v0.1.0

<!-- markdownlint-enable MD024 -->
