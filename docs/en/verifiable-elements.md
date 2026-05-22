# Verifiable Elements

A verifiable element is an independently identifiable part of the Accountable
Record contract that can be claimed about, sourced, related, verified,
exported, and reviewed.

Authoritative source data lives in:

```text
data/elements/
```

Component group source data lives in:

```text
data/component-groups/
```

## Purpose

Verifiable elements are the core building blocks of AR.

They let the contract be modular without losing identity, traceability, or
verification structure.

## Element Identity

Each element has stable identity metadata, including:

- canonical URI;
- persistent ID;
- compact ID;
- local name;
- label.

Element identity is independent of package identity.

## Elements and Packages

Packages distribute elements.

Packages do not own the stable identity of the elements they distribute.

## Boundary

A verifiable element defines accountable-record structure.

It does not decide final domain truth, authority, legitimacy, or meaning.
