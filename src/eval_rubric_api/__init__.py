"""eval-rubric-api package."""

from eval_rubric_api.aggregation import aggregate_batch_results
from eval_rubric_api.export import export_batch_json
from eval_rubric_api.rules import check_validation_rules
from eval_rubric_api.schemas import validate_rubric
from eval_rubric_api.scoring import score_answer, score_batch, score_with_metadata
from eval_rubric_api.templates import get_template_rubric, list_template_metadata

__all__ = [
    "aggregate_batch_results",
    "check_validation_rules",
    "export_batch_json",
    "get_template_rubric",
    "list_template_metadata",
    "score_answer",
    "score_batch",
    "score_with_metadata",
    "validate_rubric",
]
__version__ = "0.4.0"
