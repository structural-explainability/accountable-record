"""Tests for the contract check engine and the check CLI.

These tests exercise the actual tooling code under
``src/accountable_record/checks/`` and ``commands/``, giving real coverage of
the logic rather than only validating the ``data/`` source.

Two complementary strategies are used:

1. Positive: the real repository must pass every base check. This guards
   against the checks themselves rotting away from the layout they validate.
2. Negative: a synthetic broken repository is built in a temp directory and
   each check is shown to *catch* the specific defect it is responsible for.
   A check that never fails is not a check.
"""

from __future__ import annotations

import json
from pathlib import Path
import tomllib

import pytest

from accountable_record.checks import (
    CheckResult,
    component_groups,
    conformance,
    contracts,
    elements,
    namespace,
    records,
    run_all_checks,
    schemas,
    source,
)
from accountable_record.commands.check import check_main
from accountable_record.commands.root import main as root_main


def repo_root() -> Path:
    """Return the repository root (two levels up from this test file)."""
    return Path(__file__).resolve().parents[1]


# ---------------------------------------------------------------------------
# Positive: the real repository passes.
# ---------------------------------------------------------------------------


def test_real_repo_passes_base_checks() -> None:
    """The real repository must pass every base check."""
    result = run_all_checks(repo_root(), strict_mode=False)
    assert result.ok, "\n".join(result.failures)
    assert len(result.checks_run) >= 15


def test_real_repo_passes_strict_checks() -> None:
    """The real repository must also pass the stricter checks."""
    result = run_all_checks(repo_root(), strict_mode=True)
    assert result.ok, "\n".join(result.failures)
    # Strict mode runs strictly more checks than base mode.
    base = run_all_checks(repo_root(), strict_mode=False)
    assert len(result.checks_run) > len(base.checks_run)


def test_check_result_ok_property() -> None:
    """CheckResult.ok reflects the presence of failures."""
    assert CheckResult().ok is True
    assert CheckResult(failures=["x"]).ok is False


# ---------------------------------------------------------------------------
# A reusable, valid synthetic repository fixture.
# ---------------------------------------------------------------------------


