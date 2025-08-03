from eval_rubric_api.aggregation import aggregate_batch_results


def test_aggregate_batch_results_summary():
    results = [
        {"overall": 0.8, "dimensions": {"a": {"passed": True}}},
        {"overall": 0.6, "dimensions": {"b": {"passed": False}}},
    ]
    summary = aggregate_batch_results(results)
    assert summary["count"] == 2
    assert summary["mean"] == 0.7
    assert summary["min"] == 0.6
    assert summary["max"] == 0.8
    assert summary["pass_rate"] == 0.5


def test_aggregate_batch_results_empty():
    summary = aggregate_batch_results([])
    assert summary["count"] == 0
    assert summary["mean"] == 0.0
