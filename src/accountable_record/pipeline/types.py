"""Types shared by Accountable Record pipeline stages."""

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class StageResult:
    """Successful pipeline stage result."""

    stage_id: str
    code: str
    message: str


class PipelineStageError(RuntimeError):
    """Raised when a pipeline stage cannot complete."""

    def __init__(self, stage_id: str, code: str, message: str) -> None:
        """Initialize a stage failure."""
        self.stage_id = stage_id
        self.code = code
        self.message = message
        super().__init__(f"[{stage_id} {code}] {message}")


StageRunner = Callable[[Path], StageResult]


@dataclass(frozen=True)
class PipelineStage:
    """Registered Accountable Record pipeline stage."""

    stage_id: str
    code: str
    title: str
    run: StageRunner
