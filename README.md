# Accountable Record

[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)
[![Contract](https://img.shields.io/badge/contract-data--first-blue)](./data/)
[![Docs](https://img.shields.io/badge/docs-generated-blue)](./docs/en/)
[![Python Tooling](https://img.shields.io/badge/tooling-contract--checks-blue)](./pyproject.toml)

[![CI](https://github.com/structural-explainability/accountable-record/actions/workflows/ci-python-zensical.yml/badge.svg?branch=main)](https://github.com/structural-explainability/accountable-record/actions/workflows/ci-python-zensical.yml)
[![Docs-Deploy](https://github.com/structural-explainability/accountable-record/actions/workflows/deploy-zensical.yml/badge.svg?branch=main)](https://github.com/structural-explainability/accountable-record/actions/workflows/deploy-zensical.yml)
[![Links](https://github.com/structural-explainability/accountable-record/actions/workflows/links.yml/badge.svg?branch=main)](https://github.com/structural-explainability/accountable-record/actions/workflows/links.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen.svg)](https://github.com/structural-explainability/accountable-record/security)

Accountable Record (AR) is a language-neutral, data-first contract for
information systems whose records must stay inspectable, contestable,
auditable, correctable, and reusable under persistent disagreement.

AR specifies what a conforming system exports and how a verifier checks it:
bundles, profiles, reports, and conformance semantics.
It is export-first and implementation-neutral.
It requires no particular database, API, language, or runtime.

## When AR Might Be Helpful

AR is for systems where records may be questioned later and must remain usable
despite disagreement about source, scope, authority, classification, evidence,
status, interpretation, or change over time.
The domain does not decide whether AR applies;
the need for durable record structure under disagreement does.
If ordinary schema validation is enough, AR is probably more structure than the
system needs.

## What AR Does Not Do

AR preserves structure for inspection.
It does not resolve disagreement.

AR does not decide truth, domain correctness, legal authority, institutional
legitimacy, obligation, enforcement, causality, credibility, analytics,
optimization, or recommendation.

AR does not define storage, APIs, authentication, authorization, access
control, attestation, or deployment.
Those belong to profiles, implementations,
or operational systems layered around AR.

## Core Architecture

AR separates three concepts:

| Concept            | Role                                                                                                                                                                             |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Component group    | Organizes related verifiable element types.                                                                                                                                      |
| Verifiable element | An independently checkable AR building block; the unit of identity and verification.                                                                                             |
| Element package    | Distributes one or more element types with their schemas, checks, examples, mappings, fixtures, expected reports, and verifier expectations; the unit of versioned distribution. |

Profiles compose element packages or selected element types.
Element identity is package-independent;
an element can be repackaged without being renamed.

## Data-First

The durable AR contract lives under `data/`.

Pages under `docs/en/` explain and render that data;
they are not the source of truth.

A change to the contract is a change to `data/`, never to the narrative.

AR uses TOML for authored source declarations and JSON for
schemas, examples, interchange, lock files, and canonical exports.
Digests are computed over canonical generated JSON, not authored TOML,
so comments, formatting, and ordering do not change package identity.

Generated files must not be hand edited.

## Verification and Conformance

A verifier checks selected applicable claims and emits a report.

Each claim that runs receives exactly one outcome from the closed outcome
vocabulary defined in `data/conformance/outcomes.toml`.

Claims that are not selected or not applicable are recorded as `not_run`
metadata, not as outcomes.

Composite claims resolve failure-first: a determinate negative result is not
masked by missing evidence.

## Identity and Packaging

AR identifiers are authority-based and version-free.

A verifiable element is identified by namespace authority, project space,
component group, and local name.
The canonical forms are defined in
`data/contracts/identity-contract.toml`.

Authoring may use version ranges.
Validation resolves to a lock file with exact versions and digests.
A resolved graph may contain only one major version of any
package or element identity.

## Repository Layout

```text
  data/      Authoritative contract source (TOML) and generated JSON
  docs/en/   Generated and explanatory documentation
  src/       Contract tooling
  tests/     Tooling tests
  tools/     Scaffolding and maintenance scripts
```

Important distinction:

```text
data/export-contract/
  Authored TOML source defining export semantics.

data/export/
  Generated JSON export artifacts.
```

## Documentation

Documentation lives under `docs/en/`.
Good entry points include:

- `scope.md`
- `when-to-use-ar.md`
- `non-goals.md`
- `subjects.md`
- `claims.md`
- `traits.md`
- `conformance.md`
- `verification.md`
- `exports.md`
- `transformations.md`
- `failure-modes.md`

## Companion Implementations

This repository defines the language-neutral AR contract.
Verifier and tooling implementations consume it.

| Repository              | Purpose                                         |
| ----------------------- | ----------------------------------------------- |
| `accountable-record`    | Language-neutral AR contract (this repository). |
| `accountable-record-py` | Python reference implementation.                |
| `accountable-record-rs` | Rust implementation.                            |

## Command Reference

Python tooling is used to verify internal consistency and generate artifacts.

<details>
<summary>Show command reference</summary>

### In a machine terminal

Open a machine terminal where you want the project:

```shell
git clone https://github.com/structural-explainability/accountable-record

cd accountable-record
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.15
uv sync --extra dev --extra docs --upgrade
uvx pre-commit install

git add -A
uvx pre-commit run --all-files

# scaffold (only at start)
uv run python tools/scaffold_ar_repo.py

# run self-consistency checks
uv run accountable-record check --strict
uv run accountable-record validate-source --strict
uv run accountable-record verify-lock --strict

# run self-consistency checks (todo)
uv run accountable-record validate-generated
uv run accountable-record export
uv run accountable-record render-docs
uv run accountable-record build-catalog
uv run accountable-record resolve-packages
uv run accountable-record write-lock

uv run accountable-record digest

# scaffold any missing files
uv run accountable-record scaffold-missing

uv run python -m pyright
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Citation

[CITATION.cff](./CITATION.cff)

## License

[MIT](./LICENSE)

## Manifest

[MANIFEST.toml](./MANIFEST.toml)
