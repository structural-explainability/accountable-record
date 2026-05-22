# Conformance

Accountable Record conformance is claim-based.

A verifier runs applicable claims against a bundle and emits a report. The
report records outcomes, evidence, not-run metadata, declared level, and
achieved level.

Authoritative conformance semantics live in:

```text
data/conformance/
```

Conformance-related element types live in:

```text
data/elements/conformance/
```

## Conformance units

AR conformance is evaluated over exported artifacts.

The primary conformance unit is a bundle. A bundle may be evaluated with:

- the AR core profile
- a domain profile
- a declared maturity level
- a selected verifier configuration

Profiles and reports are also AR artifacts, but a report is the output of
verification, not the input being judged.

## Claim outcomes

Every applicable claim that is run produces exactly one outcome:

| Outcome | Meaning |
| --- | --- |
| `pass` | The required evidence is present and the claim is satisfied. |
| `fail` | The required evidence is present and the claim is not satisfied. |
| `partial` | The claim has multiple verifiable requirements; at least one is satisfied, at least one fails, and required evidence is present. |
| `cannot-verify` | The claim applies, but required evidence is missing. |

No other claim outcomes are defined by AR.

A `cannot-verify` outcome is not a pass. It is also not a failure of the
substantive requirement. It means the verifier cannot determine the claim from
the bundle as exported.

## Not-run metadata

A claim may be not run because:

- it is outside the selected maturity level;
- it is outside the selected profile;
- it is optional and not selected;
- its preconditions are absent;
- it is not applicable to the bundle.

Claims that are not run do not receive outcomes.

Not-run metadata may be included so readers can distinguish:

- a claim that was checked and passed;
- a claim that was checked and failed;
- a claim that could not be verified;
- a claim that was not in scope.

## Claim selection

The claim set is determined by:

- the declared AR contract version;
- the declared target maturity level;
- the selected profile;
- the profile's adopted AR claims;
- profile-defined claims;
- verifier configuration for optional claims.

Mandatory AR claims for the declared level and all lower levels are selected.

Optional AR claims are selected only when included by a profile, bundle, or
verifier configuration.

Profile claims are selected according to the profile.

## Maturity-level conformance

AR maturity levels are nested.

A bundle may declare a target maturity level. The verifier reports an achieved
maturity level.

A bundle achieves a level only when all mandatory AR claims for that level and
all lower levels produce `pass`.

A `fail`, `partial`, or `cannot-verify` result for a mandatory AR claim prevents
that level from being achieved.

Profiles may define additional profile conformance rules, but profiles do not
redefine AR achieved-level semantics.

## Profile conformance

A Level 5 bundle is evaluated against a declared domain profile.

A profile may:

- adopt AR claims;
- define profile claims;
- require specific AR traits for record types;
- define domain traits;
- define profile-specific transformation kinds;
- define profile-specific field mappings;
- define additional acceptance rules for profile conformance.

A profile may not:

- redefine AR claim outcomes;
- redefine AR subject-kind or upstream kind semantics;
- redefine AR transformation behaviors;
- weaken AR mandatory claim semantics;
- rename AR identifiers into the profile namespace.

When a profile adopts an AR claim or trait, it cites the AR identifier directly.

## Trait conformance

Trait conformance is evaluated for declared record-type and trait pairs.

A record type that declares a trait is making a structural commitment. The
verifier checks that commitment using the applicable trait-conformance claim.

A record type that does not declare a trait is not failing that trait. The trait
is outside that record type's declared commitment set.

## Evidence and findings

Verifier reports include structured evidence for outcomes.

Results with `fail`, `partial`, or `cannot-verify` outcomes must include enough
evidence for a reader to identify:

- what was checked;
- which records were involved;
- what failed;
- what was partially satisfied;
- what evidence was missing.

Evidence cites bundle elements by stable identifiers.

Evidence does not decide truth, authority, legitimacy, obligation, enforcement,
or domain correctness.

## Summary aggregation

Reports summarize outcomes for claims that were run.

The default severity order for aggregation is:

```text
fail > partial > cannot-verify > pass
```

This order is for reporting and aggregation. It does not change the meaning of
individual outcomes.

## Structural non-conformance

A bundle is structurally non-conforming at a declared level when any mandatory
AR claim for that level or a lower level produces:

- `fail`
- `partial`
- `cannot-verify`

The report should still preserve every run claim result. Verification should
not stop at the first failure when the bundle can still be read.

## Verifier-level errors

Some errors prevent verification from producing an AR report.

Examples include:

- input cannot be parsed;
- input is not a readable document;
- required external profile cannot be loaded;
- verifier configuration is invalid.

Verifier-level errors are not claim outcomes.

If the verifier can read the bundle and run claims, it should produce a report.

If a readable bundle is missing required AR fields, that is a claim outcome, not
a verifier-level error.

## Conformance declarations

A bundle may declare:

- the AR contract version;
- the target maturity level;
- the profile identifier;
- the producing system version.

A declaration is a target claim. It is not proof of achieved conformance.

The verifier report determines achieved conformance.

## Compatibility

Conforming verifier implementations must preserve AR outcome semantics.

For the same bundle, profile, claims, traits, and AR contract version,
implementations should produce the same claim outcomes.

Differences in timestamps, formatting, diagnostic wording, or
implementation-specific metadata are not conformance differences.

Compatibility authority is provided by the AR contract repository, including:

- specifications;
- schemas;
- claim definitions;
- trait definitions;
- examples;
- expected reports.

## Boundary

AR conformance does not establish:

- truth;
- correctness;
- authority;
- legitimacy;
- obligation;
- enforcement;
- causality;
- domain validity;
- institutional approval;
- legal effect.

AR conformance means only that the artifact satisfies the AR structural
requirements that were selected and checked.