@pytest.fixture
def synthetic_repo(tmp_path: Path) -> Path:
    """Build a minimal but valid AR-shaped repository in a temp dir.

    The synthetic repo carries only what the checks read, arranged so that a
    clean build passes every check. Individual negative tests then mutate one
    thing and assert the responsible check fails.
    """
    root = tmp_path / "repo"
    (root / "data").mkdir(parents=True)

    # Required root files.
    (root / "README.md").write_text("# AR\n", encoding="utf-8")
    (root / "MANIFEST.toml").write_text(
        '[repo]\nname = "accountable-record"\n', encoding="utf-8"
    )
    (root / "CITATION.cff").write_text("cff-version: 1.2.0\n", encoding="utf-8")
    (root / "DECISIONS.md").write_text("# DECISIONS\n", encoding="utf-8")
    (root / "AGENTS.md").write_text("# Agents\n", encoding="utf-8")
    (root / "CHANGELOG.md").write_text("# Changelog\n", encoding="utf-8")
    (root / "pyproject.toml").write_text('[project]\nname = "x"\n', encoding="utf-8")

    # Required docs.
    docs = root / "docs" / "en"
    docs.mkdir(parents=True)
    for name in source.REQUIRED_DOCS:
        doc_path = root / name
        doc_path.parent.mkdir(parents=True, exist_ok=True)
        doc_path.write_text(
            "identity subjects claims traits sources references relations "
            "provenance verification status disagreement conformance maturity "
            "mappings exports governance\n",
            encoding="utf-8",
        )

    # data/index.toml
    (root / "data" / "index.toml").write_text(
        'schema = "ar-data-index-1"\n'
        "[source]\n"
        'vocabulary = "data/vocabulary/terms.toml"\n'
        'component_groups = "data/component-groups/index.toml"\n'
        'elements = "data/elements/"\n'
        "[export]\n"
        'index = "data/export/index.json"\n'
        'vocabulary = "data/export/vocabulary/"\n'
        'component_groups = "data/export/component-groups/"\n'
        'elements = "data/export/elements/"\n',
        encoding="utf-8",
    )
    (root / "data" / "vocabulary").mkdir()
    (root / "data" / "vocabulary" / "terms.toml").write_text(
        'schema = "ar-vocabulary-1"\n', encoding="utf-8"
    )

    # schemas/
    schemas_dir = root / "schemas"
    schemas_dir.mkdir()
    for relative in schemas.REQUIRED_INTERCHANGE_SCHEMAS:
        (root / relative).write_text(
            json.dumps(
                {
                    "$schema": "https://json-schema.org/draft/2020-12/schema",
                    "type": "object",
                }
            ),
            encoding="utf-8",
        )

    # data/conformance/outcomes.toml
    conf = root / "data" / "conformance"
    conf.mkdir()
    outcomes_rows = "".join(
        f'[[outcomes]]\nid = "{oid}"\nlabel = "L"\ndescription = "d"\n'
        f"is_pass = false\nis_failure = false\nevidence_sufficient = true\n"
        f"blocks_mandatory_level = false\n"
        for oid in sorted(conformance.EXPECTED_OUTCOME_IDS)
    )
    (conf / "outcomes.toml").write_text(
        'schema = "ar-conformance-outcomes-1"\n'
        + outcomes_rows
        + "[closed_vocabulary]\n"
        + "only_defined_outcomes_allowed = true\n"
        + "defined_outcomes = ["
        + ", ".join(f'"{oid}"' for oid in sorted(conformance.EXPECTED_OUTCOME_IDS))
        + "]\n",
        encoding="utf-8",
    )

    # data/entity-kinds
    ek = root / "data" / "entity-kinds"
    ek.mkdir()
    ek_rows = "".join(
        f'[[accountable_entity_kinds]]\nid = "{eid}"\norder = {i}\n'
        f'canonical_family = "F"\ncanonical_profile = "P"\nlabel = "L"\n'
        for i, eid in enumerate(sorted(conformance.EXPECTED_ENTITY_KIND_IDS), start=1)
    )
    (ek / "accountable_entity_kinds.toml").write_text(ek_rows, encoding="utf-8")

    # data/component-groups + one element
    cg = root / "data" / "component-groups"
    cg.mkdir()
    (cg / "index.toml").write_text(
        'schema = "ar-component-group-index-1"\ngroups = ["identity"]\n',
        encoding="utf-8",
    )
    (cg / "identity").mkdir()
    (cg / "identity" / "group.toml").write_text(
        'schema = "ar-component-group-1"\nid = "identity"\n'
        'expected_elements = ["namespace"]\n',
        encoding="utf-8",
    )

    el = root / "data" / "elements" / "identity" / "namespace"
    el.mkdir(parents=True)
    (el / "element.toml").write_text(
        'schema = "ar-element-type-1"\n'
        "[identity]\n"
        'compact_id = "se.accountable-record.identity.namespace"\n'
        'local_name = "namespace"\n'
        "[namespace]\n"
        'authority = "structural-explainability.org"\n'
        'authority_alias = "se"\n'
        'project = "accountable-record"\n'
        "[classification]\n"
        'component_group = "identity"\n'
        "[release]\nstatus = \"working-draft\"\n",
        encoding="utf-8",
    )

    # data/locks
    locks = root / "data" / "locks"
    locks.mkdir()
    (locks / "elements.lock.json").write_text(
        json.dumps(
            {
                "schema": "ar-element-lock-1",
                "packages": [{"compact_id": "se.accountable-record.packages.core"}],
                "elements": [
                    {"compact_id": "se.accountable-record.identity.namespace"}
                ],
            }
        ),
        encoding="utf-8",
    )

    # data/namespace
    ns = root / "data" / "namespace"
    ns.mkdir()
    (ns / "authority-aliases.toml").write_text(
        'schema = "ar-authority-aliases-1"\n'
        "[[aliases]]\n"
        'alias = "se"\nauthority = "structural-explainability.org"\n',
        encoding="utf-8",
    )
    (ns / "authorities.toml").write_text(
        'schema = "ar-namespace-authorities-1"\n'
        "[[authorities]]\n"
        'authority = "structural-explainability.org"\n'
        'authority_alias = "se"\n',
        encoding="utf-8",
    )

    # data/contracts
    contracts_dir = root / "data" / "contracts"
    contracts_dir.mkdir()
    (contracts_dir / "identity-contract.toml").write_text(
        'schema = "ar-identity-contract-1"\n'
        "[principles]\n"
        "identity_is_authority_based = true\n"
        "canonical_identity_does_not_include_version = true\n"
        "released_identifiers_must_not_be_renamed = true\n"
        "[element_identity]\n"
        "package_independent = true\n"
        "element_id_must_not_include_package_id = true\n",
        encoding="utf-8",
    )

    # data/records/progressive
    prog = root / "data" / "records" / "progressive"
    prog.mkdir(parents=True)
    for level in range(0, 3):
        (prog / f"level-{level}.json").write_text(
            json.dumps(
                {"schema": "ar-record-1", "maturity_level": level, "elements": []}
            ),
            encoding="utf-8",
        )

    return root


