"""Rubric schema validation."""

from __future__ import annotations

from pydantic import BaseModel, Field, ValidationError

from eval_rubric_api.rules import check_validation_rules

MAX_DIMENSIONS = 20
MAX_CRITERION_LEN = 500
MIN_CRITERION_LEN = 3


class RubricDimension(BaseModel):
    key: str = Field(pattern=r"^[a-z][a-z0-9_]*$", min_length=2, max_length=40)
    criterion: str = Field(min_length=MIN_CRITERION_LEN, max_length=MAX_CRITERION_LEN)


class RubricValidationError(BaseModel):
    field: str
    message: str


class RubricValidationResult(BaseModel):
    valid: bool
    dimensions: list[str] = Field(default_factory=list)
    errors: list[RubricValidationError] = Field(default_factory=list)


def validate_rubric(rubric: dict[str, str]) -> RubricValidationResult:
    """Validate rubric keys and criterion strings."""
    errors: list[RubricValidationError] = []
    if not rubric:
        errors.append(
            RubricValidationError(field="rubric", message="must have at least one dimension")
        )
        return RubricValidationResult(valid=False, errors=errors)
    if len(rubric) > MAX_DIMENSIONS:
        errors.append(
            RubricValidationError(
                field="rubric",
                message=f"at most {MAX_DIMENSIONS} dimensions allowed",
            )
        )
    keys: list[str] = []
    for key, criterion in rubric.items():
        try:
            RubricDimension(key=key, criterion=criterion)
            keys.append(key)
        except ValidationError as exc:
            for err in exc.errors():
                loc = err.get("loc", ())
                field = key if not loc or loc[0] == "key" else f"{key}.{loc[-1]}"
                errors.append(RubricValidationError(field=str(field), message=err["msg"]))
    for msg in check_validation_rules(rubric):
        errors.append(RubricValidationError(field="rubric", message=msg))
    return RubricValidationResult(
        valid=len(errors) == 0,
        dimensions=keys if not errors else [],
        errors=errors,
    )
