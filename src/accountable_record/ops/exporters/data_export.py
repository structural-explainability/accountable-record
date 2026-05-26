"""Export authored TOML contract source to canonical JSON.

WHY: ``data/index.toml`` declares a [source] -> [export] mapping. The authored
source of truth is TOML (human-friendly, commentable); the distributed and
verifiable form is canonical JSON. This module performs that conversion so
``digest`` can hash a stable form and ``validate-generated`` can diff committed
output against a fresh regeneration.

Each source entry is either:
- a single ``*.toml`` file  -> one ``*.json`` file at the export path, or
- a directory of ``*.toml`` -> a mirrored tree of ``*.json`` under the export
  directory (preserving subfolders).
"""

from dataclasses import dataclass, field
from pathlib import Path
import tomllib

from accountable_record.ops.exporters.canonical_json import to_canonical_json


@dataclass
class ExportPlan:
    """A single source -> export conversion to perform.

    Attributes:
        key: The logical name from data/index.toml (e.g. "elements").
        source: Absolute path to the authored TOML file or directory.
        target: Absolute path to the JSON file or directory to write.
        is_dir: True when source is a directory tree.
    """

    key: str
    source: Path
    target: Path
    is_dir: bool


@dataclass
class ExportResult:
    """Outcome of an export run.

    Attributes:
        written: Relative paths of JSON files written (or that would be).
        errors: Human-readable problems encountered.
    """

    written: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when no errors occurred."""
        return not self.errors


def _load_index(root: Path) -> dict[str, object]:
    path = root / "data" / "index.toml"
    return tomllib.loads(path.read_text(encoding="utf-8"))


def build_plans(root: Path) -> tuple[list[ExportPlan], list[str]]:
    """Build the export plans from data/index.toml.

    Args:
        root: Repository root.

    Returns:
        (plans, errors). Errors describe source paths that do not exist or a
        malformed index.
    """
    errors: list[str] = []
    try:
        index = _load_index(root)
    except FileNotFoundError:
        return [], ["missing data/index.toml"]
    except tomllib.TOMLDecodeError as exc:
        return [], [f"invalid TOML in data/index.toml: {exc}"]

    source = index.get("source")
    export = index.get("export")
    if not isinstance(source, dict) or not isinstance(export, dict):
        return [], ["data/index.toml must define [source] and [export] tables"]

    plans: list[ExportPlan] = []
    for key, source_rel in source.items():
        if key not in export:
            errors.append(f"source key {key!r} has no matching export path")
            continue
        if not isinstance(source_rel, str) or not isinstance(export[key], str):
            errors.append(f"source/export entries for {key!r} must be strings")
            continue

        source_path = (root / source_rel).resolve()
        target_path = (root / export[key]).resolve()

        if not source_path.exists():
            errors.append(f"source path for {key!r} does not exist: {source_rel}")
            continue

        plans.append(
            ExportPlan(
                key=key,
                source=source_path,
                target=target_path,
                is_dir=source_path.is_dir(),
            )
        )

    return plans, errors


def _export_file(source: Path, target: Path, *, write: bool) -> str:
    """Convert one TOML file to canonical JSON. Returns the JSON text."""
    data = tomllib.loads(source.read_text(encoding="utf-8"))
    text = to_canonical_json(data)
    if write:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    return text


def run_export(root: Path, *, write: bool = True) -> ExportResult:
    """Export all authored TOML source to canonical JSON.

    Args:
        root: Repository root.
        write: When True, write files to disk. When False, perform a dry run
            (parse and serialize, report what would be written, write nothing).

    Returns:
        An :class:`ExportResult`.
    """
    resolved_root = root.resolve()
    result = ExportResult()
    plans, plan_errors = build_plans(resolved_root)
    result.errors.extend(plan_errors)

    for plan in plans:
        if plan.is_dir:
            for toml_path in sorted(plan.source.rglob("*.toml")):
                relative = toml_path.relative_to(plan.source)
                json_path = plan.target / relative.with_suffix(".json")
                try:
                    _export_file(toml_path, json_path, write=write)
                except tomllib.TOMLDecodeError as exc:
                    result.errors.append(f"invalid TOML in {toml_path}: {exc}")
                    continue
                result.written.append(json_path.relative_to(resolved_root).as_posix())
        else:
            # WHY: A file source may map to a directory target (e.g.
            # vocabulary/terms.toml -> data/export/vocabulary/). In that case
            # write <source-stem>.json inside the target directory; otherwise
            # treat the target as the JSON file path directly.
            target_str = str(plan.target)
            if plan.target.is_dir() or target_str.endswith(("/", "\\")):
                json_path = plan.target / plan.source.with_suffix(".json").name
            elif plan.target.suffix == ".json":
                json_path = plan.target
            else:
                json_path = plan.target / plan.source.with_suffix(".json").name
            try:
                _export_file(plan.source, json_path, write=write)
            except tomllib.TOMLDecodeError as exc:
                result.errors.append(f"invalid TOML in {plan.source}: {exc}")
                continue
            result.written.append(json_path.relative_to(resolved_root).as_posix())

    # WHY: data/index.toml declares export.index but has no source.index. The
    # export index is itself generated: a manifest listing every artifact this
    # run produced, so consumers (and validate-generated) have a single entry
    # point. It is written last so it can list the other outputs.
    index = _load_index(resolved_root)
    export_table = index.get("export")
    if isinstance(export_table, dict) and isinstance(export_table.get("index"), str):
        index_path = (resolved_root / export_table["index"]).resolve()
        manifest = {
            "schema": "ar-export-index-1",
            "artifact_count": len(result.written),
            "artifacts": sorted(result.written),
        }
        if write:
            index_path.parent.mkdir(parents=True, exist_ok=True)
            index_path.write_text(to_canonical_json(manifest), encoding="utf-8")
        # The index lists the other artifacts but is itself an output too.
        result.written.append(index_path.relative_to(resolved_root).as_posix())

    return result