def test_synthetic_repo_is_valid(synthetic_repo: Path) -> None:
    """The synthetic baseline must pass, or negative tests prove nothing."""
    result = run_all_checks(synthetic_repo, strict_mode=False)
    assert result.ok, "\n".join(result.failures)


# ---------------------------------------------------------------------------
# Negative: each check catches its defect.
# ---------------------------------------------------------------------------


def test_missing_root_file_detected(synthetic_repo: Path) -> None:
    """Removing a required root file is caught."""
    (synthetic_repo / "CITATION.cff").unlink()
    failures = source.check_required_source_files(synthetic_repo)
    assert any("CITATION.cff" in f for f in failures)


def test_missing_doc_detected(synthetic_repo: Path) -> None:
    """Removing a required doc is caught."""
    (synthetic_repo / "docs" / "en" / "scope.md").unlink()
    failures = source.check_required_docs(synthetic_repo)
    assert any("scope.md" in f for f in failures)


def test_invalid_toml_detected(synthetic_repo: Path) -> None:
    """Broken TOML is caught."""
    (synthetic_repo / "data" / "broken.toml").write_text(
        "this = = invalid\n", encoding="utf-8"
    )
    failures = source.check_toml_files_parse(synthetic_repo)
    assert any("broken.toml" in f for f in failures)


def test_invalid_json_detected(synthetic_repo: Path) -> None:
    """Broken JSON under data/ is caught."""
    (synthetic_repo / "data" / "broken.json").write_text("{not json", encoding="utf-8")
    failures = source.check_json_files_parse(synthetic_repo)
    assert any("broken.json" in f for f in failures)


def test_data_index_dangling_source_detected(synthetic_repo: Path) -> None:
    """A data/index.toml source path that does not exist is caught."""
    index = synthetic_repo / "data" / "index.toml"
    index.write_text(
        index.read_text(encoding="utf-8").replace(
            'elements = "data/elements/"', 'elements = "data/nope/"'
        ),
        encoding="utf-8",
    )
    failures = source.check_data_index(synthetic_repo)
    assert any("does not exist" in f for f in failures)


def test_missing_schema_detected(synthetic_repo: Path) -> None:
    """A missing interchange schema is caught."""
    (synthetic_repo / "schemas" / "report-1.json").unlink()
    failures = schemas.check_required_schemas(synthetic_repo)
    assert any("report-1.json" in f for f in failures)


