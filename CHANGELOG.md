# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.1.0] - 2026-05-19

### Added

### Added

- Established `accountable-record` as the language-neutral Accountable
  Record contract repository.
- Added boundary documents for scope, non-goals, when to use AR, architectural
  decisions, and annotation guidance.
- Defined the current AR contract model:
  - bundles,
  - profiles,
  - reports,
  - claims,
  - traits,
  - adoption levels,
  - transformation behavior,
  - verifier reports.
- Added `DECISIONS.md` with the initial durable architecture decisions:
  - AR uses canonical upstream `AE.*` entity-kind identifiers.
  - Applicable claims have exactly four outcomes: `pass`, `fail`, `partial`,
    and `cannot-verify`.
  - AR core claims use declarative claim shapes.
  - AR owns `AR.CLAIM.*`, `AR.TRAIT.*`, `AR.TRANSFORM.*`, and
    `AR.PROFILE.*`, but references upstream `AE.*` kinds.
  - AR conformance is incremental.
  - AR exports bundles, profiles, and reports.
- Added `ENTITY_KINDS.md` and local entity-kind metadata mapping AR-facing
  labels to upstream `AE.*` identifiers.
- Added `TRAITS.md` describing the AR trait model and current AR-facing trait
  vocabulary.
- Added `CLAIMS.md` describing claim shapes, claim selection, and the current
  AR core claim set.
- Added `ADOPTION_LEVELS.md` defining incremental Level 0 through Level 5
  adoption.
- Added `EXPORT_CONTRACT.md` defining bundle, profile, and report export
  boundaries.
- Added `VERIFICATION_MODEL.md` defining verifier behavior, claim selection,
  evidence, aggregation, achieved level, and verifier-level errors.
- Added `TRANSFORMATION_MODEL.md` defining AR transformation behavior:
  identity-preserving, identity-breaking, identity-inheriting, and
  no-identity-question.
- Added `FAILURE_MODES.md` describing common structural collapses AR is designed
  to surface.
- Added JSON Schema placeholders / working schemas for:
  - `schemas/bundle-1.json`
  - `schemas/profile-1.json`
  - `schemas/report-1.json`
  - `schemas/claim-1.json`
  - `schemas/trait-1.json`
- Added lightweight Python contract-check tooling under
  `src/accountable_record/`.
- Added a single public CLI entry point:
  `accountable-record`.
- Added contract check command:
  `uv run accountable-record check --strict`.
- Added manifest synchronization command:
  `uv run accountable-record sync-manifest-version`.
- Added repository checks for required files, JSON schema parsing, TOML parsing,
  entity-kind metadata, report outcome vocabulary, forbidden legacy identifiers,
  and manifest shape.
- Added `SE_MANIFEST.toml`, `CITATION.cff`, repository metadata, release notes,
  and initial documentation structure.
- Added documentation build support with Zensical.

---

## Notes on Versioning and Releases

This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

- **MAJOR** versions indicate breaking changes.
- **MINOR** versions indicate backward-compatible additions or clarifications.
- **PATCH** versions indicate editorial fixes, documentation updates, or
  non-normative changes.

Versions are defined by git tags of the form `vX.Y.Z`.
Tagged releases are the authoritative source of version state.

Documentation and badges, where present, should reference the latest tagged
release.

## Release Procedure (Required)

Follow these steps exactly when creating a new release.

### Task 1. Update release metadata (manual edits)

1.1. `CITATION.cff` - update `version` and `date-released`
1.2. CHANGELOG.md: add section, move unreleased entries, update links

### Task 2. Sync and Validate

```shell
uv run accountable-record sync-manifest-version

# as needed
uv pip uninstall se-manifest-schema
uv cache clean se-manifest-schema

uv sync --extra dev --extra docs --upgrade

uv run accountable-record check --strict

git add -A
uvx pre-commit run --all-files
uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build
git add -A
uvx pre-commit run --all-files
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
