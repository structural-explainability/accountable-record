# Subject Mappings

Subject mappings connect external, domain, institutional, or profile-specific
subject vocabularies to AR subject structure.

They let adopters keep the words and classifications they already use while
making the mapping explicit, machine-readable, and citable.

Subject mapping source files live in:

````text
data/subject-mappings/
````

Subject-related element types live in:

````text
data/elements/subjects/
````

## Purpose

AR does not require every system to adopt one universal subject ontology.

Instead, a profile may map its own subject vocabulary into AR subject
structure.

A subject mapping can support:

- record type declarations;
- subject-kind declarations;
- trait selection;
- field mappings;
- transformation checks;
- conformance checks;
- failure-mode detection;
- generated documentation;
- profile-specific reports.

## Mapping guides

A subject mapping guide declares how a profile, domain, institutional system,
or external vocabulary connects to AR subject structure.

Each guide may include:

- identity metadata;
- scope;
- mapping semantics;
- profile responsibilities;
- subject-kind maps;
- mapping questions;
- examples.

Current mapping guide folders include:

````text
data/subject-mappings/identity-regimes/
data/subject-mappings/accountable-entities/
````

These guides are mappings, not canonical AR ontology.

## Mapping questions

A profile should answer questions such as:

| Question | Purpose |
| --- | --- |
| What is the record about? | Identifies the subject the record preserves information about. |
| Which subject vocabulary is used? | Identifies whether the profile uses a local, domain, institutional, or external vocabulary. |
| How is the subject kind mapped? | Declares the mapping from the profile's subject vocabulary to AR subject structure. |

## External vocabularies

External vocabularies remain owned by their publishing authorities.

AR may reference them through mappings.

AR does not rename, redefine, or absorb them.

A mapping entry should preserve:

- the external identifier;
- the external label;
- the AR subject kind or subject structure it maps to;
- the mapping status;
- explanatory notes.

## Example mapping

````toml
[[mappings]]
external_id = "AE.NOR_C"
external_label = "Rule Content"
ar_subject_kind = "normative-content-subject"
mapping_status = "candidate"
notes = """
Maps the content of a rule, policy, standard, contract term, or requirement
into AR subject structure.
"""
````

This mapping does not make `AE.NOR_C` an AR-owned identifier.

It says that a profile may use that external identifier and map it into AR
subject structure.

## Mapping status

A mapping may use statuses such as:

| Status | Meaning |
| --- | --- |
| `candidate` | Proposed or working-draft mapping. |
| `active` | Current mapping used by a profile or package. |
| `deprecated` | Older mapping retained for citability. |
| `superseded` | Mapping replaced by a successor. |

The exact allowed statuses should be defined by the relevant schema or mapping
contract.

## Profile responsibilities

A profile using a subject mapping should:

- declare which mapping guide it uses;
- declare which subject vocabulary it uses;
- bind record types to subject structure;
- cite external identifiers directly;
- avoid redefining external vocabulary;
- provide field mappings when local fields are needed for verification.

## Why this replaces entity-kind source files

Earlier formation material described fixed entity kinds as AR's canonical
vocabulary. The current AR architecture instead treats those classifications as
external or profile-selected subject vocabularies that may be mapped into AR
subject structure. The useful substance is preserved as subject mappings, while
AR itself remains ontology-neutral.

## Boundary

Subject mappings help AR preserve classification structure.

They do not decide whether a classification is true, authoritative, complete,
or universally correct.
