"""Score aggregation helpers."""

from __future__ import annotations


def aggregate_batch_results(results: list[dict[str, object]]) -> dict[str, object]:
    """Summarize overall scores and dimension pass rates."""
    if not results:
        return {
            "count": 0,
            "mean": 0.0,
            "min": 0.0,
            "max": 0.0,
            "pass_rate": 0.0,
        }

    overalls: list[float] = []
    passed = 0
    total_dims = 0

    for result in results:
        overall = result.get("overall")
        if isinstance(overall, (int, float)):
            overalls.append(float(overall))
        dims = result.get("dimensions")
        if isinstance(dims, dict):
            for dim in dims.values():
                if isinstance(dim, dict):
                    total_dims += 1
                    if dim.get("passed") is True:
                        passed += 1

    mean = round(sum(overalls) / len(overalls), 2) if overalls else 0.0
    pass_rate = round(passed / total_dims, 2) if total_dims else 0.0

    return {
        "count": len(results),
        "mean": mean,
        "min": round(min(overalls), 2) if overalls else 0.0,
        "max": round(max(overalls), 2) if overalls else 0.0,
        "pass_rate": pass_rate,
    }