def test_extra_outcome_detected(synthetic_repo: Path) -> None:
    """Adding an outcome outside the closed set is caught."""
    outcomes = synthetic_repo / "data" / "conformance" / "outcomes.toml"
    outcomes.write_text(
        outcomes.read_text(encoding="utf-8")
        + '[[outcomes]]\nid = "warning"\nlabel = "L"\ndescription = "d"\n'
        + "is_pass = false\nis_failure = false\nevidence_sufficient = true\n"
        + "blocks_mandatory_level = false\n",
        encoding="utf-8",
    )
    failures = conformance.check_outcomes_closed(synthetic_repo)
    assert any("unexpected ids" in f for f in failures)


def test_forbidden_outcome_token_detected(synthetic_repo: Path) -> None:
    """A forbidden outcome token anywhere in data/ is caught."""
    (synthetic_repo / "data" / "leak.toml").write_text(
        'bad = "inapplicable"\n', encoding="utf-8"
    )
    failures = conformance.check_no_forbidden_outcomes(synthetic_repo)
    assert any("forbidden outcome token" in f for f in failures)


def test_missing_entity_kind_detected(synthetic_repo: Path) -> None:
    """Dropping an entity kind is caught."""
    ek = synthetic_repo / "data" / "entity-kinds" / "accountable_entity_kinds.toml"
    parsed = tomllib.loads(ek.read_text(encoding="utf-8"))
    rows = parsed["accountable_entity_kinds"]
    # Rebuild the file without the AE.OBL row (order 1).
    kept = [row for row in rows if row["id"] != "AE.OBL"]
    rebuilt = "".join(
        f'[[accountable_entity_kinds]]\nid = "{row["id"]}"\n'
        f'order = {row["order"]}\ncanonical_family = "{row["canonical_family"]}"\n'
        f'canonical_profile = "{row["canonical_profile"]}"\nlabel = "{row["label"]}"\n'
        for row in kept
    )
    ek.write_text(rebuilt, encoding="utf-8")
    failures = conformance.check_entity_kinds(synthetic_repo)
    assert failures  # either missing id or non-contiguous order


def test_component_group_dangling_element_detected(synthetic_repo: Path) -> None:
    """A group expecting a missing element is caught."""
    group = synthetic_repo / "data" / "component-groups" / "identity" / "group.toml"
    group.write_text(
        group.read_text(encoding="utf-8").replace(
            'expected_elements = ["namespace"]',
            'expected_elements = ["namespace", "ghost"]',
        ),
        encoding="utf-8",
    )
    failures = component_groups.check_group_index_resolves(synthetic_repo)
    assert any("ghost" in f for f in failures)


def test_element_compact_id_mismatch_detected(synthetic_repo: Path) -> None:
    """A compact_id inconsistent with namespace/group/local is caught."""
    el = (
        synthetic_repo / "data" / "elements" / "identity" / "namespace" / "element.toml"
    )
    el.write_text(
        el.read_text(encoding="utf-8").replace(
            "se.accountable-record.identity.namespace",
            "se.accountable-record.identity.WRONG",
        ),
        encoding="utf-8",
    )
    failures = elements.check_element_identity_consistency(synthetic_repo)
    assert any("compact_id" in f for f in failures)


def test_lock_unknown_element_detected(synthetic_repo: Path) -> None:
    """A lock referencing a non-existent element is caught."""
    lock = synthetic_repo / "data" / "locks" / "elements.lock.json"
    data = json.loads(lock.read_text(encoding="utf-8"))
    data["elements"].append({"compact_id": "se.accountable-record.identity.ghost"})
    lock.write_text(json.dumps(data), encoding="utf-8")
    failures = elements.check_lock_references_resolve(synthetic_repo)
    assert any("ghost" in f for f in failures)


