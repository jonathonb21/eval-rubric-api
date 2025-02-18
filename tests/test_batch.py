from eval_rubric_api.scoring import score_batch


def test_score_batch_preserves_order():
    items = [
        {
            "answer": "Redis cache-aside reduces read load on PostgreSQL.",
            "rubric": {"correctness": "Mentions cache-aside and database"},
        },
        {
            "answer": "Use plain words.",
            "rubric": {"clarity": "Plain language without jargon"},
        },
    ]
    results = score_batch(items)
    assert len(results) == 2
    assert "overall" in results[0]
    assert "overall" in results[1]


def test_score_batch_empty_rubric_raises():
    try:
        score_batch([{"answer": "text", "rubric": {}}])
        assert False, "expected ValueError"
    except ValueError:
        pass
