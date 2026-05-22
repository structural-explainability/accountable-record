# Packages

Element packages are versioned distribution units for Accountable Record
verifiable elements and their supporting artifacts.

Authoritative package source data lives in:

```text
data/packages/
```

Package rules live in:

```text
data/contracts/package-contract.toml
```

Change rules live in:

```text
data/contracts/change-contract.toml
```

## Purpose

Packages make AR composable.

A profile can depend on AR core packages, domain packages, local institutional
packages, or proprietary packages without copying the whole contract.

Packages let independently published systems share accountable-record structure
while preserving stable element identity.

## Core distinction

AR separates three concepts:

| Concept | Role |
| --- | --- |
| Component group | Organizes related verifiable element types. |
| Verifiable element | Defines an independently checkable AR building block. |
| Element package | Distributes one or more element types with supporting artifacts. |

Element identity is package-independent.

A package may include an element, but the package does not own the element's
identity.

## What packages contain

A package may include or reference:

- element types;
- schemas;
- checks;
- examples;
- mappings;
- subject mappings;
- compatibility fixtures;
- expected reports;
- verifier expectations;
- dependency declarations;
- rationale;
- generated canonical exports;
- lock metadata.

The exact package contract is defined in source data, not repeated here.

## Package identity and element identity

Package identity and element identity are distinct.

A package is a versioned distribution unit.

A verifiable element is a stable contract unit.

An element identifier does not include the package name or package version. This
allows packages to reorganize, split, merge, or specialize without renaming the
elements they distribute.

## Packages and profiles

Profiles select packages or selected element types.

A profile may use packages to declare:

- selected structure;
- mandatory claims;
- required traits;
- field mappings;
- subject mappings;
- verifier expectations;
- compatibility fixtures;
- expected reports.

Profiles should compose packages rather than copy their definitions.

## Resolution, locks, and digests

Authoring may use version ranges.

Validation uses a resolved lock file with exact versions and digests.

Digests are computed from canonical generated JSON, not authored TOML.

This means non-semantic TOML edits, such as comments or formatting, do not
change package identity.

See the package contract and change contract for the authoritative rules.

## Core, domain, and proprietary packages

AR core packages define reusable structure expected across many profiles.

Domain packages define profile-specific structure, such as judicial-record or
civic-record elements, claims, traits, mappings, fixtures, and expected reports.

Proprietary packages may define private structure while still using AR package,
identity, lock, digest, and verification semantics.

A package does not have to be public to be structurally compatible. A verifier
can validate it if the resolved artifacts and lock metadata are available.

## Generated exports

Authored package source lives under:

```text
data/packages/
```

Generated package exports may be written under:

```text
data/export/
```

The generated JSON export is the canonical interchange artifact.

The authored TOML remains the maintainer-facing source.

## Boundary

Packages distribute accountable-record structure.

They do not decide truth, authority, legitimacy, legal effect, obligation
enforcement, or final domain meaning.