def test_namespace_alias_mismatch_detected(synthetic_repo: Path) -> None:
    """An alias that disagrees between the two namespace tables is caught."""
    auths = synthetic_repo / "data" / "namespace" / "authorities.toml"
    auths.write_text(
        auths.read_text(encoding="utf-8").replace(
            'authority_alias = "se"', 'authority_alias = "other"'
        ),
        encoding="utf-8",
    )
    failures = namespace.check_authority_aliases_resolve(synthetic_repo)
    assert failures


def test_identity_contract_principle_violation_detected(
    synthetic_repo: Path,
) -> None:
    """Flipping a load-bearing identity principle to false is caught."""
    ic = synthetic_repo / "data" / "contracts" / "identity-contract.toml"
    ic.write_text(
        ic.read_text(encoding="utf-8").replace(
            "identity_is_authority_based = true",
            "identity_is_authority_based = false",
        ),
        encoding="utf-8",
    )
    failures = contracts.check_identity_contract_shape(synthetic_repo)
    assert any("identity_is_authority_based" in f for f in failures)


def test_record_maturity_mismatch_detected(synthetic_repo: Path) -> None:
    """A progressive record whose declared level != filename is caught."""
    rec = synthetic_repo / "data" / "records" / "progressive" / "level-1.json"
    rec.write_text(
        json.dumps({"schema": "ar-record-1", "maturity_level": 9, "elements": []}),
        encoding="utf-8",
    )
    failures = records.check_record_maturity_levels(synthetic_repo)
    assert any("maturity_level" in f for f in failures)


def test_engine_isolates_a_crashing_check(monkeypatch: pytest.MonkeyPatch) -> None:
    """A check that raises is reported, not allowed to abort the run."""
    from accountable_record.checks import engine

    def boom(_root: Path) -> list[str]:
        raise RuntimeError("kaboom")

    # Patch the engine's registry so the crashing check is actually run.
    patched = [*engine._BASE_CHECKS, ("boom-check", boom)]
    monkeypatch.setattr(engine, "_BASE_CHECKS", patched)
    result = run_all_checks(repo_root(), strict_mode=False)
    assert any("kaboom" in f for f in result.failures)
    assert "boom-check" in result.checks_run


# ---------------------------------------------------------------------------
# CLI behavior.
# ---------------------------------------------------------------------------


def test_check_main_passes_on_real_repo(capsys: pytest.CaptureFixture[str]) -> None:
    """check_main returns 0 against the real repo and prints OK."""
    code = check_main(["--root", str(repo_root())])
    assert code == 0
    assert "OK" in capsys.readouterr().out


def test_check_main_fails_on_broken_repo(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """check_main returns 1 against an empty/broken repo and prints FAIL."""
    code = check_main(["--root", str(tmp_path)])
    assert code == 1
    assert "FAIL" in capsys.readouterr().err


def test_root_check_command(capsys: pytest.CaptureFixture[str]) -> None:
    """The root dispatcher routes 'check' to the engine."""
    code = root_main(["check", "--root", str(repo_root())])
    assert code == 0


def test_root_validate_source_alias(capsys: pytest.CaptureFixture[str]) -> None:
    """validate-source is an alias for check."""
    code = root_main(["validate-source", "--root", str(repo_root())])
    assert code == 0


def test_root_not_implemented_command(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """A not-yet-implemented command exits 2 with a clear message."""
    code = root_main(["export"])
    assert code == 2
    assert "not yet implemented" in capsys.readouterr().err


def test_root_no_command_runs_check(monkeypatch: pytest.MonkeyPatch) -> None:
    """No subcommand defaults to running check against the cwd."""
    # WHY: argparse subparsers reject a bare '--root X' with no subcommand, so
    # the documented "no command defaults to check" behavior applies to a truly
    # bare invocation that reads the current working directory.
    monkeypatch.chdir(repo_root())
    code = root_main([])
    assert code == 0
