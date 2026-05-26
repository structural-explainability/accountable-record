"""Generate schema inventory artifacts.

WHY: Accountable Record data uses explicit schema identifiers across authored
TOML and generated JSON. A generated schema inventory gives validators and
readers a stable view of which schema IDs are currently present.
"""

from dataclasses import dataclass, field
from pathlib import Path
import tomllib
from typing import Any

from accountable_record.ops.exporters.canonical_json import to_canonical_json

SCHEMA_INDEX_SCHEMA = "ar-schema-index-1"


@dataclass
class SchemaIndexBuild:
    """Result of building the schema inventory."""

    document: dict[str, object] | None = None
    errors: list[str] = field(default_factory=list)
    count: int = 0

    @property
    def ok(self) -> bool:
        """True when the schema inventory was built without errors."""
        return self.document is not None and not self.errors


def _collect_schema_values(value: Any) -> list[str]:
    """Collect schema identifier strings from a parsed TOML value."""
    found: list[str] = []

    if isinstance(value, dict):
        for key, item in value.items():
            if key == "schema" and isinstance(item, str):
                found.append(item)
            found.extend(_collect_schema_values(item))
    elif isinstance(value, list):
        for item in value:
            found.extend(_collect_schema_values(item))

    return found


def build_schema_index(root: Path) -> SchemaIndexBuild:
    """Build a schema inventory from authored TOML files."""
    resolved_root = root.resolve()
    data_root = resolved_root / "data"

    if not data_root.is_dir():
        return SchemaIndexBuild(errors=["missing data/ directory"])

    entries: list[dict[str, object]] = []
    errors: list[str] = []

    for path in sorted(data_root.rglob("*.toml")):
        relative = path.relative_to(resolved_root).as_posix()
        try:
            data = tomllib.loads(path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            errors.append(f"invalid TOML in {relative}: {exc}")
            continue

        for schema in sorted(set(_collect_schema_values(data))):
            entries.append(
                {
                    "schema": schema,
                    "source": relative,
                }
            )

    entries.sort(key=lambda entry: (str(entry["schema"]), str(entry["source"])))

    document = {
        "schema": SCHEMA_INDEX_SCHEMA,
        "count": len(entries),
        "schemas": entries,
    }
    return SchemaIndexBuild(document=document, errors=errors, count=len(entries))


def write_schema_index(root: Path) -> SchemaIndexBuild:
    """Write data/catalog/schemas.json."""
    resolved_root = root.resolve()
    build = build_schema_index(resolved_root)

    if build.ok and build.document is not None:
        path = resolved_root / "data" / "catalog" / "schemas.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(to_canonical_json(build.document), encoding="utf-8")

    return build
