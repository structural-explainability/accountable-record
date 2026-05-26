"""AR-specific strict checks, appended to the kit registry via registry.extend.

These encode AR's own artifact model and its working-draft policy, which the
generic kit deliberately does not know about:

  - released-only TODO policy: TODO text is allowed in draft elements but not
    in elements marked release.status = "released" (the kit's generic
    structural.strict.no-todo is blunter — it flags TODO in any artifact — and
    is intentionally NOT used by AR, which permits TODO in drafts).
  - docs coverage: every declared component group must be mentioned in docs/en/.

Both are strict-only: they gate releases, not everyday CI.

The manifest-shape check that previously lived here has been removed; manifest
validation is delegated to se-manifest-schema (`se-manifest validate-manifest`).
"""

from collections.abc import Iterable

from se_contract_kit.base.errors import ContractKitError
from se_contract_kit.base.io import read_text, read_toml
from se_contract_kit.resolution.context import ResolutionContext
from se_contract_kit.validation.registry import Check
from se_contract_kit.validation.results import CheckResult, failure, ok, partial

__all__ = [
    "NO_TODO_CHECK_ID",
    "DOCS_COVERAGE_CHECK_ID",
    "check_no_todo_in_released_elements",
    "check_docs_cover_component_groups",
    "NO_TODO_CHECK",
    "DOCS_COVERAGE_CHECK",
    "AR_STRICT_CHECKS",
]

NO_TODO_CHECK_ID = "ar.strict.no-todo-in-released-elements"
DOCS_COVERAGE_CHECK_ID = "ar.strict.docs-cover-component-groups"

_RELEASED_STATUS = "released"
_TODO_MARKER = "TODO"


def _as_object_dict(value: object) -> dict[str, object] | None:
    """Return value as a string-keyed object dict if it is a dict, else None."""
    if not isinstance(value, dict):
        return None
    narrowed: dict[str, object] = {}
    for key, item in value.items():  # type: ignore[misc]
        narrowed[str(key)] = item  # type: ignore[index]
    return narrowed


def check_no_todo_in_released_elements(
    context: ResolutionContext,
) -> Iterable[CheckResult]:
    """Released elements must not carry TODO definition text.

    AR's working-draft policy: TODO is permitted in draft elements, forbidden
    once an element is marked release.status = "released". Scans the repo's
    data/elements tree for element.toml files at released status and checks
    their definition text.
    """
    elements_dir = context.repo_root / "data" / "elements"
    if not elements_dir.is_dir():
        return [partial(NO_TODO_CHECK_ID, "no data/elements directory to check")]

    results: list[CheckResult] = []
    checked = 0

    for path in sorted(elements_dir.rglob("element.toml")):
        try:
            data = _as_object_dict(read_toml(path))
        except ContractKitError:
            # existence/parse is structural.source's job; skip quietly here
            continue
        if data is None:
            continue

        release = _as_object_dict(data.get("release"))
        status = release.get("status") if release is not None else None
        if status != _RELEASED_STATUS:
            continue

        checked += 1
        definition = _as_object_dict(data.get("definition"))
        if definition is None:
            continue

        text = " ".join(
            value for value in definition.values() if isinstance(value, str)
        )
        if _TODO_MARKER in text:
            relative = path.relative_to(context.repo_root).as_posix()
            results.append(
                failure(
                    NO_TODO_CHECK_ID,
                    f"released element still has TODO definition text: {relative}",
                    detail={"path": relative},
                )
            )

    if not results:
        results.append(
            ok(NO_TODO_CHECK_ID, f"{checked} released element(s) free of TODO text")
        )
    return results


def check_docs_cover_component_groups(
    context: ResolutionContext,
) -> Iterable[CheckResult]:
    """Every declared component group must be mentioned in docs/en/.

    Reads data/component-groups/index.toml for the declared groups and confirms
    each appears somewhere in the docs/en/ markdown corpus.
    """
    index_path = context.repo_root / "data" / "component-groups" / "index.toml"
    docs_dir = context.repo_root / "docs" / "en"
    if not index_path.is_file() or not docs_dir.is_dir():
        return [
            partial(
                DOCS_COVERAGE_CHECK_ID,
                "no component-groups index or docs/en directory to check",
            )
        ]

    try:
        index = _as_object_dict(read_toml(index_path))
    except ContractKitError as exc:
        return [
            failure(
                DOCS_COVERAGE_CHECK_ID,
                f"component-groups index unreadable: {exc}",
            )
        ]
    if index is None:
        return [
            failure(DOCS_COVERAGE_CHECK_ID, "component-groups index is not a table")
        ]

    raw_groups = index.get("groups")
    if not isinstance(raw_groups, list):
        return [
            partial(DOCS_COVERAGE_CHECK_ID, "component-groups index declares no groups")
        ]
    groups: list[str] = [str(group) for group in raw_groups]  # type: ignore[misc]

    corpus_parts: list[str] = []
    for doc_path in docs_dir.rglob("*.md"):
        try:
            corpus_parts.append(read_text(doc_path))
        except ContractKitError:
            continue
    corpus = " ".join(corpus_parts).lower()

    results: list[CheckResult] = []
    for group in groups:
        if group.lower() not in corpus:
            results.append(
                failure(
                    DOCS_COVERAGE_CHECK_ID,
                    f"component group not mentioned in docs/en/: {group}",
                    detail={"group": group},
                )
            )

    if not results:
        results.append(
            ok(
                DOCS_COVERAGE_CHECK_ID,
                f"all {len(groups)} component group(s) covered in docs/en/",
            )
        )
    return results


NO_TODO_CHECK = Check(
    check_id=NO_TODO_CHECK_ID,
    title="No TODO in released elements",
    run=check_no_todo_in_released_elements,
    strict_only=True,
)

DOCS_COVERAGE_CHECK = Check(
    check_id=DOCS_COVERAGE_CHECK_ID,
    title="Docs cover all component groups",
    run=check_docs_cover_component_groups,
    strict_only=True,
)

# Convenience: the AR strict checks as a tuple, for registry.extend(*AR_STRICT_CHECKS).
AR_STRICT_CHECKS: tuple[Check, ...] = (NO_TODO_CHECK, DOCS_COVERAGE_CHECK)
