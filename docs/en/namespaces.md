# Namespaces and Identifiers

Accountable Records uses authority-based identifiers.

A namespace authority owns stable names within a project space. A project space
may be a public project, private project, repository, package, standard,
product, or domain-specific system.

A verifiable element type has:

- a canonical URI
- an optional persistent ID
- a compact ID
- a local name
- a version

## Canonical URI

Canonical URIs are preferred for public identifiers.

```text
https://<authority>/<project>/elements/<component-group>/<element-type>
```

Example:

```text
https://structural-explainability.org/accountable-record/elements/claims/claim
```

## Persistent ID

Persistent IDs may be used for archival, proprietary, private, or non-web
contexts.

```text
urn:ar:<authority-alias>:<project>:<component-group>:<element-type>
```

Example:

```text
urn:ar:se:accountable-record:claims:claim
```

## Compact ID

Compact IDs are human-readable and tool-friendly.

```text
<authority-alias>.<project>.<component-group>.<element-type>
```

Example:

```text
se.accountable-record.claims.claim
```

Authority aliases are registry-scoped. A catalog must resolve each alias
through the namespace authority registry.

## Versions

Canonical identity does not include version.

A versioned reference appends a version to the compact ID:

```text
se.accountable-record.claims.claim@0.1.0
```

Published identifiers must not be renamed, repurposed, or silently reused. A
breaking change requires a new major version or a replacement identifier.
Deprecated identifiers remain citable and must point to their successors when
successors exist.

## Hosting

Hosting location is metadata, not identity.

A project may be hosted on GitHub, GitLab, an institutional repository, a
private registry, or another system without changing canonical identity.
