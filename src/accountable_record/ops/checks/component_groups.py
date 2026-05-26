"""AR component-group index and membership checks, as a kit Check record.

WHY: data/component-groups/index.toml lists the canonical component groups.
Each must resolve to a group.toml whose declared id matches its folder, and any
declared expected_elements must resolve to real element folders. A dangling
group or element reference breaks package composition. AR-specific (knows AR's
component-groups/elements layout), appended to the kit registry via extend.

Converted from (root: Path) -> list[str] to the kit Check contract.
"""

from collections.abc import Iterable
import tomllib

from se_contract_kit.resolution.context import ResolutionContext
from se_contract_kit.validation.registry import Check
from se_contract_kit.validation.results import CheckResult, failure, ok

__all__ = ["CHECK_ID", "check_group_index_resolves", "GROUP_INDEX_CHECK"]

CHECK_ID = "ar.component-groups.index-resolves"


def _as_object_dict(value: object) -> dict[str, object] | None:
    """Return value as a string-keyed object dict if it is a dict, else None."""
    if not isinstance(value, dict):
        return None
    narrowed: dict[str, object] = {}
    for key, item in value.items():  # type: ignore[misc]
        narrowed[str(key)] = item  # type: ignore[index]
    return narrowed


def check_group_index_resolves(context: ResolutionContext) -> Iterable[CheckResult]:
    """Every indexed group resolves to a group.toml with a matching id."""
    root = context.repo_root
    index_path = root / "data" / "component-groups" / "index.toml"
    if not index_path.is_file():
        return [failure(CHECK_ID, "missing data/component-groups/index.toml")]

    try:
        parsed: object = tomllib.loads(index_path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        return [
            failure(CHECK_ID, f"invalid TOML in component-groups/index.toml: {exc}")
        ]

    index = _as_object_dict(parsed)
    if index is None:
        return [failure(CHECK_ID, "component-groups/index.toml is not a table")]

    raw_groups = index.get("groups")
    if not isinstance(raw_groups, list) or not raw_groups:
        return [
            failure(
                CHECK_ID,
                "component-groups/index.toml must list a non-empty groups array",
            )
        ]

    results: list[CheckResult] = []

    for raw_group in raw_groups:  # raw_group: object
        if not isinstance(raw_group, str):
            results.append(
                failure(CHECK_ID, f"group entry is not a string: {raw_group!r}")
            )
            continue
        group_name = raw_group

        group_path = root / "data" / "component-groups" / group_name / "group.toml"
        if not group_path.is_file():
            results.append(
                failure(CHECK_ID, f"missing group.toml for group: {group_name}")
            )
            continue

        try:
            group_parsed: object = tomllib.loads(group_path.read_text(encoding="utf-8"))
        except tomllib.TOMLDecodeError as exc:
            results.append(
                failure(CHECK_ID, f"invalid TOML in {group_name}/group.toml: {exc}")
            )
            continue

        group_data = _as_object_dict(group_parsed)
        if group_data is None:
            results.append(failure(CHECK_ID, f"{group_name}/group.toml is not a table"))
            continue

        declared_id = group_data.get("id")
        if declared_id != group_name:
            results.append(
                failure(
                    CHECK_ID,
                    f"group {group_name} declares id {declared_id!r}, "
                    f"expected {group_name!r}",
                )
            )

        expected_elements = group_data.get("expected_elements")
        if expected_elements is None:
            continue
        if not isinstance(expected_elements, list):
            results.append(
                failure(
                    CHECK_ID, f"group {group_name} expected_elements must be a list"
                )
            )
            continue

        for raw_element in expected_elements:  # raw_element: object
            if not isinstance(raw_element, str):
                results.append(
                    failure(
                        CHECK_ID, f"group {group_name} expected element is not a string"
                    )
                )
                continue
            element_path = (
                root / "data" / "elements" / group_name / raw_element / "element.toml"
            )
            if not element_path.is_file():
                results.append(
                    failure(
                        CHECK_ID,
                        f"group {group_name} expects missing element: {raw_element}",
                    )
                )

    return results or [ok(CHECK_ID, "all component groups resolve")]


GROUP_INDEX_CHECK = Check(
    CHECK_ID, "Component-group index resolves", check_group_index_resolves
)
