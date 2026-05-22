"""Tests for generated Accountable Record exports."""

import json
from pathlib import Path


def repo_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict[str, object]:
    """Load a JSON file from the repository root."""
    path = repo_root() / relative_path
    with path.open(encoding="utf-8") as file:
        data = json.load(file)

    assert isinstance(data, dict)
    return data


def test_export_index_exists() -> None:
    """Generated export index exists."""
    path = repo_root() / "data" / "export" / "index.json"

    assert path.exists()
    assert path.is_file()


def test_export_index_has_schema() -> None:
    """Generated export index declares its schema."""
    data = load_json("data/export/index.json")

    assert data.get("schema") == "ar-export-index-1"


def test_export_index_has_generated_export_metadata() -> None:
    """Generated export index has basic metadata."""
    data = load_json("data/export/index.json")

    assert data.get("schema") == "ar-export-index-1"
    assert data


def test_generated_export_paths_exist() -> None:
    """Paths listed in the generated export index exist."""
    data = load_json("data/export/index.json")
    root = repo_root()

    for key, value in data.items():
        if key in {"schema", "generated_at", "version", "contract"}:
            continue

        if isinstance(value, str):
            path = root / value
            assert path.exists(), f"{key} path does not exist: {value}"

        if isinstance(value, list):
            for item in value:
                assert isinstance(item, str)
                path = root / item
                assert path.exists(), f"{key} path does not exist: {item}"


def test_export_contract_source_exists() -> None:
    """Generated exports are distinct from authored export-contract source."""
    export_contract = repo_root() / "data" / "export-contract"
    generated_export = repo_root() / "data" / "export"

    assert export_contract.exists()
    assert generated_export.exists()
    assert export_contract != generated_export
