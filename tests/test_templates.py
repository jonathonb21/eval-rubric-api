from eval_rubric_api.templates import get_template_rubric, list_template_metadata


def test_list_template_metadata_includes_bundled():
    templates = list_template_metadata()
    names = {t["name"] for t in templates}
    assert "technical_qa" in names
    assert "code_review" in names
    assert "safety_review" in names


def test_get_template_rubric_returns_dimensions():
    rubric = get_template_rubric("technical_qa")
    assert "correctness" in rubric
    assert len(rubric["correctness"]) >= 3


def test_get_template_rubric_unknown_raises():
    try:
        get_template_rubric("missing_template")
        assert False, "expected FileNotFoundError"
    except FileNotFoundError:
        pass
