"""Batch score export helpers."""

from __future__ import annotations

import json

from eval_rubric_api.aggregation import aggregate_batch_results


def export_batch_json(
    results: list[dict[str, object]],
    *,
    include_summary: bool = True,
) -> str:
    """Serialize batch score results to indented JSON."""
    payload: dict[str, object] = {"results": results}
    if include_summary:
        payload["summary"] = aggregate_batch_results(results)
    return json.dumps(payload, indent=2)
