# Changelog

## 0.4.0 — 2026-02-11

- Added `score_with_metadata()` helper and `POST /score/inspect` for dimension count and answer-length metadata.
- Bumped API/package versioning to `0.4.0` and expanded scoring/API tests for inspect behavior.
- Updated docs to include inspect route usage alongside existing score, batch, and aggregation flows.

## 0.3.0 — 2025-07-06

- Rubric template registry with `GET /rubric/templates` and `GET /rubric/templates/{name}/rubric`.
- Score aggregation via `POST /score/aggregate` and summary stats in batch export.
- `POST /score/batch/export` returns indented JSON with optional summary block.
- Extended validation rules (reserved keys, duplicate criteria) integrated into `/rubric/validate`.
- Bundled `safety_review` template and expanded pytest coverage.

## 0.2.0 — 2025-06-14

- `POST /score/batch` for up to `BATCH_MAX_ITEMS` (default 50) answer/rubric pairs.
- Rubric schema validation via `POST /rubric/validate` and pre-check on score routes.
- Bundled example rubrics: `GET /rubric/examples` and `GET /rubric/examples/{name}`.
- `docs/RUBRIC.md`, expanded README, and GitHub Actions matrix (Python 3.11, 3.12).
- Expanded pytest coverage (schemas, batch, examples).

## 0.1.0 — 2024-11-11

- Initial FastAPI `/health` and `/score` with keyword-overlap heuristic.
- Docker and docker-compose for local deploy.
- GitHub Actions CI with pytest.
