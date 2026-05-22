"""Generate and verify the element lock file.

WHY: ``data/locks/elements.lock.json`` pins resolved packages and elements with
sha256 digests over their canonical-JSON form. ``write-lock`` regenerates it
from the package sources; ``verify-lock`` confirms the committed lock matches a
fresh resolution (same membership, same digests) so a stale or tampered lock is
caught in CI.

The lock shape mirrors the existing committed lock:
    {
      "schema": "ar-element-lock-1",
      "resolved_at": "<iso8601 or empty>",
      "resolution_policy": { ... },
      "packages": [ { compact_id, version, canonical_uri,
                      digest_algorithm, digest_target, digest, source } ],
      "elements": [ { compact_id, version, included_by[],
                      digest_algorithm, digest_target, digest } ]
    }
"""

from dataclasses import dataclass, field
from datetime import UTC, datetime
import json
from pathlib import Path

from accountable_record.exporters.canonical_json import to_canonical_json
from accountable_record.resolvers.packages import resolve_packages
from accountable_record.resolvers.versions import (
    digest_toml_file,
    element_source_path,
    package_source_path,
)

LOCK_SCHEMA = "ar-element-lock-1"
DIGEST_ALGORITHM = "sha256"
DIGEST_TARGET = "canonical-generated-json"

RESOLUTION_POLICY = {
    "one_major_version_per_identity_per_graph": True,
    "range_conflicts_are_errors": True,
}


@dataclass
class LockBuild:
    """Result of building a lock document.

    Attributes:
        document: The lock as a JSON-ready dict (None if resolution failed).
        errors: Problems encountered (resolution conflicts, missing sources).
    """

    document: dict[str, object] | None = None
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when a document was built without errors."""
        return self.document is not None and not self.errors


def build_lock(root: Path, *, timestamp: bool = True) -> LockBuild:
    """Build the lock document from package sources.

    Args:
        root: Repository root.
        timestamp: When True, set ``resolved_at`` to now (UTC ISO 8601).
            When False, leave it empty (useful for reproducible comparisons).

    Returns:
        A :class:`LockBuild`.
    """
    resolved_root = root.resolve()
    build = LockBuild()

    resolution = resolve_packages(resolved_root)
    build.errors.extend(resolution.errors)

    packages_out: list[dict[str, object]] = []
    for package in resolution.packages:
        source_path = package_source_path(resolved_root, package.compact_id)
        if source_path is None:
            build.errors.append(f"no package source for {package.compact_id}")
            digest = ""
            source_rel = package.source
        else:
            digest = digest_toml_file(source_path)
            source_rel = source_path.relative_to(resolved_root).as_posix()
        packages_out.append(
            {
                "compact_id": package.compact_id,
                "version": package.version,
                "canonical_uri": package.canonical_uri,
                "digest_algorithm": DIGEST_ALGORITHM,
                "digest_target": DIGEST_TARGET,
                "digest": digest,
                "source": source_rel,
            }
        )

    elements_out: list[dict[str, object]] = []
    for element in resolution.elements:
        source_path = element_source_path(resolved_root, element.compact_id)
        if source_path is None:
            build.errors.append(f"no element source for {element.compact_id}")
            digest = ""
        else:
            digest = digest_toml_file(source_path)
        elements_out.append(
            {
                "compact_id": element.compact_id,
                "version": element.version,
                "included_by": list(element.included_by),
                "digest_algorithm": DIGEST_ALGORITHM,
                "digest_target": DIGEST_TARGET,
                "digest": digest,
            }
        )

    resolved_at = ""
    if timestamp:
        resolved_at = datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")

    build.document = {
        "schema": LOCK_SCHEMA,
        "resolved_at": resolved_at,
        "resolution_policy": dict(RESOLUTION_POLICY),
        "packages": packages_out,
        "elements": elements_out,
    }
    return build


def write_lock(root: Path) -> LockBuild:
    """Build the lock and write it to data/locks/elements.lock.json.

    Args:
        root: Repository root.

    Returns:
        The :class:`LockBuild`. The file is written only when the build is ok.
    """
    build = build_lock(root, timestamp=True)
    if build.ok and build.document is not None:
        lock_path = root.resolve() / "data" / "locks" / "elements.lock.json"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        text = json.dumps(build.document, indent=2, ensure_ascii=False) + "\n"
        lock_path.write_text(text, encoding="utf-8")
    return build


def _comparable(document: dict[str, object]) -> str:
    """Return a canonical, timestamp-free comparison form of a lock document."""
    copy = dict(document)
    # WHY: resolved_at is wall-clock; it must not affect equality.
    copy["resolved_at"] = ""
    return to_canonical_json(copy)


@dataclass
class LockVerification:
    """Result of verifying the committed lock against a fresh build.

    Attributes:
        failures: Human-readable mismatches. Empty means the lock is current.
    """

    failures: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when the committed lock matches a fresh resolution."""
        return not self.failures


def verify_lock(root: Path) -> LockVerification:
    """Verify the committed lock matches a freshly built one.

    Compares membership and digests (ignoring ``resolved_at``). Reports the
    specific differences when they diverge.

    Args:
        root: Repository root.

    Returns:
        A :class:`LockVerification`.
    """
    resolved_root = root.resolve()
    verification = LockVerification()

    lock_path = resolved_root / "data" / "locks" / "elements.lock.json"
    if not lock_path.is_file():
        verification.failures.append("missing data/locks/elements.lock.json")
        return verification

    try:
        committed = json.loads(lock_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        verification.failures.append(f"invalid JSON in lock: {exc}")
        return verification

    fresh_build = build_lock(resolved_root, timestamp=False)
    verification.failures.extend(fresh_build.errors)
    if fresh_build.document is None:
        return verification

    if _comparable(committed) != _comparable(fresh_build.document):
        verification.failures.extend(_diff_locks(committed, fresh_build.document))

    return verification


def _digest_map(document: dict[str, object], key: str) -> dict[str, str]:
    out: dict[str, str] = {}
    rows = document.get(key)
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict):
                compact = row.get("compact_id")
                digest = row.get("digest")
                if isinstance(compact, str) and isinstance(digest, str):
                    out[compact] = digest
    return out


def _diff_locks(committed: dict[str, object], fresh: dict[str, object]) -> list[str]:
    """Produce targeted mismatch messages between two lock documents."""
    failures: list[str] = []
    for key in ("packages", "elements"):
        committed_map = _digest_map(committed, key)
        fresh_map = _digest_map(fresh, key)

        missing = sorted(set(fresh_map) - set(committed_map))
        extra = sorted(set(committed_map) - set(fresh_map))
        for compact in missing:
            failures.append(f"lock missing {key[:-1]}: {compact}")
        for compact in extra:
            failures.append(f"lock has stale {key[:-1]}: {compact}")

        for compact in sorted(set(committed_map) & set(fresh_map)):
            if committed_map[compact] != fresh_map[compact]:
                failures.append(
                    f"{key[:-1]} digest changed for {compact} "
                    f"(lock is stale; run write-lock)"
                )
    if not failures:
        failures.append("lock differs from fresh resolution (run write-lock)")
    return failures
