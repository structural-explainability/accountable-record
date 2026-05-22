# Failure Modes

Failure modes describe recurrent structural collapses that make records harder
to inspect, verify, transform, compare, or preserve under disagreement.

A structural collapse occurs when a record fuses things that AR requires to
remain separable.

Authoritative failure-mode source files live in:

````text
data/failure-modes/
````

Failure-mode element types live in:

````text
data/elements/failure-modes/
````

Failure modes are not exhaustive. They name recurring risks that profiles,
claims, traits, mappings, transformation checks, and conformance checks can
detect or help prevent.

## Core concepts

| Concept | Meaning |
| --- | --- |
| Failure Mode | A common way records become unreliable or hard to inspect. |
| Structural Collapse | A record design failure where separate structures are fused. |
| Collapse Pattern | A recurring pattern where a record mixes things that should stay separate. |
| Collapse Detection | A claim, trait, mapping, check, or profile rule used to detect a collapse. |
| Collapse Remediation | Guidance for fixing or avoiding a record collapse. |
| Profile Failure Mode | A domain-specific failure mode defined by a profile. |

## Core AR failure modes

AR defines six core structural-collapse patterns:

| Failure Mode | Collapse |
| --- | --- |
| Source vs. Interpretation | Source material is fused with an interpretation of what the source means. |
| Name vs. Identity | Identity is tied to a mutable name, title, address, label, or designation. |
| Content vs. Status | Content is mutated to encode current status. |
| Event vs. Record | A record describing an event is treated as the event itself. |
| Provenance vs. Authority | Provenance is treated as conferring authority. |
| Context vs. Claim | Contextual limits are folded into the claim itself. |

These are structural patterns, not final judgments about truth, authority,
legitimacy, obligation, enforcement, or domain meaning.

## Source vs. interpretation

This collapse occurs when a record fuses source material with an
interpretation of what the source means.

It may appear in:

- source records whose content field is an extracted thesis rather than an
  extracted passage;
- event records that re-characterize the event using interpretive vocabulary;
- domain records that paraphrase source material into an asserted conclusion.

Detection may use:

- source traceability checks;
- observation non-authority traits;
- interpretation non-mutation checks.

Remediation: keep source-bearing fields faithful to source material. Express
interpretation in separate records, profile-specific interpretive records,
claims, annotations, or cross-referenced structures.

## Name vs. identity

This collapse occurs when identity is tied to a name, title, address, section
number, display label, or other mutable designation.

It may appear in:

- identity records keyed by current display name;
- place or asset records whose stable ID is a postal address;
- rule records identified only by the latest section number.

Detection may use:

- stable identifier checks;
- subject identity checks;
- identity-preserving transformation checks.

Remediation: use stable identifiers for records and subjects. Treat names,
titles, addresses, display labels, section numbers, and other designations as
mutable fields rather than identity.

## Content vs. status

This collapse occurs when content is mutated to encode current status.

It may appear in:

- rule records where repeal is represented by deleting rule text;
- policy records where supersession overwrites prior policy content;
- records that can no longer answer what the content said before the status
  changed.

Detection may use:

- content/status separation traits;
- status history checks;
- interpretation non-mutation checks.

Remediation: keep content separable from status. Express repeal, supersession,
limitation, current status, or other status changes as separate status
structure, status history, linked records, or declared transformations.

## Event vs. record

This collapse occurs when a record treats a representation of an event as the
event itself.

It may appear in:

- event records rewritten when better information arrives;
- audit records where correcting a logged event mutates the original entry;
- records that cannot distinguish the occurrence from later descriptions.

Detection may use:

- subject mapping checks;
- transformation admissibility checks;
- record correction lineage checks.

Remediation: treat the event and the record describing the event as distinct.
Corrections, additions, and reinterpretations should be new records or declared
transformations that reference the original record.

## Provenance vs. authority

This collapse occurs when provenance is treated as conferring authority.

It may appear in:

- records that omit scrutiny because of producer reputation;
- profiles that conflate signed-by with true;
- verifiers that pass checks because provenance is trusted.

Detection may use:

- authority non-assertion traits;
- provenance traceability checks;
- claim outcome checks.

Remediation: record provenance as information about how the record came to be.
Treat authority as a separate interpretive, profile-specific, institutional, or
downstream claim rather than as something AR infers from provenance.

## Context vs. claim

This collapse occurs when contextual limits, scope, environment, observation
conditions, or applicability boundaries are folded into the claim itself.

It may appear in:

- observation records that absorb caveats into their statements;
- rule records whose scope is silently incorporated into content;
- reports that treat partial outcomes as pass because context explains the
  failure.

Detection may use:

- scope declaration traits;
- context subject mappings;
- claim outcome vocabulary checks.

Remediation: keep context separate and citable. Claims may cite their context,
scope, environment, observation conditions, or applicability boundary, but they
should not absorb that context in a way that makes the claim appear stronger or
more general than it is.

## Detection

Failure modes may be detected by:

- claims;
- traits;
- field mappings;
- subject mappings;
- transformation checks;
- conformance checks;
- profile rules.

A detector reports a structural failure, risk, or finding.

It does not decide truth, authority, legitimacy, obligation, enforcement, or
final domain meaning.

## Remediation

Remediation guidance describes how records, profiles, mappings, or checks can
be structured to avoid or repair a collapse.

Remediation does not rewrite records by itself.

Remediation does not decide final domain meaning.

## Profile failure modes

Profiles may define additional domain-specific failure modes.

Profile failure modes compose with AR core failure modes. They may specialize
AR failure modes, but they must not redefine AR failure modes or AR conformance
outcomes.

A profile-defined failure mode should identify:

- the collapse;
- where it appears;
- how it is detected;
- relevant traits, claims, mappings, or transformation rules;
- remediation guidance.

Examples:

- a judicial-record profile might define holding-vs-dictum,
  citation-vs-dependency, or majority-claim-vs-court-endorsement collapses;
- a civic or institutional profile might define contribution-vs-influence or
  meeting-vs-decision collapses.

## Why failure modes matter

Many collapses are locally attractive because they make records simpler in the
short term.

The cost appears later, when a record must be inspected, audited, transformed,
mapped, compared, or reviewed under disagreement.

AR pays structural cost up front so downstream inspection is possible.

## Boundary

Failure modes help AR preserve structural separability.

They do not decide:

- truth;
- authority;
- legitimacy;
- legal effect;
- enforcement;
- final domain meaning;
- whether a profile-specific interpretation is correct.
