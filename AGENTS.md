# Agents

Follow the repository source-of-truth boundaries.
Data files define the specification.
Generated files must not be hand edited.

## Annotations

This repository uses the Structural Explainability annotation convention for
rationale-bearing comments in code, configuration, and generated-source
templates.

Common annotation prefixes include:

- `WHY:` rationale for a decision or structure
- `OBS:` observation about current behavior or known limitation
- `REQ:` requirement that should not be weakened casually
- `ALT:` alternative considered
- `CUSTOM:` intentional local customization

Do not remove rationale-bearing annotations unless the underlying decision,
requirement, or alternative is also being updated.

Reference:
<https://github.com/structural-explainability/.github/blob/main/ANNOTATIONS.md>
