# Package Contract

The package contract defines how AR element packages are composed, versioned,
resolved, locked, and verified.

Authoritative source data lives in:

```text
data/contracts/package-contract.toml
```

Package source data lives in:

```text
data/packages/
```

## Purpose

Packages allow AR, domain systems, local institutions, and proprietary systems
to compose reusable verifiable elements without copying the whole contract.

The package contract supports:

- dependency declarations;
- version ranges during authoring;
- exact versions during validation;
- lock files;
- digests;
- compatibility rules;
- one-major-version-per-identity resolution.

## Boundary

This page explains the package model.

The TOML source files define the package contract.
