# Authoring Guidance

This page gives lightweight guidance for writing Accountable Record artifacts.

For the shared annotation standard, see:

<https://github.com/structural-explainability/.github/blob/main/ANNOTATIONS.md>

## Annotation prefixes

AR artifacts may use the shared annotation prefixes when a choice needs durable
explanation.

| Prefix | Use |
| --- | --- |
| `WHY:` | Rationale for a design choice. |
| `OBS:` | Observation about the current artifact. |
| `REQ:` | Requirement imposed downstream. |
| `ALT:` | Alternative considered and rejected. |
| `CUSTOM:` | Profile- or implementation-specific note. |

Annotations are optional.

Use them when they preserve information a future reader, implementor, reviewer,
or verifier maintainer will need.

Do not use annotations to restate obvious text.

## Where annotations appear

Annotations may appear in:

- specification prose,
- TOML or JSON rationale fields,
- examples and fixtures,
- implementation comments,
- profile-specific documentation.

For prose, use short set-aside blocks:

```markdown
> **WHY:** A record has one entity kind so trait applicability and
> transformation behavior remain unambiguous.
```

For TOML, use rationale fields when the explanation belongs with the artifact:

```toml
[trait."AR.TRAIT.SOURCE_TRACEABLE".rationale]
why = """
Source traceability lets a verifier distinguish the source record from later
interpretation or derived claims.
"""
```

## When to annotate

Add an annotation when:

- the reason for a choice is not obvious,
- an alternative was considered and rejected,
- an artifact imposes a downstream requirement,
- a profile needs to record domain-specific context,
- removing the explanation would make future maintenance riskier.

Do not annotate when the annotation merely repeats the surrounding text.

## Normative status

Annotations are non-normative.

They explain artifacts.

They do not replace the specification, schema, claim definition, trait
definition, profile, bundle, or report.

Changing annotation text is not a breaking change unless the normative artifact
itself changes.

## Profile-specific notes

Use `CUSTOM:` only for information specific to a profile or implementation.

Do not use `CUSTOM:` as a substitute for `WHY:` when explaining an AR-level
design choice.
