"""Canonical-JSON digest computation and source-path resolution.

WHY (lock model): each package and element in the lock carries a digest with
``digest_algorithm = "sha256"`` and
``digest_target = "canonical-generated-json"``. The digest must be computed over
the *canonical JSON* form of the artifact, not the authored TOML, so that
comment/whitespace edits do not change identity.

For an element, the digest target is the canonical JSON of its ``element.toml``.
For a package, the digest target is the canonical JSON of its ``package.toml``.
"""

import hashlib
from pathlib import Path
import tomllib

from accountable_record.exporters.canonical_json import to_canonical_json


def digest_text(text: str) -> str:
    """Return the sha256 hex digest of UTF-8 text."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def digest_toml_file(path: Path) -> str:
    """Return the sha256 digest of a TOML file's canonical-JSON form.

    Args:
        path: Path to a ``*.toml`` source file.

    Returns:
        Hex sha256 digest of the canonical JSON serialization.
    """
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return digest_text(to_canonical_json(data))


def element_source_path(root: Path, compact_id: str) -> Path | None:
    """Resolve an element compact_id to its element.toml source path.

    The compact id is ``alias.project.group.local_name``; the element lives at
    ``data/elements/<group>/<local_name>/element.toml``.

    Args:
        root: Repository root.
        compact_id: e.g. ``se.accountable-record.claims.claim``.

    Returns:
        The path if it exists, else None.
    """
    parts = compact_id.split(".")
    if len(parts) < 4:
        return None
    group = parts[2]
    local_name = ".".join(parts[3:])
    candidate = root / "data" / "elements" / group / local_name / "element.toml"
    return candidate if candidate.is_file() else None


def package_source_path(root: Path, compact_id: str) -> Path | None:
    """Resolve a package compact_id to its package.toml source path.

    Args:
        root: Repository root.
        compact_id: e.g. ``se.accountable-record.packages.core``.

    Returns:
        The path if it exists, else None.
    """
    parts = compact_id.split(".")
    if len(parts) < 4:
        return None
    local_name = parts[-1]
    candidate = root / "data" / "packages" / local_name / "package.toml"
    return candidate if candidate.is_file() else None
