"""Component-group index and membership checks.

WHY: ``data/component-groups/index.toml`` lists the canonical component groups.
Each must resolve to a ``group.toml`` whose declared id matches its folder, and
any declared ``expected_elements`` must resolve to real element folders. A
dangling group or element reference breaks package composition.
"""

from pathlib import Path
import tomllib


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def check_group_index_resolves(root: Path) -> list[str]:
    """Every indexed group resolves to a group.toml with a matching id."""
    index_path = root / "data" / "component-groups" / "index.toml"
    if not index_path.is_file():
        return ["missing data/component-groups/index.toml"]

    try:
        index = _load_toml(index_path)
    except tomllib.TOMLDecodeError as exc:
        return [f"invalid TOML in component-groups/index.toml: {exc}"]

    groups = index.get("groups")
    if not isinstance(groups, list) or not groups:
        return ["component-groups/index.toml must list a non-empty groups array"]

    failures: list[str] = []

    for group_name in groups:
        if not isinstance(group_name, str):
            failures.append(f"group entry is not a string: {group_name!r}")
            continue

        group_path = root / "data" / "component-groups" / group_name / "group.toml"
        if not group_path.is_file():
            failures.append(f"missing group.toml for group: {group_name}")
            continue

        try:
            group_data = _load_toml(group_path)
        except tomllib.TOMLDecodeError as exc:
            failures.append(f"invalid TOML in {group_name}/group.toml: {exc}")
            continue

        declared_id = group_data.get("id")
        if declared_id != group_name:
            failures.append(
                f"group {group_name} declares id {declared_id!r}, "
                f"expected {group_name!r}"
            )

        expected_elements = group_data.get("expected_elements")
        if expected_elements is None:
            continue
        if not isinstance(expected_elements, list):
            failures.append(f"group {group_name} expected_elements must be a list")
            continue

        for element_name in expected_elements:
            if not isinstance(element_name, str):
                failures.append(f"group {group_name} expected element is not a string")
                continue
            element_path = (
                root / "data" / "elements" / group_name / element_name / "element.toml"
            )
            if not element_path.is_file():
                failures.append(
                    f"group {group_name} expects missing element: {element_name}"
                )

    return failures
