"""Load bundled example rubrics."""

from __future__ import annotations

import json
from importlib import resources
from pathlib import Path

_EXAMPLES_PKG = "eval_rubric_api.examples"


def list_example_names() -> list[str]:
    root = resources.files(_EXAMPLES_PKG)
    return sorted(p.stem for p in root.iterdir() if p.suffix == ".json")


def load_example(name: str) -> dict[str, object]:
    path = resources.files(_EXAMPLES_PKG) / f"{name}.json"
    if not path.is_file():
        raise FileNotFoundError(name)
    return json.loads(path.read_text(encoding="utf-8"))
