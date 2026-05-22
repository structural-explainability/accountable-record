# Maturity Levels

Accountable Record conformance is incremental.

The AR contract is designed for full domain-profile conformance, but systems
may adopt it in levels. Each level preserves compatibility with later levels.
Later levels extend earlier levels; they do not replace them.

## Levels

| Level | Label | Summary |
| --- | --- | --- |
| 0 | Bundle Shape | Exports a valid AR bundle envelope. |
| 1 | Source Traceability | Preserves source references and provenance links. |
| 2 | Accountable Entity Kinds | Declares accountable subject kinds for relevant records. |
| 3 | Trait Declarations | Declares AR traits and field mappings needed to verify trait conformance. |
| 4 | Transformation-Aware Verification | Declares transformations and verifies identity behavior. |
| 5 | Domain Profile Conformance | Satisfies a declared domain profile. |

## Nesting

Levels are nested. A system achieves a level only if it satisfies that level's
mandatory requirements and the mandatory requirements of all lower levels.

## Declared and achieved levels

A system may declare a target level in its bundle. The verifier runs every
mandatory check for the declared level and all lower levels. The verifier
reports the achieved level.

Optional checks run only when selected by the bundle, profile, or verifier
configuration. Optional outcomes appear in the report but do not block the
achieved level unless a profile explicitly makes them mandatory.

## Boundary

A system is not penalized for claims outside its declared level. Claims outside
the declared level may be listed as `not_run` metadata, but they do not receive
outcomes.
