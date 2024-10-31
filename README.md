# eval-rubric-api

**FastAPI** service that scores free-text answers against JSON rubrics (correctness, completeness, clarity). Supports single and batch scoring, rubric validation, templates, aggregation, inspect metadata, batch export, and bundled example rubrics.

## Inspired by

Ideas from technical evaluation workflows and self-hosted API projects (structured rubrics, FastAPI services, Dockerized dev). This is **not** a fork of any upstream repo.

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate   # Windows
pip install -e ".[dev]"
cp .env.example .env
uvicorn eval_rubric_api.main:app --reload
```

### Single score

`POST /score`:

```json
{
  "answer": "Redis cache-aside reduces read load on PostgreSQL.",
  "rubric": {
    "correctness": "Mentions cache-aside and database",
    "completeness": "Explains benefit",
    "clarity": "Plain language"
  }
}
```

### Batch score and export

- `POST /score/batch` — score many answer/rubric pairs
- `POST /score/batch/export` — same input, returns indented JSON with summary stats
- `POST /score/aggregate` — summarize existing score results (mean, min, max, pass rate)
- `POST /score/inspect` — single score plus metadata (`dimensions_count`, `answer_length`)

### Rubric helpers

- `POST /rubric/validate` — check keys, criteria, and extended rules without scoring
- `GET /rubric/templates` — list bundled rubric templates with titles
- `GET /rubric/templates/technical_qa/rubric` — fetch rubric dimensions from a template
- `GET /rubric/examples` — list bundled templates (legacy alias)
- `GET /rubric/examples/technical_qa` — fetch full template JSON

See [docs/RUBRIC.md](docs/RUBRIC.md) for the rubric schema and validation rules.

## Docker

```bash
docker compose up --build
```

## Tests

```bash
pytest
```

## License

MIT
