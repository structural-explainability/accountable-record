# Verification

Verification is the process by which a verifier checks selected claims against
an Accountable Record bundle and emits a report.

A verifier loads the bundle, identifies the selected claim set, runs every
selected applicable claim, and emits a report whose emissions can be inspected
by identifier.

Authoritative verification semantics live in:

```text
data/verification/
```

Verification-related element types live in:

```text
data/elements/verification/
```

Conformance outcome semantics live in:

```text
data/conformance/
```

## Verifier contract

A verifier satisfies this contract:

```text
verify(bundle, profile?, contract_version) -> report
```

The verifier is deterministic. The same inputs produce the same outputs.
Outcome nondeterminism is a defect.

The verifier is complete over the selected claim set. Every selected applicable
claim is run, regardless of whether earlier claims failed.

A verifier is disciplined about explanation. It reports outcomes, findings,
identifiers, and structured evidence. It does not add uncited editorial
conclusions.

## Claim set selection

Given a bundle, contract version, and optional profile, the verifier selects
claims from:

- AR core claims for the declared contract version and maturity level;
- adopted AR claims selected by the profile;
- profile-defined claims;
- optional claims selected by the bundle, profile, or verifier configuration.

If the same AR claim is selected by more than one source, it is run once.

Profile requirements may change whether an adopted AR claim is mandatory for
profile conformance, but they do not redefine the AR claim.

A bundle that declares no profile is checked against the AR core claims at the
declared level only.

## Outcome rules

Every applicable claim that is run produces one of the outcomes defined by AR:

- `pass`
- `fail`
- `partial`
- `cannot-verify`

The verifier never invents a fifth outcome.

Claims that are not selected, outside the requested maturity level, or not
applicable to the bundle are not run and do not receive outcomes.

If a claim applies but required evidence is missing, the outcome is
`cannot-verify`.

## Evidence

A result may carry an evidence block.

Results with `fail`, `partial`, or `cannot-verify` outcomes must include
evidence sufficient to identify:

- what failed;
- what was partially satisfied;
- what evidence was missing;
- which records or identifiers were involved.

Evidence is structured data collected while running the claim.

A `cannot-verify` outcome's evidence describes what required evidence was
missing.

A `partial` outcome's evidence describes which requirements passed, which
failed, and which records or identifiers were involved.

## Sub-results

A claim that produces `partial` includes sub-results when the sub-checks are
individually citable.

For trait-conformance claims, sub-checks correspond to the trait's specified
requirements.

For record-field claims, sub-checks correspond to the requirements within the
field requirements block.

A profile may treat sub-results as individual data points without rerunning the
parent claim.

## Aggregation

The report summary aggregates outcomes by:

- claim shape;
- maturity level;
- overall result.

The default severity order is:

```text
fail > partial > cannot-verify > pass
```

This severity order is for reporting and aggregation. It does not change the
meaning of individual outcomes.

The report's achieved level is the highest level such that every mandatory AR
claim for that level and all lower levels produced `pass`.

Profiles may define acceptance rules for profile-specific claims, but profiles
do not redefine AR achieved-level semantics.

## Inspecting reports

A report is itself inspectable.

A reader who wants to know why an achieved level is lower than a declared level
can inspect the outcomes for the mandatory claims at the missing level and
lower levels. Those outcomes will include at least one `fail`, `partial`, or
`cannot-verify`.

The report does not require a separate editorial `why` field. The explanation
is carried by claim identifiers, outcomes, findings, and evidence.

## Verifier identity

A report records which verifier produced it.

Verifier identity should include:

- verifier ID;
- verifier version;
- implementation URL, when available.

Example:

```json
{
  "verifier": {
    "id": "accountable-record-py",
    "version": "1.0.0",
    "implementation_url": "https://github.com/structural-explainability/accountable-record-py"
  }
}
```

Conforming verifier implementations must agree on claim outcomes for the same
bundle, profile, claims, traits, and AR contract version.

Differences in timestamps, formatting, diagnostic wording, or
implementation-specific metadata are not contract differences.

## Verifier operations

The AR contract defines validation semantics and describes common verifier
operations.

Implementations choose their own CLI, API, or library surface.

### Inspect

Inspection summarizes a bundle's declared level, profile, record types, record
counts, subject kinds, traits, and transformations.

Inspection does not run claims and does not produce an AR report.

### Validate

Validation runs applicable claims and produces an AR report.

## Verifier-level errors

Some errors prevent verification from producing an AR report.

Examples include:

- input cannot be parsed;
- input is not a readable document;
- required external profile cannot be loaded;
- verifier configuration is invalid.

Verifier-level errors are not claim outcomes.

A bundle that fails to parse as JSON is a verifier-level error. The verifier
emits a parse error and exits without producing a report.

A readable bundle that is missing required AR fields should still produce a
report. Missing required fields in a readable bundle are claim outcomes, not
verifier-level errors.

Implementations may use distinct exit codes for verifier-level errors and
claim-outcome failures. The AR contract specifies the distinction; individual
implementations specify the codes.
