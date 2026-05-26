"""Verifiable-element identity and lock-reference checks, as kit Check records.

WHY (identity contract, AR-D-004): an element's identity is authority-based,
version-free, and package-independent. The compact id encodes
``<alias>.<project>.<component-group>.<local-name>``. These checks confirm each
element's declared identity is internally consistent and that its folder
placement matches its declared component group, so an element cannot silently
drift out of its identity. They also confirm data/locks/elements.lock.json
references only elements and packages that exist in the contract source.
AR-specific; appended to the kit registry via registry.extend.

Converted from (root: Path) -> list[str] to the kit Check contract.
"""

from collections.abc import Iterable
import json
from pathlib import Path
import tomllib

from se_contract_kit.resolution.context import ResolutionContext
from se_contract_kit.validation.registry import Check
from se_contract_kit.validation.results import CheckResult, cannot_verify, failure, ok

__all__ = [
    "IDENTITY_ID",
    "LOCK_ID",
    "check_element_identity_consistency",
    "check_lock_references_resolve",
    "ELEMENT_IDENTITY_CHECK",
    "ELEMENT_LOCK_CHECK",
    "AR_ELEMENT_CHECKS",
]

IDENTITY_ID = "ar.elements.identity-consistency"
LOCK_ID = "ar.elements.lock-references-resolve"


def _load_toml(path: Path) -> dict[str, object]:
    return tomllib.loads(path.read_text(encoding="utf-8"))


def check_element_identity_consistency(
    context: ResolutionContext,
) -> Iterable[CheckResult]:
    """Each element's compact id, local name, group, and folder must agree."""
    root = context.repo_root
    elements_dir = root / "data" / "elements"
    if not elements_dir.is_dir():
        return [cannot_verify(IDENTITY_ID, "missing data/elements/ directory")]

    element_files = sorted(elements_dir.rglob("element.toml"))
    if not element_files:
        return [
            cannot_verify(IDENTITY_ID, "data/elements/ contains no element.toml files")
        ]

    results: list[CheckResult] = []

    for path in element_files:
        relative = path.relative_to(root).as_posix()
        try:
            data = _load_toml(path)
        except tomllib.TOMLDecodeError as exc:
            results.append(failure(IDENTITY_ID, f"invalid TOML in {relative}: {exc}"))
            continue

        identity = data.get("identity")
        namespace = data.get("namespace")
        classification = data.get("classification")

        if not isinstance(identity, dict):
            results.append(failure(IDENTITY_ID, f"{relative} missing [identity] table"))
            continue
        if not isinstance(namespace, dict):
            results.append(
                failure(IDENTITY_ID, f"{relative} missing [namespace] table")
            )
            continue
        if not isinstance(classification, dict):
            results.append(
                failure(IDENTITY_ID, f"{relative} missing [classification] table")
            )
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
            results.append(
                failure(
                    IDENTITY_ID,
                    f"{relative} local_name {local_name!r} != folder {folder_local!r}",
                )
            )
        if declared_group != folder_group:
            results.append(
                failure(
                    IDENTITY_ID,
                    f"{relative} component_group {declared_group!r} != folder {folder_group!r}",
                )
            )

        if (
            isinstance(alias, str)
            and isinstance(project, str)
            and isinstance(declared_group, str)
            and isinstance(local_name, str)
        ):
            expected = f"{alias}.{project}.{declared_group}.{local_name}"
            if compact_id != expected:
                results.append(
                    failure(
                        IDENTITY_ID,
                        f"{relative} compact_id {compact_id!r} != expected {expected!r}",
                    )
                )
        else:
            results.append(
                failure(IDENTITY_ID, f"{relative} has incomplete identity fields")
            )

    return results or [
        ok(IDENTITY_ID, f"{len(element_files)} element(s) identity-consistent")
    ]


def check_lock_references_resolve(context: ResolutionContext) -> Iterable[CheckResult]:
    """Every element compact id in the lock must exist in the contract source."""
    root = context.repo_root
    lock_path = root / "data" / "locks" / "elements.lock.json"
    if not lock_path.is_file():
        return [cannot_verify(LOCK_ID, "missing data/locks/elements.lock.json")]

    try:
        lock = json.loads(lock_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [cannot_verify(LOCK_ID, f"invalid JSON in elements.lock.json: {exc}")]

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

    results: list[CheckResult] = []

    locked_elements = lock.get("elements")
    if not isinstance(locked_elements, list):
        results.append(
            failure(LOCK_ID, "elements.lock.json must define an elements array")
        )
    else:
        for entry in locked_elements:
            if not isinstance(entry, dict):
                results.append(failure(LOCK_ID, "lock element entry is not an object"))
                continue
            compact = entry.get("compact_id")
            if not isinstance(compact, str):
                results.append(
                    failure(LOCK_ID, "lock element entry missing compact_id")
                )
                continue
            if compact not in known:
                results.append(
                    failure(
                        LOCK_ID,
                        f"lock references unknown element compact_id: {compact}",
                    )
                )

    locked_packages = lock.get("packages")
    if not isinstance(locked_packages, list):
        results.append(
            failure(LOCK_ID, "elements.lock.json must define a packages array")
        )

    return results or [ok(LOCK_ID, "all lock references resolve")]


ELEMENT_IDENTITY_CHECK = Check(
    IDENTITY_ID, "Element identity is consistent", check_element_identity_consistency
)
ELEMENT_LOCK_CHECK = Check(
    LOCK_ID, "Element lock references resolve", check_lock_references_resolve
)

AR_ELEMENT_CHECKS: tuple[Check, ...] = (ELEMENT_IDENTITY_CHECK, ELEMENT_LOCK_CHECK)
