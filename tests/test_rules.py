from eval_rubric_api.rules import check_validation_rules
from eval_rubric_api.schemas import validate_rubric


def test_check_validation_rules_reserved_key():
    errors = check_validation_rules({"overall": "Some valid criterion text here"})
    assert any("reserved" in e for e in errors)


def test_check_validation_rules_duplicate_criteria():
    text = "Mentions cache-aside and database read patterns"
    errors = check_validation_rules(
        {"correctness": text, "completeness": text},
    )
    assert any("duplicate" in e for e in errors)


def test_validate_rubric_applies_rules():
    result = validate_rubric({"overall": "Some valid criterion text here"})
    assert result.valid is False
    assert any("reserved" in e.message for e in result.errors)
