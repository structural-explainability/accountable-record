"""Generate reference documentation from Accountable Record data.

WHY: Human-readable reference pages should be derived from the same authored
data that drives exports, catalogs, locks, and validation. Narrative docs remain
authored by humans; reference docs can be regenerated.
"""

from dataclasses import dataclass, field
from pathlib import Path
import tomllib
from typing import Any


@dataclass
class DocsBuild:
    """Result of generating reference documentation."""

    written: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when docs were generated without errors."""
        return not self.errors


def _load_toml(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        return tomllib.loads(path.read_text(encoding="utf-8")), None
    except tomllib.TOMLDecodeError as exc:
        return None, str(exc)


def _front_matter(title: str) -> str:
    return f"---\ntitle: {title}\n---\n\n"


def build_elements_reference(root: Path) -> tuple[str, list[str]]:
    """Build Markdown reference content for element definitions."""
    resolved_root = root.resolve()
    elements_root = resolved_root / "data" / "elements"
    errors: list[str] = []

    if not elements_root.is_dir():
        return "", ["missing data/elements/ directory"]

    rows: list[tuple[str, str, str, str, str]] = []

    for path in sorted(elements_root.rglob("element.toml")):
        relative = path.relative_to(resolved_root).as_posix()
        data, error = _load_toml(path)
        if error is not None or data is None:
            errors.append(f"invalid TOML in {relative}: {error}")
            continue

        identity = data.get("identity")
        classification = data.get("classification")
        release = data.get("release")

        if not isinstance(identity, dict):
            errors.append(f"{relative} missing [identity]")
            continue

        compact_id = str(identity.get("compact_id", ""))
        label = str(identity.get("label", ""))
        group = ""
        kind = ""
        version = ""

        if isinstance(classification, dict):
            group = str(classification.get("component_group", ""))
            kind = str(classification.get("artifact_kind", ""))

        if isinstance(release, dict):
            version = str(release.get("version", ""))

        rows.append((compact_id, label, group, kind, version))

    rows.sort(key=lambda row: row[0])

    lines = [
        _front_matter("Element Reference"),
        "# Element Reference",
        "",
        "| Compact ID | Label | Component group | Artifact kind | Version |",
        "| --- | --- | --- | --- | --- |",
    ]

    for compact_id, label, group, kind, version in rows:
        lines.append(
            f"| `{compact_id}` | {label} | `{group}` | `{kind}` | `{version}` |"
        )

    lines.append("")
    return "\n".join(lines), errors


def build_packages_reference(root: Path) -> tuple[str, list[str]]:
    """Build Markdown reference content for package definitions."""
    resolved_root = root.resolve()
    packages_root = resolved_root / "data" / "packages"
    errors: list[str] = []

    if not packages_root.is_dir():
        return "", ["missing data/packages/ directory"]

    rows: list[tuple[str, str, str, int]] = []

    for path in sorted(packages_root.glob("*/package.toml")):
        relative = path.relative_to(resolved_root).as_posix()
        data, error = _load_toml(path)
        if error is not None or data is None:
            errors.append(f"invalid TOML in {relative}: {error}")
            continue

        identity = data.get("identity")
        release = data.get("release")
        composition = data.get("composition")

        if not isinstance(identity, dict):
            errors.append(f"{relative} missing [identity]")
            continue

        compact_id = str(identity.get("compact_id", ""))
        label = str(identity.get("label", ""))
        version = ""

        if isinstance(release, dict):
            version = str(release.get("version", ""))

        count = 0
        if isinstance(composition, dict):
            element_types = composition.get("element_types")
            if isinstance(element_types, list):
                count = len(element_types)

        rows.append((compact_id, label, version, count))

    rows.sort(key=lambda row: row[0])

    lines = [
        _front_matter("Package Reference"),
        "# Package Reference",
        "",
        "| Compact ID | Label | Version | Element count |",
        "| --- | --- | --- | ---: |",
    ]

    for compact_id, label, version, count in rows:
        lines.append(f"| `{compact_id}` | {label} | `{version}` | {count} |")

    lines.append("")
    return "\n".join(lines), errors


def render_reference_docs(root: Path) -> DocsBuild:
    """Write generated reference docs under docs/en/reference/."""
    resolved_root = root.resolve()
    output_root = resolved_root / "docs" / "en" / "reference"
    build = DocsBuild()

    outputs = {
        "elements.md": build_elements_reference,
        "packages.md": build_packages_reference,
    }

    for filename, builder in outputs.items():
        text, errors = builder(resolved_root)
        build.errors.extend(errors)
        if errors:
            continue

        path = output_root / filename
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        build.written.append(path.relative_to(resolved_root).as_posix())

    return build
