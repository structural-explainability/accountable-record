# Identity Contract

The identity contract defines stable identifier rules for Accountable Record
artifacts.

Authoritative source data lives in:

```text
data/contracts/identity-contract.toml
```

## Purpose

AR identifiers are designed to remain stable across packaging, versioning,
profile selection, and generated exports.

A verifiable element is identified by:

- namespace authority;
- project space;
- component group;
- local element name.

Element identity is package-independent.

## Version-free Identity

Versions do not belong in stable element identifiers.

Versions belong in package releases, resolved dependency graphs, lock files,
and generated export metadata.

This keeps element identity stable even when packages are reorganized.

## Boundary

This page summarizes the model.

The identity contract TOML source is authoritative.
