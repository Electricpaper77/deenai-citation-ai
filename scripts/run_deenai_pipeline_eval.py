"""Run the DeenAI eval dataset through the pipeline stub.

This is rule-based pipeline contract validation only. It does not call a real
LLM, live APIs, vector stores, or religious content sources.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from deenai_pipeline_stub import DeenAIPipelineStub


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "evals" / "deenai_eval_prompts.jsonl"
DEFAULT_TRACE_OUTPUT = ROOT / "evals" / "pipeline_eval_traces.jsonl"
DEFAULT_SUMMARY_OUTPUT = ROOT / "evals" / "pipeline_eval_summary.json"

REQUIRED_FIELDS = {
    "id": str,
    "category": str,
    "user_question": str,
    "risk_level": str,
    "should_refuse": bool,
    "scholar_escalation_required": bool,
    "citation_required": bool,
    "should_answer": bool,
}


def load_eval_rows(path: Path) -> list[dict[str, Any]]:
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
            validate_eval_row(row, line_number)
            rows.append(row)
    return rows


def validate_eval_row(row: dict[str, Any], line_number: int) -> None:
    for field, expected_type in REQUIRED_FIELDS.items():
        if field not in row:
            raise ValueError(f"line {line_number}: missing required field {field!r}")
        if not isinstance(row[field], expected_type):
            raise ValueError(
                f"line {line_number}: field {field!r} must be {expected_type.__name__}"
            )


def evaluate_row(row: dict[str, Any], pipeline: DeenAIPipelineStub) -> dict[str, Any]:
    result = pipeline.process(row["user_question"])
    classification = result["classification"]
    retrieval = result["retrieval_packet"]
    citation = result["citation_verification"]
    guardrail = result["guardrail"]
    response = result["response_contract"]
    trace_log = result["trace_log"]

    predicted_risk_level = classification["risk_level"]
    predicted_should_answer = response["allowed_to_answer"]
    predicted_should_refuse = not predicted_should_answer
    predicted_scholar_escalation_required = classification["scholar_escalation_required"]
    predicted_citation_required = classification["citation_required"]

    checks = {
        "risk_level": (predicted_risk_level, row["risk_level"]),
        "should_refuse": (predicted_should_refuse, row["should_refuse"]),
        "scholar_escalation_required": (
            predicted_scholar_escalation_required,
            row["scholar_escalation_required"],
        ),
        "citation_required": (predicted_citation_required, row["citation_required"]),
        "should_answer": (predicted_should_answer, row["should_answer"]),
    }

    mismatch_reasons: list[str] = []
    for field, (predicted, expected) in checks.items():
        if predicted != expected:
            mismatch_reasons.append(f"{field}: predicted={predicted!r}, expected={expected!r}")

    return {
        "eval_id": row["id"],
        "category": row["category"],
        "user_question": row["user_question"],
        "expected_risk_level": row["risk_level"],
        "predicted_risk_level": predicted_risk_level,
        "expected_should_refuse": row["should_refuse"],
        "predicted_should_refuse": predicted_should_refuse,
        "expected_scholar_escalation_required": row["scholar_escalation_required"],
        "predicted_scholar_escalation_required": predicted_scholar_escalation_required,
        "expected_citation_required": row["citation_required"],
        "predicted_citation_required": predicted_citation_required,
        "expected_should_answer": row["should_answer"],
        "predicted_should_answer": predicted_should_answer,
        "guardrail_decision": guardrail["guardrail_decision"],
        "response_type": response["response_type"],
        "source_registry_ids": retrieval["source_registry_ids"],
        "verified_source_ids": citation["verified_source_ids"],
        "pass_fail": "pass" if not mismatch_reasons else "fail",
        "mismatch_reasons": mismatch_reasons,
        "notes": trace_log["notes"],
    }


def build_binary_matrix(rows: list[dict[str, Any]], expected_key: str, predicted_key: str) -> dict[str, int]:
    matrix = {
        "expected_true_actual_true": 0,
        "expected_true_actual_false": 0,
        "expected_false_actual_true": 0,
        "expected_false_actual_false": 0,
    }
    for row in rows:
        expected = bool(row[expected_key])
        predicted = bool(row[predicted_key])
        key = f"expected_{str(expected).lower()}_actual_{str(predicted).lower()}"
        matrix[key] += 1
    return matrix


def build_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    category_breakdown: dict[str, dict[str, int]] = defaultdict(
        lambda: {"total": 0, "passed": 0, "failed": 0}
    )
    risk_level_breakdown: dict[str, dict[str, int]] = defaultdict(
        lambda: {"total": 0, "passed": 0, "failed": 0}
    )
    guardrail_decision_breakdown: Counter[str] = Counter()
    mismatch_counter: Counter[str] = Counter()

    passed = 0
    for row in rows:
        is_pass = row["pass_fail"] == "pass"
        if is_pass:
            passed += 1

        category = row["category"]
        category_breakdown[category]["total"] += 1
        category_breakdown[category]["passed" if is_pass else "failed"] += 1

        risk = row["expected_risk_level"]
        risk_level_breakdown[risk]["total"] += 1
        risk_level_breakdown[risk]["passed" if is_pass else "failed"] += 1

        guardrail_decision_breakdown[row["guardrail_decision"]] += 1
        for reason in row["mismatch_reasons"]:
            mismatch_counter[reason] += 1

    total = len(rows)
    failed = total - passed
    return {
        "runner_type": "rule_based_pipeline_contract_validation",
        "production_ai_evaluation": False,
        "real_llm_called": False,
        "real_live_apis_called": False,
        "religious_content_generated": False,
        "total_prompts": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "category_breakdown": dict(sorted(category_breakdown.items())),
        "risk_level_breakdown": dict(sorted(risk_level_breakdown.items())),
        "guardrail_decision_breakdown": dict(sorted(guardrail_decision_breakdown.items())),
        "refusal_expected_vs_actual": build_binary_matrix(
            rows, "expected_should_refuse", "predicted_should_refuse"
        ),
        "escalation_expected_vs_actual": build_binary_matrix(
            rows,
            "expected_scholar_escalation_required",
            "predicted_scholar_escalation_required",
        ),
        "citation_required_expected_vs_actual": build_binary_matrix(
            rows, "expected_citation_required", "predicted_citation_required"
        ),
        "top_failure_modes": [
            {"reason": reason, "count": count}
            for reason, count in mismatch_counter.most_common(10)
        ],
    }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=True, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the 60-prompt DeenAI eval dataset through DeenAIPipelineStub."
    )
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--trace-output", type=Path, default=DEFAULT_TRACE_OUTPUT)
    parser.add_argument("--summary-output", type=Path, default=DEFAULT_SUMMARY_OUTPUT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    eval_rows = load_eval_rows(args.input)
    pipeline = DeenAIPipelineStub()
    trace_rows = [evaluate_row(row, pipeline) for row in eval_rows]
    summary = build_summary(trace_rows)

    write_jsonl(args.trace_output, trace_rows)
    write_json(args.summary_output, summary)

    print(
        "DeenAI pipeline eval complete: "
        f"{summary['passed']}/{summary['total_prompts']} passed "
        f"({summary['pass_rate']:.2%})."
    )
    print(f"Trace JSONL: {args.trace_output}")
    print(f"Summary JSON: {args.summary_output}")
    return 0 if summary["failed"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
