# Examples

Working examples using real data.

The end-of-2026 commitment includes a set of worked examples that
exercise the AR contract end-to-end:

- One or more bundles at each maturity level (0-5).
- At least two domain profiles demonstrated: judicial records and civic
  influence records.
- Reports produced by both `accountable-record-py` and
  `accountable-record-rs` for each example bundle, demonstrating
  cross-implementation agreement.
- `compare` outputs demonstrating bundle-to-bundle and report-to-report
  comparison.

Each example lives under its own subdirectory with:

- `README.md` - what this example demonstrates.
- `bundle.json` - the bundle.
- `expected-report.json` - the report a conforming verifier produces.
- `notes.md` - annotations on what the example is intended to teach.

## Status

Empty until the contract reaches schema stability. Examples will be
populated as worked cases from JR, CIR, and Civic Interconnect are
adapted to the AR envelope.
