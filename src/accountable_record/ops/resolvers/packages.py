"""Package resolution: expand packages into a resolved element graph.

WHY (resolution policy in the lock): a resolved graph pins exactly one major
version per identity, and range conflicts are errors. This module reads the
package index and each package's composition, resolves the set of elements they
include, records which package(s) included each element, and reports conflicts.

OBS: Versions in the current contract are simple ("0.1.0"); full semver-range
resolution is not yet needed. The conflict check here enforces the invariant
that an element must not be pinned to two different versions across the graph,
which is the property the lock depends on.
"""

from dataclasses import dataclass, field
from pathlib import Path
import tomllib


@dataclass
class ResolvedPackage:
    """A package resolved from its package.toml.

    Attributes:
        compact_id: Package compact id.
        version: Declared release version.
        canonical_uri: Package canonical URI.
        source: Repo-relative path to package.toml.
        element_ids: Element compact ids the package composes.
    """

    compact_id: str
    version: str
    canonical_uri: str
    source: str
    element_ids: list[str] = field(default_factory=list)


@dataclass
class ResolvedElement:
    """An element resolved into the graph.

    Attributes:
        compact_id: Element compact id.
        version: Pinned version.
        included_by: Package references ("<pkg-id>@<version>") that include it.
    """

    compact_id: str
    version: str
    included_by: list[str] = field(default_factory=list)


@dataclass
class Resolution:
    """The outcome of resolving all packages.

    Attributes:
        packages: Resolved packages, ordered by the package index.
        elements: Resolved elements, ordered by first appearance.
        errors: Resolution problems (conflicts, missing sources).
    """

    packages: list[ResolvedPackage] = field(default_factory=list)
    elements: list[ResolvedElement] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when no resolution errors occurred."""
        return not self.errors


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def _package_order(root: Path) -> list[str]:
    index_path = root / "data" / "packages" / "index.toml"
    if not index_path.is_file():
        return []
    index = _load_toml(index_path)
    packages = index.get("packages")
    if isinstance(packages, list):
        return [p for p in packages if isinstance(p, str)]
    return []


def resolve_packages(root: Path) -> Resolution:
    """Resolve all packages into a flattened element graph.

    Args:
        root: Repository root.

    Returns:
        A :class:`Resolution`. On a healthy contract, ``ok`` is True and every
        package's elements appear in ``elements`` with their including packages.
    """
    resolved_root = root.resolve()
    resolution = Resolution()

    order = _package_order(resolved_root)
    if not order:
        resolution.errors.append("missing or empty data/packages/index.toml")
        return resolution

    # element compact_id -> ResolvedElement (preserve first-seen order)
    element_index: dict[str, ResolvedElement] = {}

    for local_name in order:
        package_path = resolved_root / "data" / "packages" / local_name / "package.toml"
        if not package_path.is_file():
            resolution.errors.append(f"missing package.toml for: {local_name}")
            continue

        try:
            data = _load_toml(package_path)
        except tomllib.TOMLDecodeError as exc:
            resolution.errors.append(
                f"invalid TOML in {local_name}/package.toml: {exc}"
            )
            continue

        identity = data.get("identity")
        release = data.get("release")
        composition = data.get("composition")
        if not isinstance(identity, dict) or not isinstance(release, dict):
            resolution.errors.append(f"package {local_name} missing identity/release")
            continue

        compact_id = identity.get("compact_id")
        version = release.get("version")
        canonical_uri = identity.get("canonical_uri", "")
        if not isinstance(compact_id, str) or not isinstance(version, str):
            resolution.errors.append(f"package {local_name} missing compact_id/version")
            continue

        element_ids: list[str] = []
        if isinstance(composition, dict):
            raw = composition.get("element_types")
            if isinstance(raw, list):
                element_ids = [e for e in raw if isinstance(e, str)]

        package = ResolvedPackage(
            compact_id=compact_id,
            version=version,
            canonical_uri=canonical_uri if isinstance(canonical_uri, str) else "",
            source=package_path.relative_to(resolved_root).as_posix(),
            element_ids=element_ids,
        )
        resolution.packages.append(package)

        package_ref = f"{compact_id}@{version}"
        for element_id in element_ids:
            existing = element_index.get(element_id)
            if existing is None:
                element_index[element_id] = ResolvedElement(
                    compact_id=element_id,
                    version=version,
                    included_by=[package_ref],
                )
            else:
                # WHY: one-major-version-per-identity. Differing versions for
                # the same element across packages is a conflict, not a merge.
                if existing.version != version:
                    resolution.errors.append(
                        f"version conflict for {element_id}: "
                        f"{existing.version} vs {version} (from {package_ref})"
                    )
                if package_ref not in existing.included_by:
                    existing.included_by.append(package_ref)

    resolution.elements = list(element_index.values())
    return resolution
