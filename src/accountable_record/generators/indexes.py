"""Generate index artifacts for Accountable Record data.

WHY: Indexes are generated discovery surfaces. They should be reproducible from
authored source files rather than maintained by hand.
"""

from dataclasses import dataclass, field
from pathlib import Path
import tomllib

from accountable_record.exporters.canonical_json import to_canonical_json

EXPORT_INDEX_SCHEMA = "ar-export-index-1"


@dataclass
class IndexBuild:
    """Result of building an index artifact."""

    document: dict[str, object] | None = None
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when an index document was built without errors."""
        return self.document is not None and not self.errors


def build_export_index(root: Path, artifacts: list[str]) -> IndexBuild:
    """Build the generated export index document.

    Args:
        root: Repository root.
        artifacts: Repo-relative generated artifact paths, excluding the export
            index itself.

    Returns:
        Generated export index build result.
    """
    index_path = root / "data" / "index.toml"
    if not index_path.is_file():
        return IndexBuild(errors=["missing data/index.toml"])

    try:
        index = tomllib.loads(index_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return IndexBuild(errors=[f"invalid TOML in data/index.toml: {exc}"])

    export = index.get("export")
    if not isinstance(export, dict) or not isinstance(export.get("index"), str):
        return IndexBuild(errors=["data/index.toml missing export.index"])

    document = {
        "schema": EXPORT_INDEX_SCHEMA,
        "artifact_count": len(artifacts),
        "artifacts": sorted(artifacts),
    }
    return IndexBuild(document=document)


def write_export_index(root: Path, artifacts: list[str]) -> IndexBuild:
    """Write data/export/index.json from the generated artifact list."""
    resolved_root = root.resolve()
    build = build_export_index(resolved_root, artifacts)

    if build.ok and build.document is not None:
        index = tomllib.loads(
            (resolved_root / "data" / "index.toml").read_text(encoding="utf-8")
        )
        export = index["export"]
        path = resolved_root / export["index"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(to_canonical_json(build.document), encoding="utf-8")

    return build
