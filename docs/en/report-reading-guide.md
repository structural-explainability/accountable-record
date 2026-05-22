# Report Reading Guide

A report is the artifact a verifier emits after checking a bundle against a
selected level, profile, package set, or verifier configuration.

Conformance source data lives in:

```text
data/conformance/
```

Verification source data lives in:

```text
data/verification/
```

## Outcome Vocabulary

A claim that runs receives exactly one outcome:

| Outcome | Meaning |
| --- | --- |
| `pass` | Required evidence is present and the claim is satisfied. |
| `fail` | Required evidence is present and the claim is not satisfied. |
| `partial` | A multi-requirement claim has mixed satisfied and failed requirements. |
| `cannot-verify` | The claim applies, but required evidence is missing. |

Claims that are not selected or not applicable do not receive outcomes.

They may appear as not-run metadata.

## Reading Failures

A failure means the verifier had enough evidence to determine that the claim was
not satisfied.

A failure should not be hidden by missing evidence in another requirement.

AR uses failure-first composite rollup for this reason.

## Reading cannot-verify

`cannot-verify` means the claim applies, but required evidence is missing.

It is not a pass.
It is not a fail.
It means the verifier cannot complete the check from the available record
structure and evidence.

## Boundary

A report describes verifier results under AR semantics.

It does not decide final truth, authority, legal effect, legitimacy, or domain
meaning.
