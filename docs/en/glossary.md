# Glossary

AR vocabulary is data-driven.

Authoritative vocabulary source data lives in:

```text
data/vocabulary/terms.toml
```

## Purpose

This page explains where glossary terms come from.

It does not duplicate the full vocabulary list.

Generated documentation may render glossary tables from the vocabulary source.

## Source of Truth

The vocabulary source defines:

- term IDs;
- labels;
- definitions;
- plain-language explanations;
- aliases;
- deprecated aliases;
- related terms.

If this page and `data/vocabulary/terms.toml` disagree, the TOML source governs.

## Preferred Terms

Use preferred AR term IDs in source data.

Deprecated aliases may be retained for migration and searchability, but new
source data should use the preferred term.

## Boundary

The AR glossary defines AR contract language.

It does not define a universal domain ontology.
