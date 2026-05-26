"""Pipeline stage s080: validate generated artifacts."""

from pathlib import Path

from accountable_record.ops.generators.docs import render_reference_docs
from accountable_record.ops.resolvers.versions import digest_toml_file
from accountable_record.ops.validators.generated import validate_generated
from accountable_record.pipeline.types import PipelineStageError, StageResult

STAGE_ID = "s080"
STAGE_CODE = "GN"
STAGE_TITLE = "Validate generated artifacts"


def digest_only(root: Path) -> StageResult:
    """Print sha256 digests for package and element TOML sources."""
    paths = [
        *sorted((root / "data" / "packages").glob("*/package.toml")),
        *sorted((root / "data" / "elements").glob("*/*/element.toml")),
    ]

    for path in paths:
        digest = digest_toml_file(path)
        print(f"{digest}  {path.as_posix()}")

    return StageResult(STAGE_ID, STAGE_CODE, f"printed {len(paths)} digest(s)")


def render_docs_only(root: Path) -> StageResult:
    """Render generated reference Markdown from contract data."""
    result = render_reference_docs(root)
    if result.errors:
        raise PipelineStageError(STAGE_ID, STAGE_CODE, "; ".join(result.errors))

    return StageResult(
        STAGE_ID,
        STAGE_CODE,
        f"rendered {len(result.written)} reference document(s)",
    )


def validate_only(root: Path) -> StageResult:
    """Validate committed generated JSON against regenerated output."""
    result = validate_generated(root)
    if result.failures:
        raise PipelineStageError(STAGE_ID, STAGE_CODE, "; ".join(result.failures))

    return StageResult(
        STAGE_ID,
        STAGE_CODE,
        f"generated artifacts are current ({result.compared} file(s) compared)",
    )


def run(root: Path) -> StageResult:
    """Run generated artifact production and validation."""
    digest_only(root)
    render_docs_only(root)
    validation = validate_only(root)

    return StageResult(STAGE_ID, STAGE_CODE, validation.message)
