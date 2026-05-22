# Subjects

A record subject is what an Accountable Record is about.

AR uses subject-oriented structure without requiring every adopter to use the
same domain ontology. Profiles may use their own subject vocabularies,
identity-regime vocabularies, institutional classifications, or external
standards, but those vocabularies are mapped into AR subject structure rather
than made canonical AR vocabulary.

Authoritative subject element types live in:

````text
data/elements/subjects/
````

Subject mapping guides live in:

````text
data/subject-mappings/
````

## Core subject concepts

| Concept | Meaning |
| --- | --- |
| Record Subject | The thing, event, decision, action, condition, artifact, or referent that a record is about. |
| Subject Kind | A declared kind or category for a record subject. |
| Subject Scope | The context or boundary in which a subject is considered. |
| Subject Classification | A classification assigned to a record subject by a profile, vocabulary, mapping guide, or verifier. |
| Subject Kind Declaration | A declaration that a subject kind is being used under a specified vocabulary or mapping context. |
| Subject Kind Mapping | A machine-readable mapping from a profile, domain, institutional, or external vocabulary into AR subject structure. |
| Record Type Subject Binding | A declaration that binds a profile-defined record type to the subject structure expected for records of that type. |

## AR does not own a universal ontology

AR owns subject structure.

AR does not own every domain ontology, identity vocabulary, institutional
classification, or profile-specific subject system.

This means a profile may declare that its record types use a specific external
or domain vocabulary, but the vocabulary remains owned by its publishing
authority.

AR preserves the mapping.

It does not make the external vocabulary universal.

## Record subjects and record types

A profile defines record types.

A record type may declare the subject structure expected for records of that
type.

Example:

````toml
[record_type.holding_record]
subject_kind = "normative-content-subject"
subject_mapping = "accountable-entities"
external_subject_kind = "AE.NOR_C"
````

This says that `holding_record` is a profile-defined record type whose subject
is mapped through the accountable-entities subject mapping guide.

The external identifier remains external. The AR structure records the mapping.

## One record, one primary subject structure

A record should have a clear primary subject structure.

If one domain artifact needs to describe multiple subject structures, the
profile should normally decompose it into multiple records with explicit
relations between them.

This keeps subjects, claims, traits, sources, and transformations inspectable.

## Subject kinds and traits

Subject kinds may help determine which traits a profile declares for a record
type.

For example, a profile may map a record type to a normative-content subject and
then declare traits related to source traceability, content/status separation,
or authority non-assertion.

AR does not infer every trait from the subject kind automatically. The profile
declares the commitments it intends to make.

## Subject kinds and transformations

Subject mappings may also help a profile describe which transformations are
valid for a record type.

Transformation behavior is profile- and mapping-sensitive. AR preserves the
declared subject structure, transformation declarations, and verification
results so the behavior can be inspected.

## Subject kinds and failure modes

Subject mappings can help detect structural collapses.

For example, a profile may distinguish source material from interpretation,
content from status, or an instrument from the role it occupies. If a record
collapses those structures, a verifier may report the relevant failure through
claims, findings, evidence, or conformance results.

## Profile responsibilities

A profile that uses subject kinds should:

- declare the vocabulary or mapping guide being used;
- bind record types to subject structure;
- use citable identifiers for external subject vocabularies;
- avoid redefining external identifiers;
- avoid making an external vocabulary canonical for AR;
- provide field mappings when subject-related checks require local fields.

Profiles may use a subset of an external vocabulary.

Profiles may also define their own subject vocabulary.

## Boundary

AR subject structure answers:

> What is this record about, and how is that subject classification declared or
> mapped?

AR does not decide:

- truth;
- authority;
- legitimacy;
- legal effect;
- institutional approval;
- final domain meaning;
- whether one domain ontology is universally correct.
