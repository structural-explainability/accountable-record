# Vocabulary

AR vocabulary terms are defined as machine-readable source data.

Authoritative vocabulary source data lives in:

````text
data/vocabulary/terms.toml
````

This page explains how vocabulary is used. It does not duplicate the full term
list.

## Purpose

The vocabulary gives AR terms stable identifiers, labels, definitions,
plain-language explanations, aliases, deprecated aliases, and relationships to
other terms.

Vocabulary terms help:

- keep generated documentation consistent;
- support profile and package authors;
- preserve preferred names and deprecated names;
- make mappings readable by humans and machines;
- prevent terminology drift across implementations.

## Source of truth

The source of truth is:

````text
data/vocabulary/terms.toml
````

Generated docs, schemas, validators, and package metadata should consume that
file rather than maintaining separate vocabulary copies.

If this page and the TOML source disagree, the TOML source governs.

## Term identifiers

Each vocabulary term has a stable `id`.

A term ID is a lowercase, hyphenated identifier such as:

````text
verifiable-element
subject-kind
claim-outcome
element-package
````

The ID is used by tooling and generated documentation.

The label is used for human-readable display.

## Definitions and plain language

Vocabulary entries may include both:

- `definition`
- `plain_language`

The definition is the contract-oriented explanation.

The plain-language field is a reader-friendly explanation for docs, reports,
chooser tools, and onboarding materials.

## Aliases and deprecated aliases

A term may include aliases.

Aliases help readers and tools recognize alternate wording.

Deprecated aliases are retained for migration and searchability, but they are
not preferred terms.

New AR source data should use the preferred term ID.

## Related terms

Related terms identify vocabulary connections without creating formal
dependency rules.

For example, `verifiable-element`, `element-package`, and `component-group`
are related, but each names a distinct concept.

## Vocabulary is not ontology

The AR vocabulary defines the language used by the AR contract.

It does not define a universal domain ontology.

Domain profiles, external standards, institutional vocabularies, and
subject-mapping guides may define their own terms and map them into AR
structure.

## Updating vocabulary

Vocabulary changes should preserve existing term IDs whenever possible.

Renaming or repurposing a released term ID is a breaking change.

When terminology changes, prefer:

- retaining the old term as a deprecated alias;
- adding a new preferred term when the meaning has changed;
- documenting the relationship between old and new terms;
- updating generated docs from the TOML source.

## Generated vocabulary references

Generated documentation may render vocabulary tables from:

````text
data/vocabulary/terms.toml
````

This page intentionally does not include that generated table.

It explains the vocabulary model so the term list can remain data-driven.
