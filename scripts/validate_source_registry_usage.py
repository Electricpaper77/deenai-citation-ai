"""Validate DeenAI pipeline source IDs against the source registry.

This script is metadata-only. It does not call APIs, retrieve religious source
content, infer authenticity, or validate theological correctness.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "sources" / "source_registry.json"
DEFAULT_TRACES = ROOT / "evals" / "pipeline_eval_traces.jsonl"
DEFAULT_REPORT = ROOT / "evals" / "source_registry_validation_report.json"

REQUIRED_ENTRY_FIELDS = {
    "source_id",
    "content_type",
    "provider",
    "url",
    "storage_policy",
    "citation_required_fields",
    "allowed_use",
    "restricted_use",
    "risk_level",
    "notes",
}

VALID_RISK_LEVELS = {"low", "medium", "high"}
CITATION_REQUIRED_CONTENT_TYPES = {"quran", "hadith", "dua", "prayer time"}

# These patterns are intentionally conservative. They check for positive claims
# in allowed-use/notes fields, while restricted_use can contain prohibited items.
PROHIBITED_CLAIM_PATTERNS = {
    "scholar_approval": [
        "scholar approved",
        "scholar-approved",
        "approved by scholars",
        "verified by scholars",
    ],
    "fatwa_capability": [
        "fatwa capability",
        "can issue fatwas",
        "issues fatwas",
        "religious ruling engine",
    ],
    "inferred_hadith_grading": [
        "infer hadith grade",
        "infer hadith grading",
        "model can grade hadith",
        "auto-grade hadith",
    ],
    "unrestricted_copied_religious_text_usage": [
        "unrestricted copied religious text",
        "unrestricted copying",
        "copy any religious text",
        "republish any religious text",
        "store any religious text",
    ],
}


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_number}: invalid JSONL: {exc}") from exc
            if not isinstance(row, dict):
                raise ValueError(f"{path}:{line_number}: each JSONL row must be an object")
            rows.append(row)
    return rows


def entry_id(entry: dict[str, Any]) -> str:
    value = entry.get("source_id") or entry.get("id")
    return value if isinstance(value, str) else "<missing_source_id>"


def flatten_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(flatten_text(item) for item in value)
    if isinstance(value, dict):
        return " ".join(flatten_text(item) for item in value.values())
    return ""


def extract_referenced_source_ids(trace_rows: list[dict[str, Any]]) -> list[str]:
    referenced: set[str] = set()
    for row in trace_rows:
        for field in ("source_registry_ids", "verified_source_ids"):
            values = row.get(field, [])
            if isinstance(values, list):
                referenced.update(value for value in values if isinstance(value, str))
    return sorted(referenced)


def validate_entry(entry: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    sid = entry_id(entry)

    missing = sorted(field for field in REQUIRED_ENTRY_FIELDS if field not in entry)
    if missing:
        problems.append(f"{sid}: missing required fields: {', '.join(missing)}")

    risk = entry.get("risk_level")
    if risk not in VALID_RISK_LEVELS:
        problems.append(f"{sid}: risk_level must be one of {sorted(VALID_RISK_LEVELS)}")

    citation_fields = entry.get("citation_required_fields")
    content_type = str(entry.get("content_type", "")).lower()
    if any(marker in content_type for marker in CITATION_REQUIRED_CONTENT_TYPES):
        if not isinstance(citation_fields, list) or not citation_fields:
            problems.append(
                f"{sid}: citation_required_fields must be non-empty for {entry.get('content_type')}"
            )

    claim_surface = " ".join(
        [
            flatten_text(entry.get("allowed_use", "")),
            flatten_text(entry.get("notes", "")),
            flatten_text(entry.get("provider", "")),
            flatten_text(entry.get("content_type", "")),
        ]
    ).lower()
    for label, patterns in PROHIBITED_CLAIM_PATTERNS.items():
        for pattern in patterns:
            if pattern in claim_surface:
                problems.append(f"{sid}: prohibited claim detected: {label} ({pattern})")

    return problems


def build_report(registry: dict[str, Any], trace_rows: list[dict[str, Any]]) -> dict[str, Any]:
    entries = registry.get("source_categories", [])
    if not isinstance(entries, list):
        raise ValueError("source_registry.json must contain source_categories as a list")

    registry_by_id = {
        entry_id(entry): entry
        for entry in entries
        if isinstance(entry, dict) and entry_id(entry) != "<missing_source_id>"
    }
    referenced_ids = extract_referenced_source_ids(trace_rows)

    missing_refs = [sid for sid in referenced_ids if sid not in registry_by_id]
    valid_refs = [sid for sid in referenced_ids if sid in registry_by_id]

    invalid_entries: list[str] = []
    for entry in entries:
        if not isinstance(entry, dict):
            invalid_entries.append("registry entry is not an object")
            continue
        invalid_entries.extend(validate_entry(entry))

    warnings: list[str] = []
    high_risk = sorted(
        entry_id(entry)
        for entry in entries
        if isinstance(entry, dict) and entry.get("risk_level") == "high"
    )
    if high_risk:
        warnings.append(
            "High-risk source entries require field-level licensing and permission review: "
            + ", ".join(high_risk)
        )

    if not referenced_ids:
        warnings.append(
            "No source IDs were found in pipeline traces; ensure traces include source_registry_ids or verified_source_ids."
        )

    pass_fail = "pass" if not missing_refs and not invalid_entries else "fail"

    return {
        "validator_type": "source_registry_usage_contract",
        "real_apis_called": False,
        "religious_content_loaded": False,
        "total_registry_entries": len(entries),
        "total_source_ids_referenced_by_pipeline": len(referenced_ids),
        "valid_source_references": valid_refs,
        "missing_source_references": missing_refs,
        "invalid_registry_entries": invalid_entries,
        "warnings": warnings,
        "pass_fail": pass_fail,
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=True, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate source registry usage in DeenAI pipeline traces."
    )
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--traces", type=Path, default=DEFAULT_TRACES)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry = load_json(args.registry)
    trace_rows = load_jsonl(args.traces)
    report = build_report(registry, trace_rows)
    write_json(args.report_output, report)

    print(
        "Source registry validation complete: "
        f"{report['pass_fail']} "
        f"({len(report['valid_source_references'])}/"
        f"{report['total_source_ids_referenced_by_pipeline']} referenced IDs valid)."
    )
    print(f"Report JSON: {args.report_output}")
    return 0 if report["pass_fail"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
