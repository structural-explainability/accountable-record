# Change Contract

The change contract defines how Accountable Record source artifacts may evolve
without breaking downstream profiles, packages, verifiers, or generated exports.

Authoritative source data lives in:

```text
data/contracts/change-contract.toml
```

## Purpose

AR is designed for long-lived records and independently published packages.
That means changes must be classified explicitly.

A change may be:

- additive;
- compatible;
- breaking;
- deprecated;
- superseded;
- withdrawn.

The change contract defines how these categories affect package versions,
element identity, lock files, generated exports, and downstream compatibility.

## Boundary

This page explains the model.

The TOML source defines the contract.
