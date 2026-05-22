# Contracts

AR uses explicit contracts for the parts of the system that must remain stable
across repositories, profiles, packages, verifiers, and generated exports.

Authoritative contract source data lives in:

```text
data/contracts/
```

## Core contracts

| Contract          | Purpose                                                                                |
| ----------------- | -------------------------------------------------------------------------------------- |
| Identity Contract | Defines stable, authority-based, version-free identifiers.                             |
| Package Contract  | Defines package composition, dependency resolution, locks, and digests.                |
| Change Contract   | Defines additive, compatible, breaking, deprecated, superseded, and withdrawn changes. |

## Why contracts are separate

These contracts are load-bearing.

They determine whether downstream systems can safely cite, package, resolve,
verify, and evolve AR artifacts over time.

## Boundary

This page orients readers.

The TOML files under `data/contracts/` are authoritative.
