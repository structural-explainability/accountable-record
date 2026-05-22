"""Tests for generated Accountable Record artifacts.

WHY: Generated artifacts are part of the contract surface. These tests exercise
the export, catalog, package-resolution, lock, digest, and generated-validation
chain without relying only on CLI smoke tests.
"""

from pathlib import Path

from accountable_record.exporters.data_export import build_plans, run_export
from accountable_record.generators.artifacts import build_catalog
from accountable_record.generators.lock import build_lock, verify_lock
from accountable_record.resolvers.packages import resolve_packages
from accountable_record.resolvers.versions import digest_toml_file
from accountable_record.validators.generated import validate_generated

ROOT = Path(__file__).resolve().parents[1]


def test_export_plans_are_valid() -> None:
    plans, errors = build_plans(ROOT)

    assert errors == []
    assert plans
    assert {plan.key for plan in plans} >= {
        "vocabulary",
        "namespace",
        "component_groups",
        "elements",
        "mappings",
        "records",
    }


def test_export_dry_run_has_no_errors() -> None:
    result = run_export(ROOT, write=False)

    assert result.errors == []
    assert len(result.written) == 300
    assert "data/export/index.json" in result.written


def test_validate_generated_exports_are_current() -> None:
    result = validate_generated(ROOT)

    assert result.failures == []
    assert result.compared == 300


def test_resolve_packages_has_expected_shape() -> None:
    result = resolve_packages(ROOT)

    assert result.errors == []
    assert len(result.packages) == 3
    assert len(result.elements) == 33


def test_resolve_packages_detects_expected_packages() -> None:
    result = resolve_packages(ROOT)

    package_ids = {package.compact_id for package in result.packages}

    assert package_ids == {
        "se.accountable-record.packages.core",
        "se.accountable-record.packages.source-traceability",
        "se.accountable-record.packages.verification-core",
    }


def test_resolve_packages_detects_expected_core_element() -> None:
    result = resolve_packages(ROOT)

    element_ids = {element.compact_id for element in result.elements}

    assert "se.accountable-record.claims.claim" in element_ids


def test_build_catalog_has_expected_count() -> None:
    result = build_catalog(ROOT)

    assert result.errors == []
    assert result.count == 142
    assert result.document is not None
    assert result.document["schema"] == "ar-element-catalog-1"


def test_build_catalog_orders_elements_by_compact_id() -> None:
    result = build_catalog(ROOT)

    assert result.document is not None

    elements = result.document["elements"]

    assert isinstance(elements, list)

    compact_ids = [entry["compact_id"] for entry in elements if isinstance(entry, dict)]

    assert compact_ids == sorted(compact_ids)


def test_build_lock_has_expected_shape() -> None:
    result = build_lock(ROOT, timestamp=False)

    assert result.errors == []
    assert result.document is not None
    assert result.document["schema"] == "ar-element-lock-1"
    assert result.document["resolved_at"] == ""


def test_build_lock_includes_package_digests() -> None:
    result = build_lock(ROOT, timestamp=False)

    assert result.document is not None

    packages = result.document["packages"]

    assert isinstance(packages, list)
    assert packages

    for package in packages:
        assert isinstance(package, dict)
        assert package["digest_algorithm"] == "sha256"
        assert package["digest_target"] == "canonical-generated-json"
        assert isinstance(package["digest"], str)
        assert len(package["digest"]) == 64


def test_build_lock_includes_element_digests() -> None:
    result = build_lock(ROOT, timestamp=False)

    assert result.document is not None

    elements = result.document["elements"]

    assert isinstance(elements, list)
    assert elements

    for element in elements:
        assert isinstance(element, dict)
        assert element["digest_algorithm"] == "sha256"
        assert element["digest_target"] == "canonical-generated-json"
        assert isinstance(element["digest"], str)
        assert len(element["digest"]) == 64


def test_verify_lock_is_current() -> None:
    result = verify_lock(ROOT)

    assert result.failures == []


def test_digest_toml_file_returns_sha256_hex() -> None:
    digest = digest_toml_file(
        ROOT / "data" / "elements" / "claims" / "claim" / "element.toml"
    )

    assert len(digest) == 64
    assert all(character in "0123456789abcdef" for character in digest)


def test_export_index_manifest_is_in_generated_outputs() -> None:
    result = run_export(ROOT, write=False)

    assert "data/export/index.json" in result.written


def test_generated_validation_compares_export_index() -> None:
    result = validate_generated(ROOT)

    assert result.failures == []
    assert result.compared == 300


def test_lock_resolution_policy_is_present() -> None:
    result = build_lock(ROOT, timestamp=False)

    assert result.document is not None

    policy = result.document["resolution_policy"]

    assert isinstance(policy, dict)
    assert policy["one_major_version_per_identity_per_graph"] is True
    assert policy["range_conflicts_are_errors"] is True
