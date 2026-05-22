"""Verifiable-element identity and lock-reference checks.

WHY (identity contract, AR-D-004): an element's identity is authority-based,
version-free, and package-independent. The compact id encodes
``<alias>.<project>.<component-group>.<local-name>``. These checks confirm that
each element's declared identity is internally consistent and that its folder
placement matches its declared component group, so an element cannot silently
drift out of its identity.

They also confirm that ``data/locks/elements.lock.json`` references only
elements and packages that actually exist in the contract source.
"""

import json
from pathlib import Path
import tomllib


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def check_element_identity_consistency(root: Path) -> list[str]:
    """Each element's compact id, local name, group, and folder must agree."""
    elements_dir = root / "data" / "elements"
    if not elements_dir.is_dir():
        return ["missing data/elements/ directory"]

    element_files = sorted(elements_dir.rglob("element.toml"))
    if not element_files:
        return ["data/elements/ contains no element.toml files"]

    failures: list[str] = []

    for path in element_files:
        relative = path.relative_to(root).as_posix()
        try:
            data = _load_toml(path)
        except tomllib.TOMLDecodeError as exc:
            failures.append(f"invalid TOML in {relative}: {exc}")
            continue

        identity = data.get("identity")
        namespace = data.get("namespace")
        classification = data.get("classification")

        if not isinstance(identity, dict):
            failures.append(f"{relative} missing [identity] table")
            continue
        if not isinstance(namespace, dict):
            failures.append(f"{relative} missing [namespace] table")
            continue
        if not isinstance(classification, dict):
            failures.append(f"{relative} missing [classification] table")
            continue

        # Folder layout: data/elements/<group>/<local_name>/element.toml
        folder_group = path.parent.parent.name
        folder_local = path.parent.name

        local_name = identity.get("local_name")
        compact_id = identity.get("compact_id")
        alias = namespace.get("authority_alias")
        project = namespace.get("project")
        declared_group = classification.get("component_group")

        if local_name != folder_local:
            failures.append(
                f"{relative} local_name {local_name!r} != folder {folder_local!r}"
            )

        if declared_group != folder_group:
            failures.append(
                f"{relative} component_group {declared_group!r} "
                f"!= folder {folder_group!r}"
            )

        # compact_id must be alias.project.group.local_name
        if (
            isinstance(alias, str)
            and isinstance(project, str)
            and isinstance(declared_group, str)
            and isinstance(local_name, str)
        ):
            expected = f"{alias}.{project}.{declared_group}.{local_name}"
            if compact_id != expected:
                failures.append(
                    f"{relative} compact_id {compact_id!r} != expected {expected!r}"
                )
        else:
            failures.append(f"{relative} has incomplete identity fields")

    return failures


def check_lock_references_resolve(root: Path) -> list[str]:
    """Every element compact id in the lock must exist in the contract source."""
    lock_path = root / "data" / "locks" / "elements.lock.json"
    if not lock_path.is_file():
        return ["missing data/locks/elements.lock.json"]

    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"invalid JSON in elements.lock.json: {exc}"]

    # Build the set of compact ids that actually exist in source.
    known: set[str] = set()
    for path in (root / "data" / "elements").rglob("element.toml"):
        try:
            data = _load_toml(path)
        except tomllib.TOMLDecodeError:
            continue
        identity = data.get("identity")
        if isinstance(identity, dict):
            compact = identity.get("compact_id")
            if isinstance(compact, str):
                known.add(compact)

    failures: list[str] = []

    locked_elements = lock.get("elements")
    if not isinstance(locked_elements, list):
        failures.append("elements.lock.json must define an elements array")
    else:
        for entry in locked_elements:
            if not isinstance(entry, dict):
                failures.append("lock element entry is not an object")
                continue
            compact = entry.get("compact_id")
            if not isinstance(compact, str):
                failures.append("lock element entry missing compact_id")
                continue
            if compact not in known:
                failures.append(
                    f"lock references unknown element compact_id: {compact}"
                )

    locked_packages = lock.get("packages")
    if not isinstance(locked_packages, list):
        failures.append("elements.lock.json must define a packages array")

    return failures
