"""Extended rubric validation rules."""

from __future__ import annotations

RESERVED_KEYS = frozenset({"overall", "metadata", "version", "summary"})
DUPLICATE_CRITERIA_MIN_LEN = 10


def check_validation_rules(rubric: dict[str, str]) -> list[str]:
    """Return human-readable rule violations (schema checks run separately)."""
    errors: list[str] = []

    reserved = [k for k in rubric if k in RESERVED_KEYS]
    if reserved:
        errors.append(f"reserved dimension keys: {', '.join(sorted(reserved))}")

    seen: dict[str, str] = {}
    for key, criterion in rubric.items():
        norm = criterion.strip().lower()
        if len(norm) >= DUPLICATE_CRITERIA_MIN_LEN and norm in seen:
            errors.append(f"duplicate criterion text for {key} and {seen[norm]}")
        elif len(norm) >= DUPLICATE_CRITERIA_MIN_LEN:
            seen[norm] = key

    return errors
