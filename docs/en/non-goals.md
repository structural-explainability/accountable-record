# Non-Goals

AR non-goals identify responsibilities intentionally left outside the
Accountable Record contract.

Operational systems, domain profiles, institutions, or external layers may
provide these capabilities, but AR does not require or define them.

Authoritative non-goal source data lives in:

```text
data/governance/non-goals.toml
```

Governance boundary source data lives in:

```text
data/governance/boundaries.toml
```

## Contract boundary

AR defines exported record structure, subject structure, mappings, traits,
claims, transformation behavior, conformance semantics, verification reports,
and related accountable-record artifacts.

AR does not decide final domain meaning.

AR preserves structure for inspection.

It does not adjudicate the world.

## Out of scope

AR does not define:

- domain truth;
- domain correctness;
- legal authority;
- institutional legitimacy;
- obligation enforcement;
- causal explanation;
- epistemic evaluation;
- analytics;
- optimization;
- recommendation;
- database design;
- APIs;
- authentication;
- authorization;
- access control;
- cryptographic attestation;
- operational deployment.

## Truth and correctness

AR does not decide whether a statement is true.

AR does not decide whether a domain interpretation is correct.

A verifier may report that a claim passed, failed, partially passed, or could
not be verified under the selected AR claim set and profile.

That is not the same as deciding final truth.

## Authority and legitimacy

AR does not decide whether a record, source, claim, profile, institution, or
process is authoritative.

AR does not decide whether an institution, process, decision, actor, or record
is legitimate.

Those judgments belong to domain authorities, institutions, legal systems,
governance processes, or external interpretive layers.

## Legal effect and enforcement

AR does not decide legal effect, enforceability, legal validity, remedies,
sanctions, or obligation enforcement.

AR may preserve records about obligations, rules, status, sources, claims, and
transformations.

It does not enforce them.

## Causality and epistemic evaluation

AR does not decide causal explanation.

AR does not decide credibility, certainty, belief, knowledge, or epistemic
warrant.

A domain profile may define evidence requirements. A verifier may report whether
required evidence is present or missing.

That does not make AR an epistemic adjudicator.

## Analytics and recommendations

AR does not define analytic models, optimization, prediction, recommendation,
or scoring.

Systems may analyze AR exports.

Those analyses are outside the AR contract unless separately represented by a
profile, package, or external system.

## Operational deployment

AR does not define:

- database design;
- APIs;
- authentication;
- authorization;
- access control;
- hosting;
- workflow;
- dashboards;
- runtime deployment.

An implementation may provide any of these.

AR remains the export, mapping, verification, and conformance contract.

## Cryptographic attestation

AR does not require cryptographic attestation.

Attestation may be layered outside the core contract.

A system may sign bundles, profiles, reports, package exports, or lock files,
but AR conformance does not depend on cryptographic attestation unless an
external profile or operational layer requires it.

## Layering

Out-of-scope capabilities may be layered around AR.

A system may use AR exports while also providing:

- databases;
- APIs;
- access control;
- cryptographic attestation;
- workflow;
- analytics;
- domain adjudication.

Those layers may be useful.

They are not AR itself.

## Neutrality

AR preserves record structure, source references, subject mappings, claims,
traits, transformations, conformance results, and failure-mode findings without
turning those structures into final judgments about truth, authority,
legitimacy, enforcement, or domain correctness.

That boundary is what lets AR remain usable under persistent disagreement.
