import pytest

from eval_rubric_api.scoring import score_answer


@pytest.fixture
def sample_rubric() -> dict[str, str]:
    return {
        "correctness": "Mentions cache-aside and database",
        "clarity": "Plain language",
    }


@pytest.fixture
def sample_answer() -> str:
    return "Redis cache-aside reduces read load on PostgreSQL."


@pytest.fixture
def sample_score(sample_answer: str, sample_rubric: dict[str, str]) -> dict[str, object]:
    return score_answer(sample_answer, sample_rubric)
