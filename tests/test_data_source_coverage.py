"""Tests for Accountable Record source-data coverage."""

from pathlib import Path
import tomllib
from typing import Any


def repo_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[1]


def load_toml(relative_path: str) -> dict[str, Any]:
    """Load a TOML file from the repository root."""
    path = repo_root() / relative_path
    with path.open("rb") as file:
        return tomllib.load(file)


def test_data_index_source_paths_exist() -> None:
    """Every path listed in data/index.toml source block exists."""
    data = load_toml("data/index.toml")

    source = data.get("source")
    assert isinstance(source, dict)

    for key, value in source.items():
        assert isinstance(value, str), key

        path = repo_root() / value
        assert path.exists(), f"{key} path does not exist: {value}"


def test_data_index_export_paths_are_declared() -> None:
    """data/index.toml declares generated export paths."""
    data = load_toml("data/index.toml")

    export = data.get("export")
    assert isinstance(export, dict)

    assert "index" in export
    assert "vocabulary" in export
    assert "component_groups" in export
    assert "elements" in export


def test_component_group_index_entries_exist() -> None:
    """Component-group index entries point to existing group files."""
    data = load_toml("data/component-groups/index.toml")

    groups = data.get("groups")
    assert isinstance(groups, list)
    assert groups

    for group in groups:
        assert isinstance(group, str)

        path = repo_root() / "data" / "component-groups" / group / "group.toml"
        assert path.exists(), f"component group path does not exist: {path}"


def test_component_group_expected_elements_exist_when_declared() -> None:
    """Declared component-group expected element folders exist."""
    group_paths = sorted(
        (repo_root() / "data" / "component-groups").glob("*/group.toml")
    )

    assert group_paths

    for group_path in group_paths:
        data = load_toml(str(group_path.relative_to(repo_root())))

        group_id = data.get("id")
        expected_elements = data.get("expected_elements")

        assert isinstance(group_id, str), group_path

        if expected_elements is None:
            continue

        assert isinstance(expected_elements, list), group_path

        for element_name in expected_elements:
            assert isinstance(element_name, str), group_path

            element_path = (
                repo_root()
                / "data"
                / "elements"
                / group_id
                / element_name
                / "element.toml"
            )
            assert element_path.exists(), f"missing element: {element_path}"
