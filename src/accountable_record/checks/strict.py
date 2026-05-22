"""Stricter checks run only under ``accountable-record check --strict``.

WHY: These checks are meaningful but not yet appropriate as hard gates for a
working-draft contract (for example, released elements still carry TODO
definition text). Keeping them behind ``--strict`` lets the project track
progress toward a clean release without breaking everyday CI.
"""

from pathlib import Path
import tomllib


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def check_manifest_shape(root: Path) -> list[str]:
    """MANIFEST.toml must identify this repo as the AR contract."""
    path = root / "MANIFEST.toml"
    if not path.is_file():
        return ["missing MANIFEST.toml"]

    try:
        data = _load_toml(path)
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid TOML in MANIFEST.toml: {exc}"]

    failures: list[str] = []
    repo = data.get("repo")
    if isinstance(repo, dict) and repo.get("name") not in (
        None,
        "accountable-record",
    ):
        failures.append("MANIFEST.toml repo.name should be accountable-record")
    return failures


def check_no_todo_in_released_elements(root: Path) -> list[str]:
    """Elements marked status=released must not carry TODO definition text."""
    elements_dir = root / "data" / "elements"
    if not elements_dir.is_dir():
        return []

    failures: list[str] = []
    for path in sorted(elements_dir.rglob("element.toml")):
        try:
            data = _load_toml(path)
        except tomllib.TOMLDecodeError:
            continue

        release = data.get("release")
        status = release.get("status") if isinstance(release, dict) else None
        if status != "released":
            continue

        definition = data.get("definition")
        if isinstance(definition, dict):
            text = " ".join(
                value for value in definition.values() if isinstance(value, str)
            )
            if "TODO" in text:
                relative = path.relative_to(root).as_posix()
                failures.append(f"released element still has TODO text: {relative}")

    return failures


def check_docs_cover_component_groups(root: Path) -> list[str]:
    """Every component group should have a corresponding docs page or section."""
    index_path = root / "data" / "component-groups" / "index.toml"
    docs_dir = root / "docs" / "en"
    if not index_path.is_file() or not docs_dir.is_dir():
        return []

    try:
        index = _load_toml(index_path)
    except tomllib.TOMLDecodeError:
        return []

    groups = index.get("groups")
    if not isinstance(groups, list):
        return []

    # Collect all docs text once.
    corpus = " ".join(
        path.read_text(encoding="utf-8") for path in docs_dir.rglob("*.md")
    ).lower()

    failures: list[str] = []
    for group in groups:
        if isinstance(group, str) and group.lower() not in corpus:
            failures.append(f"component group not mentioned in docs/en/: {group}")

    return failures
