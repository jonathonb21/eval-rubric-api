from fastapi.testclient import TestClient

from eval_rubric_api.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == "0.4.0"


def test_score_endpoint():
    response = client.post(
        "/score",
        json={
            "answer": "Redis cache-aside reduces read load on PostgreSQL.",
            "rubric": {"correctness": "Mentions cache-aside and database"},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "overall" in body
    assert "dimensions" in body


def test_score_rejects_invalid_rubric_key():
    response = client.post(
        "/score",
        json={"answer": "text", "rubric": {"Bad": "Some criterion text"}},
    )
    assert response.status_code == 422


def test_batch_score_endpoint():
    response = client.post(
        "/score/batch",
        json={
            "items": [
                {
                    "answer": "Redis cache-aside reduces read load on PostgreSQL.",
                    "rubric": {"correctness": "Mentions cache-aside and database"},
                },
                {
                    "answer": "Keep wording simple.",
                    "rubric": {"clarity": "Plain language without jargon"},
                },
            ]
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert len(body["results"]) == 2


def test_batch_export_endpoint():
    response = client.post(
        "/score/batch/export",
        json={
            "items": [
                {
                    "answer": "Redis cache-aside reduces read load on PostgreSQL.",
                    "rubric": {"correctness": "Mentions cache-aside and database"},
                },
            ]
        },
    )
    assert response.status_code == 200
    assert "summary" in response.text
    assert "results" in response.text


def test_score_aggregate_endpoint():
    response = client.post(
        "/score/aggregate",
        json={
            "results": [
                {"overall": 0.8, "dimensions": {"a": {"passed": True}}},
                {"overall": 0.6, "dimensions": {"b": {"passed": False}}},
            ]
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert body["mean"] == 0.7


def test_score_inspect_endpoint():
    response = client.post(
        "/score/inspect",
        json={
            "answer": "Redis cache-aside reduces read load on PostgreSQL.",
            "rubric": {"correctness": "Mentions cache-aside and database"},
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "metadata" in body
    assert body["metadata"]["dimensions_count"] == 1


def test_rubric_validate_endpoint():
    response = client.post(
        "/rubric/validate",
        json={"rubric": {"correctness": "Mentions cache-aside and database"}},
    )
    assert response.status_code == 200
    assert response.json()["valid"] is True


def test_rubric_templates_list():
    response = client.get("/rubric/templates")
    assert response.status_code == 200
    names = {t["name"] for t in response.json()["templates"]}
    assert "technical_qa" in names
    assert "safety_review" in names


def test_rubric_template_rubric():
    response = client.get("/rubric/templates/technical_qa/rubric")
    assert response.status_code == 200
    body = response.json()
    assert "correctness" in body


def test_rubric_examples_list():
    response = client.get("/rubric/examples")
    assert response.status_code == 200
    names = response.json()["examples"]
    assert "technical_qa" in names
    assert "code_review" in names


def test_rubric_example_by_name():
    response = client.get("/rubric/examples/technical_qa")
    assert response.status_code == 200
    body = response.json()
    assert "rubric" in body
    assert "title" in body
