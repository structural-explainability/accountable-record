"""Build the element catalog from element sources.

WHY: ``data/catalog/elements.toml`` is a flat discovery index of every element
so consumers can enumerate the contract surface without walking the
``data/elements/`` tree. It is generated, not authored: ``build-catalog``
regenerates it from the element sources.

The catalog is emitted as canonical JSON at ``data/catalog/elements.json`` (the
generated, verifiable form). The authored ``elements.toml`` stub carries only
the schema id; the JSON is the build product.
"""

from dataclasses import dataclass, field
from pathlib import Path
import tomllib

from accountable_record.exporters.canonical_json import to_canonical_json

CATALOG_SCHEMA = "ar-element-catalog-1"


@dataclass
class CatalogBuild:
    """Result of building the catalog.

    Attributes:
        document: The catalog as a JSON-ready dict (None on failure).
        errors: Problems encountered while reading element sources.
        count: Number of elements catalogued.
    """

    document: dict[str, object] | None = None
    errors: list[str] = field(default_factory=list)
    count: int = 0

    @property
    def ok(self) -> bool:
        """True when a catalog was built without errors."""
        return self.document is not None and not self.errors


def build_catalog(root: Path) -> CatalogBuild:
    """Build the element catalog document from element sources.

    Args:
        root: Repository root.

    Returns:
        A :class:`CatalogBuild` whose document lists every element with its
        identity, classification, and release metadata, ordered by compact_id.
    """
    resolved_root = root.resolve()
    build = CatalogBuild()

    elements_dir = resolved_root / "data" / "elements"
    if not elements_dir.is_dir():
        build.errors.append("missing data/elements/ directory")
        return build

    entries: list[dict[str, object]] = []
    for path in sorted(elements_dir.rglob("element.toml")):
        relative = path.relative_to(resolved_root).as_posix()
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            build.errors.append(f"invalid TOML in {relative}: {exc}")
            continue

        identity = data.get("identity")
        classification = data.get("classification")
        release = data.get("release")
        if not isinstance(identity, dict):
            build.errors.append(f"{relative} missing [identity]")
            continue

        entries.append(
            {
                "compact_id": identity.get("compact_id", ""),
                "local_name": identity.get("local_name", ""),
                "label": identity.get("label", ""),
                "canonical_uri": identity.get("canonical_uri", ""),
                "persistent_id": identity.get("persistent_id", ""),
                "component_group": (
                    classification.get("component_group", "")
                    if isinstance(classification, dict)
                    else ""
                ),
                "artifact_kind": (
                    classification.get("artifact_kind", "")
                    if isinstance(classification, dict)
                    else ""
                ),
                "version": (
                    release.get("version", "") if isinstance(release, dict) else ""
                ),
                "status": (
                    release.get("status", "") if isinstance(release, dict) else ""
                ),
                "source": relative,
            }
        )

    entries.sort(key=lambda entry: str(entry.get("compact_id", "")))

    build.count = len(entries)
    build.document = {
        "schema": CATALOG_SCHEMA,
        "count": len(entries),
        "elements": entries,
    }
    return build


def write_catalog(root: Path) -> CatalogBuild:
    """Build the catalog and write it to data/catalog/elements.json.

    Args:
        root: Repository root.

    Returns:
        The :class:`CatalogBuild`. The file is written only when ok.
    """
    build = build_catalog(root)
    if build.ok and build.document is not None:
        catalog_path = root.resolve() / "data" / "catalog" / "elements.json"
        catalog_path.parent.mkdir(parents=True, exist_ok=True)
        catalog_path.write_text(to_canonical_json(build.document), encoding="utf-8")
    return build
