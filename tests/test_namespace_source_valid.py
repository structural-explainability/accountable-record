"""Tests for namespace and identifier source data."""

from pathlib import Path
import re
import tomllib
from typing import Any

COMPACT_ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*(?:\.[a-z][a-z0-9-]*)+$")


def repo_root() -> Path:
    """Return the repository root."""
    return Path(__file__).resolve().parents[1]


def load_toml(relative_path: str) -> dict[str, Any]:
    """Load a TOML file from the repository root."""
    path = repo_root() / relative_path
    with path.open("rb") as file:
        return tomllib.load(file)


def iter_element_files() -> list[Path]:
    """Return all element.toml files."""
    root = repo_root() / "data" / "elements"
    return sorted(root.glob("*/*/element.toml"))


def test_element_files_exist() -> None:
    """The repository defines verifiable element source files."""
    assert iter_element_files()


def test_element_compact_ids_are_unique() -> None:
    """Element compact identifiers are unique."""
    compact_ids: list[str] = []

    for path in iter_element_files():
        data = load_toml(str(path.relative_to(repo_root())))
        identity = data.get("identity")
        assert isinstance(identity, dict), path

        compact_id = identity.get("compact_id")
        assert isinstance(compact_id, str), path
        assert compact_id

        compact_ids.append(compact_id)

    assert len(compact_ids) == len(set(compact_ids))


def test_element_compact_ids_match_pattern() -> None:
    """Element compact identifiers use the expected dotted lowercase form."""
    for path in iter_element_files():
        data = load_toml(str(path.relative_to(repo_root())))
        identity = data.get("identity")
        assert isinstance(identity, dict), path

        compact_id = identity.get("compact_id")
        assert isinstance(compact_id, str), path

        assert COMPACT_ID_PATTERN.fullmatch(compact_id), compact_id


def test_element_identity_fields_are_present() -> None:
    """Each element declares the required identity fields."""
    required_fields = {
        "canonical_uri",
        "persistent_id",
        "compact_id",
        "local_name",
        "label",
    }

    for path in iter_element_files():
        data = load_toml(str(path.relative_to(repo_root())))
        identity = data.get("identity")
        assert isinstance(identity, dict), path

        missing = required_fields - set(identity)
        assert not missing, f"{path}: missing {sorted(missing)}"


def test_element_local_name_matches_folder_name() -> None:
    """Element local names match their element folder names."""
    for path in iter_element_files():
        data = load_toml(str(path.relative_to(repo_root())))
        identity = data.get("identity")
        assert isinstance(identity, dict), path

        local_name = identity.get("local_name")
        assert isinstance(local_name, str), path

        assert local_name == path.parent.name


def test_element_classification_matches_folder_group() -> None:
    """Element component group declarations match their folder groups."""
    for path in iter_element_files():
        data = load_toml(str(path.relative_to(repo_root())))
        classification = data.get("classification")
        assert isinstance(classification, dict), path

        component_group = classification.get("component_group")
        assert isinstance(component_group, str), path

        assert component_group == path.parent.parent.name


def test_identity_contract_declares_version_free_identifiers() -> None:
    """The identity contract keeps versions out of canonical identifiers."""
    data = load_toml("data/contracts/identity-contract.toml")

    canonical_uri = data.get("canonical_uri")
    persistent_id = data.get("persistent_id")
    compact_id = data.get("compact_id")

    assert isinstance(canonical_uri, dict)
    assert isinstance(persistent_id, dict)
    assert isinstance(compact_id, dict)

    assert canonical_uri["version_included"] is False
    assert persistent_id["version_included"] is False
    assert compact_id["version_included"] is False
