"""Rubric template registry."""

from __future__ import annotations

from eval_rubric_api.examples_loader import list_example_names, load_example


def list_template_metadata() -> list[dict[str, str]]:
    """Return title and name for each bundled template."""
    out: list[dict[str, str]] = []
    for name in list_example_names():
        tpl = load_example(name)
        out.append(
            {
                "name": name,
                "title": str(tpl.get("title", name)),
                "description": str(tpl.get("description", "")),
            }
        )
    return out


def get_template_rubric(name: str) -> dict[str, str]:
    """Return rubric dimensions from a named template."""
    tpl = load_example(name)
    rubric = tpl.get("rubric")
    if not isinstance(rubric, dict):
        raise ValueError(f"template {name} has no rubric object")
    return {str(k): str(v) for k, v in rubric.items()}
