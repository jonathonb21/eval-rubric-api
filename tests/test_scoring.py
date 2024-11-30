from eval_rubric_api.scoring import score_answer, score_dimension, score_with_metadata


def test_score_dimension_passes_when_keywords_present():
    result = score_dimension(
        "We use Redis cache-aside in front of the PostgreSQL database.",
        "Mentions cache-aside and database",
    )
    assert result["passed"] is True
    assert result["score"] >= 0.4


def test_score_answer_returns_overall():
    result = score_answer(
        "Redis cache-aside reduces read load on PostgreSQL.",
        {
            "correctness": "Mentions cache-aside and database",
            "clarity": "Plain language",
        },
    )
    assert "overall" in result
    assert len(result["dimensions"]) == 2


def test_score_answer_rejects_invalid_rubric():
    try:
        score_answer("answer", {})
        assert False, "expected ValueError"
    except ValueError:
        pass


def test_score_with_metadata_adds_dimensions_count():
    result = score_with_metadata(
        "Redis cache-aside reduces read load on PostgreSQL.",
        {"correctness": "Mentions cache-aside and database"},
    )
    assert result["metadata"]["dimensions_count"] == 1
    assert result["metadata"]["answer_length"] > 0
