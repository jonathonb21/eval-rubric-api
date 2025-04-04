# Rubric format

Each rubric is a JSON object mapping **dimension keys** to **criterion strings**.

## Rules

| Field | Constraint |
|-------|------------|
| Keys | Lowercase snake_case (`correctness`, `tone`, `actionable`) |
| Criteria | 3–500 characters describing what a good answer should satisfy |
| Count | 1–20 dimensions per rubric |
| Reserved keys | `overall`, `metadata`, `version`, and `summary` are rejected |
| Duplicate criteria | Identical criterion text across dimensions is rejected |

## Validate before scoring

```bash
curl -s -X POST http://127.0.0.1:8000/rubric/validate \
  -H "Content-Type: application/json" \
  -d '{"rubric":{"correctness":"Mentions cache-aside and database"}}'
```

## Templates

```bash
curl -s http://127.0.0.1:8000/rubric/templates
curl -s http://127.0.0.1:8000/rubric/templates/technical_qa/rubric
```

Legacy example routes remain available:

```bash
curl -s http://127.0.0.1:8000/rubric/examples
curl -s http://127.0.0.1:8000/rubric/examples/technical_qa
```

## Batch scoring and export

```bash
curl -s -X POST http://127.0.0.1:8000/score/batch \
  -H "Content-Type: application/json" \
  -d '{"items":[{"answer":"...","rubric":{"clarity":"Plain language"}}]}'

curl -s -X POST http://127.0.0.1:8000/score/batch/export \
  -H "Content-Type: application/json" \
  -d '{"items":[{"answer":"...","rubric":{"clarity":"Plain language"}}]}'
```

## Aggregation

```bash
curl -s -X POST http://127.0.0.1:8000/score/aggregate \
  -H "Content-Type: application/json" \
  -d '{"results":[{"overall":0.8,"dimensions":{"a":{"passed":true}}}]}'
```

## Inspect metadata

```bash
curl -s -X POST http://127.0.0.1:8000/score/inspect \
  -H "Content-Type: application/json" \
  -d '{"answer":"Redis cache-aside reduces read load","rubric":{"correctness":"Mentions cache-aside"}}'
```

`/score/inspect` returns normal score output plus a `metadata` object with:

- `dimensions_count` number of rubric dimensions scored
- `answer_length` source answer character count

Set `BATCH_MAX_ITEMS` in the environment to raise or lower the batch cap (default 50).
