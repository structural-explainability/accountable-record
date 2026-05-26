r"""Canonical JSON serialization.

WHY: Digests, lock files, and generated-output diffs must be stable across
machines, Python versions, and authoring churn (TOML comment/whitespace edits).
A single canonical form makes "did the contract content change?" answerable by
byte comparison.

Canonical form:
- UTF-8 text, keys sorted lexicographically at every level.
- Two-space indentation, newline after each element, trailing newline at EOF.
- ``ensure_ascii=False`` so non-ASCII stays human-readable.
- Separators with no trailing whitespace.
- TOML multiline strings are normalized: a single trailing newline is stripped
  so ``\"\"\"...\n\"\"\"`` and ``\"...\"`` compare equal in content.
"""

import json
from typing import Any


def normalize(value: Any) -> Any:
    """Recursively normalize a parsed-TOML value for canonical output.

    Strips a single trailing newline from strings (TOML triple-quoted blocks
    almost always carry one), and recurses through dicts and lists. Other
    scalar types pass through unchanged.

    Args:
        value: A value parsed from TOML (dict, list, str, int, float, bool).

    Returns:
        The normalized value.
    """
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, list):
        return [normalize(item) for item in value]
    if isinstance(value, str):
        # WHY: Triple-quoted TOML blocks carry a trailing newline that is an
        # authoring artifact, not content. Strip exactly one.
        if value.endswith("\n"):
            return value[:-1]
        return value
    return value


def to_canonical_json(value: Any) -> str:
    """Serialize a value to canonical JSON text (with trailing newline).

    Args:
        value: Any JSON-serializable value. It is normalized first.

    Returns:
        Canonical JSON string ending in a single newline.
    """
    normalized = normalize(value)
    text = json.dumps(
        normalized,
        sort_keys=True,
        indent=2,
        ensure_ascii=False,
        separators=(",", ": "),
    )
    return text + "\n"
