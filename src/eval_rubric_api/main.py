"""FastAPI entrypoint."""

from __future__ import annotations

import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel, Field

from eval_rubric_api.aggregation import aggregate_batch_results
from eval_rubric_api.examples_loader import list_example_names, load_example
from eval_rubric_api.export import export_batch_json
from eval_rubric_api.schemas import RubricValidationResult, validate_rubric
from eval_rubric_api.scoring import score_answer, score_batch, score_with_metadata
from eval_rubric_api.templates import get_template_rubric, list_template_metadata

app = FastAPI(title="eval-rubric-api", version="0.4.0")

BATCH_MAX_ITEMS = int(os.environ.get("BATCH_MAX_ITEMS", "50"))


class ScoreRequest(BaseModel):
    answer: str = Field(min_length=1)
    rubric: dict[str, str] = Field(min_length=1)


class BatchScoreItem(BaseModel):
    answer: str = Field(min_length=1)
    rubric: dict[str, str] = Field(min_length=1)


class BatchScoreRequest(BaseModel):
    items: list[BatchScoreItem] = Field(min_length=1)


class ValidateRubricRequest(BaseModel):
    rubric: dict[str, str]


class AggregateRequest(BaseModel):
    results: list[dict[str, object]] = Field(min_length=1)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.4.0"}


@app.post("/score")
def score(payload: ScoreRequest) -> dict[str, object]:
    validation = validate_rubric(payload.rubric)
    if not validation.valid:
        raise HTTPException(status_code=422, detail=validation.model_dump())
    return score_answer(payload.answer, payload.rubric, validate=False)


@app.post("/score/batch")
def score_batch_endpoint(payload: BatchScoreRequest) -> dict[str, object]:
    if len(payload.items) > BATCH_MAX_ITEMS:
        raise HTTPException(
            status_code=413,
            detail=f"batch limited to {BATCH_MAX_ITEMS} items",
        )
    for idx, item in enumerate(payload.items):
        validation = validate_rubric(item.rubric)
        if not validation.valid:
            raise HTTPException(
                status_code=422,
                detail={"index": idx, "validation": validation.model_dump()},
            )
    raw = [{"answer": i.answer, "rubric": i.rubric} for i in payload.items]
    scores = score_batch(raw, validate=False)
    return {"count": len(scores), "results": scores}


@app.post("/score/batch/export", response_class=PlainTextResponse)
def score_batch_export(payload: BatchScoreRequest) -> PlainTextResponse:
    if len(payload.items) > BATCH_MAX_ITEMS:
        raise HTTPException(
            status_code=413,
            detail=f"batch limited to {BATCH_MAX_ITEMS} items",
        )
    for idx, item in enumerate(payload.items):
        validation = validate_rubric(item.rubric)
        if not validation.valid:
            raise HTTPException(
                status_code=422,
                detail={"index": idx, "validation": validation.model_dump()},
            )
    raw = [{"answer": i.answer, "rubric": i.rubric} for i in payload.items]
    scores = score_batch(raw, validate=False)
    body = export_batch_json(scores)
    return PlainTextResponse(content=body, media_type="application/json")


@app.post("/score/aggregate")
def score_aggregate(payload: AggregateRequest) -> dict[str, object]:
    return aggregate_batch_results(payload.results)


@app.post("/score/inspect")
def score_inspect(payload: ScoreRequest) -> dict[str, object]:
    validation = validate_rubric(payload.rubric)
    if not validation.valid:
        raise HTTPException(status_code=422, detail=validation.model_dump())
    return score_with_metadata(payload.answer, payload.rubric, validate=False)


@app.post("/rubric/validate", response_model=RubricValidationResult)
def rubric_validate(payload: ValidateRubricRequest) -> RubricValidationResult:
    return validate_rubric(payload.rubric)


@app.get("/rubric/templates")
def rubric_templates() -> dict[str, list[dict[str, str]]]:
    return {"templates": list_template_metadata()}


@app.get("/rubric/templates/{name}/rubric")
def rubric_template_rubric(name: str) -> dict[str, str]:
    try:
        return get_template_rubric(name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"unknown template: {exc.args[0]}") from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.get("/rubric/examples")
def rubric_examples() -> dict[str, list[str]]:
    return {"examples": list_example_names()}


@app.get("/rubric/examples/{name}")
def rubric_example(name: str) -> dict[str, object]:
    try:
        return load_example(name)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"unknown example: {exc.args[0]}") from exc
