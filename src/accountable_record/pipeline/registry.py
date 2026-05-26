"""Accountable Record pipeline stage registry."""

from accountable_record.pipeline import (
    s010_identity,
    s020_context,
    s030_source,
    s040_elements,
    s050_catalog,
    s060_exports,
    s070_lock,
    s080_generated,
    s090_verify,
)
from accountable_record.pipeline.types import PipelineStage

STAGES: tuple[PipelineStage, ...] = (
    PipelineStage(
        s010_identity.STAGE_ID,
        s010_identity.STAGE_CODE,
        s010_identity.STAGE_TITLE,
        s010_identity.run,
    ),
    PipelineStage(
        s020_context.STAGE_ID,
        s020_context.STAGE_CODE,
        s020_context.STAGE_TITLE,
        s020_context.run,
    ),
    PipelineStage(
        s030_source.STAGE_ID,
        s030_source.STAGE_CODE,
        s030_source.STAGE_TITLE,
        s030_source.run,
    ),
    PipelineStage(
        s040_elements.STAGE_ID,
        s040_elements.STAGE_CODE,
        s040_elements.STAGE_TITLE,
        s040_elements.run,
    ),
    PipelineStage(
        s050_catalog.STAGE_ID,
        s050_catalog.STAGE_CODE,
        s050_catalog.STAGE_TITLE,
        s050_catalog.run,
    ),
    PipelineStage(
        s060_exports.STAGE_ID,
        s060_exports.STAGE_CODE,
        s060_exports.STAGE_TITLE,
        s060_exports.run,
    ),
    PipelineStage(
        s070_lock.STAGE_ID,
        s070_lock.STAGE_CODE,
        s070_lock.STAGE_TITLE,
        s070_lock.run,
    ),
    PipelineStage(
        s080_generated.STAGE_ID,
        s080_generated.STAGE_CODE,
        s080_generated.STAGE_TITLE,
        s080_generated.run,
    ),
    PipelineStage(
        s090_verify.STAGE_ID,
        s090_verify.STAGE_CODE,
        s090_verify.STAGE_TITLE,
        s090_verify.run,
    ),
)

STAGE_BY_ID = {stage.stage_id: stage for stage in STAGES}
