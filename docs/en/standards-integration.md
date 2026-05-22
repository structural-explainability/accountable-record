# Standards Integration

AR is designed to work with existing standards.

It does not replace domain standards, ontologies, schemas, citation systems,
recordkeeping systems, or institutional vocabularies.

Governance source data lives in:

```text
data/governance/
```

Mapping source data lives in:

```text
data/mappings/
data/subject-mappings/
```

## Purpose

Many systems already use standards.

AR provides an accountability-oriented layer for exported records, profiles,
reports, mappings, verification semantics, and package composition.

## Examples

AR may be mapped to or used alongside:

- JSON Schema;
- RDF;
- OWL;
- SHACL;
- PROV-O;
- DCAT;
- legal citation standards;
- archival standards;
- domain-specific schemas and ontologies.

## Mapping Instead of Replacement

A profile may keep a domain standard as its operational vocabulary while mapping
selected structures into AR roles.

This lets AR check accountable-record structure without claiming ownership of
the domain vocabulary.

## Boundary

AR integration does not make an external standard canonical for AR.

It records how a profile uses or maps that standard for accountable-record
purposes.
