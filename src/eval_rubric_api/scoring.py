"""Rubric scoring helpers."""

from __future__ import annotations

from eval_rubric_api.schemas import validate_rubric


def score_dimension(answer: str, criterion: str) -> dict[str, object]:
    """Heuristic score for one rubric dimension (demo implementation)."""
    answer_l = answer.lower()
    criterion_l = criterion.lower()
    tokens = [t for t in criterion_l.replace(",", " ").split() if len(t) > 3]
    hits = sum(1 for t in tokens if t in answer_l)
    ratio = hits / max(len(tokens), 1)
    passed = ratio >= 0.4
    return {
        "criterion": criterion,
        "passed": passed,
        "score": round(ratio, 2),
        "notes": "keyword overlap heuristic (replace with model or rules later)",
    }


def score_answer(answer: str, rubric: dict[str, str], *, validate: bool = True) -> dict[str, object]:
    if validate:
        result = validate_rubric(rubric)
        if not result.valid:
            raise ValueError(result.errors[0].message if result.errors else "invalid rubric")
    dimensions = {
        key: score_dimension(answer, criterion) for key, criterion in rubric.items()
    }
    scores = [
        d["score"] for d in dimensions.values() if isinstance(d["score"], (int, float))
    ]
    overall = round(sum(scores) / len(scores), 2) if scores else 0.0
    return {"overall": overall, "dimensions": dimensions}


def score_batch(
    items: list[dict[str, object]], *, validate: bool = True
) -> list[dict[str, object]]:
    """Score multiple answer/rubric pairs; preserves input order."""
    results: list[dict[str, object]] = []
    for item in items:
        answer = str(item.get("answer", ""))
        rubric = item.get("rubric")
        if not isinstance(rubric, dict):
            raise ValueError("each item must include a rubric object")
        rubric_str = {str(k): str(v) for k, v in rubric.items()}
        results.append(score_answer(answer, rubric_str, validate=validate))
    return results


def score_with_metadata(
    answer: str,
    rubric: dict[str, str],
    *,
    validate: bool = True,
) -> dict[str, object]:
    """Score once and attach lightweight metadata for API clients."""
    result = score_answer(answer, rubric, validate=validate)
    dimensions = result.get("dimensions")
    dim_count = len(dimensions) if isinstance(dimensions, dict) else 0
    return {
        **result,
        "metadata": {
            "dimensions_count": dim_count,
            "answer_length": len(answer),
        },
    }
