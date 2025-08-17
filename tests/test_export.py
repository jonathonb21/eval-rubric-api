import json

from eval_rubric_api.export import export_batch_json


def test_export_batch_json_includes_summary():
    results = [{"overall": 0.5, "dimensions": {}}]
    raw = export_batch_json(results)
    payload = json.loads(raw)
    assert "results" in payload
    assert "summary" in payload
    assert payload["summary"]["count"] == 1


def test_export_batch_json_without_summary():
    results = [{"overall": 0.5, "dimensions": {}}]
    raw = export_batch_json(results, include_summary=False)
    payload = json.loads(raw)
    assert "results" in payload
    assert "summary" not in payload
