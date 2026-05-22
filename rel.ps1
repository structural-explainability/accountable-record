#Requires -Version 7.0

<#
Run the Accountable Record release validation sequence.

WHY: This script runs the contract checks, generated-artifact refresh,
generated-artifact validation, Python tests, type checks, and pre-commit checks
used before tagging a release.
#>

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Checking Accountable Record source artifacts..."
uv run accountable-record check --strict

Write-Host "Generating derived artifacts..."
uv run accountable-record export
uv run accountable-record build-catalog
uv run accountable-record resolve-packages
uv run accountable-record write-lock
uv run accountable-record render-docs

Write-Host "Validating generated artifacts and lock..."
uv run accountable-record validate-generated
uv run accountable-record verify-lock

Write-Host "Running tests..."
uv run python -m pytest

Write-Host "Running type checks..."
uv run python -m pyright

Write-Host "Running pre-commit checks..."
uvx pre-commit run --all-files

Write-Host "Release validation completed successfully."
