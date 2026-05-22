# Transformations

Transformations describe declared changes between records and what those
changes do to subject identity.

A transformation is not part of a single source or target record. Records
describe subjects. Transformations describe declared relationships between
records.

Authoritative transformation source files live in:

```text
data/transformations/
```

Transformation-related element types live in:

```text
data/elements/transformations/
```

Subject mapping source files live in:

```text
data/subject-mappings/
```

## Core concepts

| Concept                      | Meaning                                                                                                               |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Transformation               | A declared change or change-like relationship between records.                                                        |
| Transformation Kind          | The profile-defined domain name for the transformation.                                                               |
| Transformation Behavior      | The AR-defined effect of the transformation on subject identity.                                                      |
| Transformation Declaration   | A bundle-level declaration connecting source record, target record, kind, behavior, and optional evidence or lineage. |
| Transformation Admissibility | A rule saying whether a claimed behavior is possible in the declared subject and profile context.                     |
| Transformation Lineage       | A declared successor or accountability-lineage relation.                                                              |
| Transformation Evidence      | Evidence used to check a declared transformation.                                                                     |
| Transformation Profile Rule  | A profile rule constraining transformation kinds, connected record types, evidence, admissibility, or lineage.        |

## Transformation behaviors

AR defines a closed vocabulary of transformation behaviors:

| Behavior               | Meaning                                                                                                    |
| ---------------------- | ---------------------------------------------------------------------------------------------------------- |
| `identity-preserving`  | The target record preserves the same subject identity as the source record.                                |
| `identity-breaking`    | The target record represents a distinct subject identity from the source record.                           |
| `identity-inheriting`  | The target record represents a successor subject whose accountability lineage includes the source subject. |
| `no-identity-question` | The operation does not raise an identity question for the represented subject.                             |

Profiles may define domain-specific transformation kinds.

Profiles may not add AR transformation behaviors or redefine the meanings of
AR transformation behaviors.

## Transformation declarations

A transformation declaration connects records.

A declared transformation has:

- a source record ID;
- a target record ID;
- a profile-defined transformation kind;
- an AR-defined transformation behavior;
- optional evidence;
- optional lineage;
- optional profile context;
- optional subject mapping context.

Example:

```json
{
  "source_record_id": "rule-content:0001",
  "target_record_id": "rule-content:0002",
  "transformation_kind": "judicial.amendment",
  "behavior": "identity-inheriting",
  "lineage": {
    "lineage_relation": "successor"
  }
}
```

The transformation kind is domain-specific. The behavior is AR-defined.

## Behavior and subject structure

Transformation behavior is evaluated in relation to subject structure.

AR does not require a universal subject ontology. Instead, a profile declares
its record types, subject kinds, subject mappings, and transformation rules.

A claimed behavior may be admissible or inadmissible depending on:

- source record;
- target record;
- source subject kind;
- target subject kind;
- subject mapping;
- transformation kind;
- claimed behavior;
- profile context.

Admissibility is not proof that a transformation is valid. It only states
whether the claimed behavior is possible in the declared subject and profile
context.

## Default admissibility policy

If the subject mapping is unknown, the verifier cannot determine admissibility.

If the transformation kind is unknown, the verifier cannot determine
admissibility.

If required subject information is missing, the verifier cannot determine
admissibility.

If the claimed behavior is inadmissible, the relevant claim fails.

Default outcomes:

| Condition                            | Outcome         |
| ------------------------------------ | --------------- |
| Unknown subject mapping              | `cannot-verify` |
| Unknown transformation kind          | `cannot-verify` |
| Missing required subject information | `cannot-verify` |
| Inadmissible behavior                | `fail`          |

## Identity-preserving

A transformation is identity-preserving when the source and target records
describe the same subject identity.

The change is to the record, description, representation, encoding,
correction, or other record structure, not to the represented subject identity.

Examples:

- correcting a typographical error;
- correcting a field value without changing the represented subject;
- re-encoding a source artifact while preserving the same underlying source;
- updating representation metadata that does not change the represented subject.

A profile may define stricter evidence rules for identity-preserving
transformations.

## Identity-breaking

A transformation is identity-breaking when the source and target records
describe distinct subject identities.

References to the source subject do not silently transfer to the target
subject.

The key test is reference behavior: a system must not redirect references to a
different subject unless a profile explicitly permits a declared lineage or
successor relation.

## Identity-inheriting

A transformation is identity-inheriting when the target record represents a
successor subject whose accountability lineage includes the source subject.

Identity-inheriting transformations require lineage.

Required lineage fields include:

- source record ID;
- target record ID;
- lineage relation.

Recommended lineage fields include:

- lineage evidence;
- profile context;
- subject mapping.

Lineage records successor accountability. It does not make the source and
target the same subject.

## No identity question

`no-identity-question` is used when an operation that looks like a
transformation does not raise an identity question for the represented subject.

Examples:

- re-indexing a bundle;
- mechanically reordering records;
- updating export metadata;
- adding an external note that is itself a separate record;
- correcting presentation metadata that does not affect the represented subject.

This behavior prevents systems from forcing every operation into preserving,
breaking, or inheriting.

## Level 4 requirement

At maturity Level 4, a bundle supports transformation declarations and
transformation-behavior checks.

A Level 4 verifier checks declared transformations against:

- declared subject structure;
- declared subject mapping context;
- profile transformation rules;
- AR transformation behavior vocabulary;
- admissibility rules;
- lineage requirements for identity-inheriting behavior;
- profile-specific evidence requirements.

Levels 0 through 3 do not require transformation declarations.

If a lower-level bundle includes transformation declarations anyway, a verifier
may check them because the bundle has exposed them as data.

## Profile responsibilities

A profile that uses transformations should:

- declare recognized transformation kinds;
- make transformation kinds citable;
- declare which record types or subject structures may be connected;
- declare required evidence for each transformation kind;
- declare which AR transformation behavior each transformation claims;
- respect the AR transformation behavior vocabulary;
- respect subject-mapping-sensitive admissibility rules;
- require lineage for identity-inheriting transformations;
- avoid silent reference redirects without declared lineage.

Profiles may define domain-specific transformation kinds only within the AR
behavior vocabulary.

Profiles may not redefine AR transformation behavior meanings.

Profiles may not make an inadmissible behavior valid by local convention.

## Relationship to subjects

The earlier formation model tied transformation behavior directly to fixed
entity kinds. The current AR architecture uses subject structure and subject
mappings instead.

That means profiles can map external vocabularies, domain classifications, or
identity-regime vocabularies into AR subject structure. Transformation checks
then use the declared subject structure and mapping context.

This preserves the useful operational role of transformation behavior without
making AR own a universal ontology.

## Boundary

Transformations help AR preserve how records change, relate, succeed one
another, or remain distinct.

They do not decide:

- truth;
- authority;
- legal effect;
- institutional approval;
- final domain meaning;
- whether a domain transformation is substantively correct outside the
  declared profile and evidence context.
