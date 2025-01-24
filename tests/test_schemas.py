from eval_rubric_api.schemas import validate_rubric


def test_validate_rubric_accepts_valid_keys():
    result = validate_rubric({"correctness": "Mentions cache-aside and database"})
    assert result.valid is True
    assert result.dimensions == ["correctness"]


def test_validate_rubric_rejects_empty():
    result = validate_rubric({})
    assert result.valid is False
    assert any(e.field == "rubric" for e in result.errors)


def test_validate_rubric_rejects_bad_key():
    result = validate_rubric({"Bad-Key": "Some criterion text here"})
    assert result.valid is False


def test_validate_rubric_rejects_short_criterion():
    result = validate_rubric({"clarity": "hi"})
    assert result.valid is False
