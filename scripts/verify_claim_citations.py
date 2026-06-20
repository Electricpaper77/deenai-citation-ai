"""Verify DeenAI placeholder claim-to-citation mappings.

This script validates contract behavior only. It does not call live APIs,
invoke an LLM, load religious content, infer hadith grading, or render answers.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "sources" / "source_registry.json"
DEFAULT_CASES = ROOT / "evals" / "mock_claim_citation_cases.jsonl"
DEFAULT_REPORT = ROOT / "evals" / "claim_citation_verification_report.json"

CASE_REQUIRED_FIELDS = {
    "case_id",
    "eval_id",
    "user_question",
    "intent",
    "risk_level",
    "guardrail_decision",
    "allowed_to_answer",
    "citation_panel_present",
    "retrieved_source_ids",
    "placeholder_claims",
    "expected_verification_result",
    "expected_render_decision",
    "notes",
}

CLAIM_REQUIRED_FIELDS = {
    "claim_id",
    "claim_type",
    "claim_text_placeholder",
    "required_source_type",
    "mapped_source_registry_id",
    "citation_required",
    "support_status",
}

PROHIBITED_CONTENT_FIELDS = {
    "arabic",
    "quran_text",
    "hadith_text",
    "dua_text",
    "translation",
    "transliteration",
    "ruling_text",
}

HIGH_RISK_INTENT_MARKERS = (
    "fiqh",
    "divorce",
    "inheritance",
    "finance",
    "ruling",
    "invented_hadith",
    "fake_citation",
    "citation_bypass",
    "sectarian_bait",
    "sectarian_verdict",
    "source_missing",
)


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
                raise ValueError(f"{path}:{line_number}: each row must be an object")
            rows.append(row)
    return rows


def registry_index(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = registry.get("source_categories", [])
    if not isinstance(entries, list):
        raise ValueError("source_registry.json must contain source_categories as a list")
    return {
        entry["source_id"]: entry
        for entry in entries
        if isinstance(entry, dict) and isinstance(entry.get("source_id"), str)
    }


def find_prohibited_fields(value: Any, path: str = "$") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            nested_path = f"{path}.{key}"
            if key in PROHIBITED_CONTENT_FIELDS:
                found.append(nested_path)
            found.extend(find_prohibited_fields(nested, nested_path))
    elif isinstance(value, list):
        for index, item in enumerate(value):
            found.extend(find_prohibited_fields(item, f"{path}[{index}]"))
    return found


def high_risk_or_ruling_case(case: dict[str, Any]) -> bool:
    intent = str(case.get("intent", "")).lower()
    notes = " ".join(str(note).lower() for note in case.get("notes", []))
    if case.get("risk_level") == "blocked":
        return True
    return any(marker in intent or marker in notes for marker in HIGH_RISK_INTENT_MARKERS)


def normal_answer_rendered(case: dict[str, Any]) -> bool:
    return case.get("guardrail_decision") == "allow" and case.get("allowed_to_answer") is True


def verify_case(case: dict[str, Any], registry: dict[str, dict[str, Any]]) -> dict[str, Any]:
    case_id = str(case.get("case_id", "<missing_case_id>"))
    errors: list[str] = []
    missing_source_mappings: list[str] = []
    wrong_source_type_mappings: list[str] = []
    prohibited_fields = [f"{case_id}: {path}" for path in find_prohibited_fields(case)]
    unsupported_claims = 0
    supported_claims = 0

    missing_fields = sorted(field for field in CASE_REQUIRED_FIELDS if field not in case)
    if missing_fields:
        errors.append(f"{case_id}: missing case fields: {', '.join(missing_fields)}")

    retrieved_source_ids = case.get("retrieved_source_ids", [])
    if not isinstance(retrieved_source_ids, list):
        errors.append(f"{case_id}: retrieved_source_ids must be a list")
        retrieved_source_ids = []

    citation_required_any = False
    claims = case.get("placeholder_claims", [])
    if not isinstance(claims, list):
        errors.append(f"{case_id}: placeholder_claims must be a list")
        claims = []

    for claim in claims:
        if not isinstance(claim, dict):
            errors.append(f"{case_id}: placeholder claim must be an object")
            continue

        claim_id = str(claim.get("claim_id", "<missing_claim_id>"))
        missing_claim_fields = sorted(field for field in CLAIM_REQUIRED_FIELDS if field not in claim)
        if missing_claim_fields:
            errors.append(
                f"{case_id}/{claim_id}: missing claim fields: {', '.join(missing_claim_fields)}"
            )

        citation_required = claim.get("citation_required") is True
        citation_required_any = citation_required_any or citation_required
        mapped_source_id = claim.get("mapped_source_registry_id")

        if claim.get("support_status") == "supported":
            supported_claims += 1
        if claim.get("support_status") == "unsupported":
            unsupported_claims += 1
            errors.append(f"{case_id}/{claim_id}: unsupported claim blocks rendering")

        if citation_required and not mapped_source_id:
            missing_source_mappings.append(f"{case_id}/{claim_id}: missing mapped_source_registry_id")
            errors.append(f"{case_id}/{claim_id}: citation-required claim has no source mapping")
            continue

        if mapped_source_id is None:
            continue
        if not isinstance(mapped_source_id, str) or mapped_source_id not in registry:
            missing_source_mappings.append(f"{case_id}/{claim_id}: {mapped_source_id}")
            errors.append(f"{case_id}/{claim_id}: mapped source ID not found in registry")
            continue

        mapping_must_be_retrieved = (
            citation_required or claim.get("support_status") != "not_applicable"
        )
        if mapping_must_be_retrieved and mapped_source_id not in retrieved_source_ids:
            missing_source_mappings.append(
                f"{case_id}/{claim_id}: {mapped_source_id} not in retrieved_source_ids"
            )
            errors.append(f"{case_id}/{claim_id}: mapped source was not retrieved")

        required_source_type = claim.get("required_source_type")
        actual_source_type = registry[mapped_source_id].get("content_type")
        if required_source_type != actual_source_type:
            wrong_source_type_mappings.append(
                f"{case_id}/{claim_id}: required {required_source_type!r}, got {actual_source_type!r}"
            )
            errors.append(f"{case_id}/{claim_id}: wrong source type mapping")

    if (
        citation_required_any
        and case.get("guardrail_decision") == "allow"
        and case.get("citation_panel_present") is not True
    ):
        errors.append(f"{case_id}: citation panel missing while citation is required")

    if high_risk_or_ruling_case(case) and normal_answer_rendered(case):
        errors.append(f"{case_id}: high-risk or refusal-class case rendered as normal answer")

    if prohibited_fields:
        errors.extend(f"{item}: prohibited content field present" for item in prohibited_fields)

    actual_verification_result = "fail" if errors else "pass"
    if actual_verification_result == "fail":
        actual_render_decision = "block_render"
    elif case.get("guardrail_decision") == "refuse":
        actual_render_decision = "refuse"
    elif case.get("guardrail_decision") == "escalate":
        actual_render_decision = "escalate"
    elif case.get("allowed_to_answer") is True:
        actual_render_decision = "render_answer"
    else:
        actual_render_decision = "block_render"

    expected_verification_result = case.get("expected_verification_result")
    expected_render_decision = case.get("expected_render_decision")
    case_pass = (
        actual_verification_result == expected_verification_result
        and actual_render_decision == expected_render_decision
    )

    return {
        "case_id": case_id,
        "actual_verification_result": actual_verification_result,
        "expected_verification_result": expected_verification_result,
        "actual_render_decision": actual_render_decision,
        "expected_render_decision": expected_render_decision,
        "case_pass": case_pass,
        "errors": errors,
        "supported_claims": supported_claims,
        "unsupported_claims": unsupported_claims,
        "blocked_render": actual_render_decision in {"block_render", "refuse", "escalate"},
        "missing_source_mappings": missing_source_mappings,
        "wrong_source_type_mappings": wrong_source_type_mappings,
        "prohibited_content_fields_found": prohibited_fields,
    }


def build_report(case_results: list[dict[str, Any]], registry: dict[str, dict[str, Any]]) -> dict[str, Any]:
    total = len(case_results)
    passed = sum(1 for result in case_results if result["case_pass"])
    failed = total - passed

    missing_source_mappings = sorted(
        {
            item
            for result in case_results
            for item in result["missing_source_mappings"]
        }
    )
    wrong_source_type_mappings = sorted(
        {
            item
            for result in case_results
            for item in result["wrong_source_type_mappings"]
        }
    )
    prohibited_content_fields_found = sorted(
        {
            item
            for result in case_results
            for item in result["prohibited_content_fields_found"]
        }
    )

    warnings: list[str] = []
    high_risk_sources = sorted(
        source_id
        for source_id, entry in registry.items()
        if entry.get("risk_level") == "high"
    )
    if high_risk_sources:
        warnings.append(
            "High-risk registry sources still require licensing and permission review before real retrieval: "
            + ", ".join(high_risk_sources)
        )

    failed_case_reasons = Counter()
    for result in case_results:
        if not result["case_pass"]:
            failed_case_reasons.update(result["errors"] or ["unexpected expected/actual mismatch"])

    return {
        "verifier_type": "metadata_only_claim_citation_contract",
        "real_apis_called": False,
        "real_llm_called": False,
        "religious_content_loaded": False,
        "total_cases": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "supported_claims": sum(result["supported_claims"] for result in case_results),
        "unsupported_claims": sum(result["unsupported_claims"] for result in case_results),
        "blocked_render_cases": sum(1 for result in case_results if result["blocked_render"]),
        "missing_source_mappings": missing_source_mappings,
        "wrong_source_type_mappings": wrong_source_type_mappings,
        "prohibited_content_fields_found": prohibited_content_fields_found,
        "warnings": warnings,
        "case_results": case_results,
        "top_unexpected_failures": [
            {"reason": reason, "count": count}
            for reason, count in failed_case_reasons.most_common(10)
        ],
        "pass_fail": "pass" if failed == 0 else "fail",
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=True, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify DeenAI claim-to-citation cases.")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--cases", type=Path, default=DEFAULT_CASES)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry = registry_index(load_json(args.registry))
    cases = load_jsonl(args.cases)
    case_results = [verify_case(case, registry) for case in cases]
    report = build_report(case_results, registry)
    write_json(args.report_output, report)

    print(
        "Claim citation verification complete: "
        f"{report['passed']}/{report['total_cases']} passed "
        f"({report['pass_rate']:.2%})."
    )
    print(f"Report JSON: {args.report_output}")
    return 0 if report["pass_fail"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
