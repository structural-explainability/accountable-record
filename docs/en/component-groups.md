# Component Groups

Component groups organize related verifiable element types.

Authoritative source data lives in:

```text
data/component-groups/
```

Verifiable element source data lives in:

```text
data/elements/
```

## Purpose

A component group is a structural organizing layer.

It helps readers, profiles, generators, and validators understand which
verifiable elements belong together.

Examples include groups for subjects, claims, traits, conformance,
verification, transformations, mappings, and failure modes.

## Component Groups and Elements

A component group does not replace element identity.

A verifiable element has its own identity.

A component group provides the grouping context for that element.

## Boundary

Component groups organize the contract.

They do not decide package composition, profile selection, truth, authority, or
domain meaning.
