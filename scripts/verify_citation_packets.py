"""Verify DeenAI mock retrieval packets.

This verifier is metadata-only. It does not call live APIs, invoke an LLM,
load religious content, infer hadith grading, or produce religious rulings.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_REGISTRY = ROOT / "sources" / "source_registry.json"
DEFAULT_PACKETS = ROOT / "evals" / "mock_retrieval_packets.jsonl"
DEFAULT_REPORT = ROOT / "evals" / "citation_verification_report.json"

PACKET_REQUIRED_FIELDS = {
    "packet_id",
    "eval_id",
    "user_question",
    "intent",
    "risk_level",
    "source_registry_ids",
    "retrieved_sources",
    "citation_required",
    "retrieval_status",
    "allowed_to_generate",
    "notes",
}

SOURCE_REQUIRED_FIELDS = {
    "source_registry_id",
    "source_type",
    "provider",
    "source_url",
    "citation_fields",
    "content_available",
    "content_placeholder",
    "licensing_review_required",
    "allowed_use",
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

NO_GENERATION_INTENT_MARKERS = (
    "high_risk",
    "fiqh",
    "personal_fiqh",
    "invented_hadith",
    "fake_citation",
    "citation_bypass",
    "arabic_hallucination",
    "source_missing",
    "sectarian_bait",
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
                raise ValueError(f"{path}:{line_number}: row must be an object")
            rows.append(row)
    return rows


def registry_index(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    entries = registry.get("source_categories", [])
    if not isinstance(entries, list):
        raise ValueError("source_registry.json must contain source_categories as a list")
    index: dict[str, dict[str, Any]] = {}
    for entry in entries:
        if isinstance(entry, dict) and isinstance(entry.get("source_id"), str):
            index[entry["source_id"]] = entry
    return index


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


def no_generation_required(packet: dict[str, Any]) -> bool:
    intent = str(packet.get("intent", "")).lower()
    notes = " ".join(str(note).lower() for note in packet.get("notes", []))
    risk = packet.get("risk_level")
    if risk == "blocked":
        return True
    return any(marker in intent or marker in notes for marker in NO_GENERATION_INTENT_MARKERS)


def validate_packet(
    packet: dict[str, Any], registry: dict[str, dict[str, Any]]
) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
    missing_source_ids: list[str] = []
    invalid_source_metadata: list[str] = []
    unsafe_generation_flags: list[str] = []
    prohibited_content_fields_found: list[str] = []
    warnings: list[str] = []

    packet_id = str(packet.get("packet_id", "<missing_packet_id>"))

    missing_packet_fields = sorted(field for field in PACKET_REQUIRED_FIELDS if field not in packet)
    if missing_packet_fields:
        invalid_source_metadata.append(
            f"{packet_id}: missing packet fields: {', '.join(missing_packet_fields)}"
        )

    prohibited_content_fields_found.extend(
        f"{packet_id}: {field_path}" for field_path in find_prohibited_fields(packet)
    )

    source_ids = packet.get("source_registry_ids", [])
    if not isinstance(source_ids, list):
        invalid_source_metadata.append(f"{packet_id}: source_registry_ids must be a list")
        source_ids = []
    for source_id in source_ids:
        if source_id not in registry:
            missing_source_ids.append(f"{packet_id}: {source_id}")

    retrieved_sources = packet.get("retrieved_sources", [])
    if not isinstance(retrieved_sources, list):
        invalid_source_metadata.append(f"{packet_id}: retrieved_sources must be a list")
        retrieved_sources = []

    retrieved_ids: set[str] = set()
    for source in retrieved_sources:
        if not isinstance(source, dict):
            invalid_source_metadata.append(f"{packet_id}: retrieved source must be an object")
            continue

        missing_source_fields = sorted(field for field in SOURCE_REQUIRED_FIELDS if field not in source)
        if missing_source_fields:
            invalid_source_metadata.append(
                f"{packet_id}: retrieved source missing fields: {', '.join(missing_source_fields)}"
            )

        sid = source.get("source_registry_id")
        if not isinstance(sid, str) or sid not in registry:
            missing_source_ids.append(f"{packet_id}: {sid}")
            continue
        retrieved_ids.add(sid)

        reg = registry[sid]
        if source.get("source_type") != reg.get("content_type"):
            invalid_source_metadata.append(
                f"{packet_id}: {sid} source_type mismatch "
                f"({source.get('source_type')!r} != {reg.get('content_type')!r})"
            )
        if source.get("provider") != reg.get("provider"):
            invalid_source_metadata.append(
                f"{packet_id}: {sid} provider mismatch "
                f"({source.get('provider')!r} != {reg.get('provider')!r})"
            )
        if source.get("source_url") != reg.get("url"):
            invalid_source_metadata.append(
                f"{packet_id}: {sid} source_url mismatch "
                f"({source.get('source_url')!r} != {reg.get('url')!r})"
            )
        if source.get("content_available") is not False:
            invalid_source_metadata.append(f"{packet_id}: {sid} content_available must be false")
        if source.get("content_placeholder") is not True:
            invalid_source_metadata.append(f"{packet_id}: {sid} content_placeholder must be true")

        citation_fields = source.get("citation_fields")
        if packet.get("citation_required") is True and (
            not isinstance(citation_fields, list) or not citation_fields
        ):
            invalid_source_metadata.append(
                f"{packet_id}: {sid} citation_required packet must include citation_fields"
            )

    for source_id in source_ids:
        if source_id not in retrieved_ids and source_id in registry and packet.get("retrieval_status") != "source_missing":
            warnings.append(f"{packet_id}: {source_id} listed in source_registry_ids but not retrieved_sources")

    if packet.get("citation_required") is True and not retrieved_sources:
        invalid_source_metadata.append(f"{packet_id}: citation_required packet has no retrieved_sources")

    if no_generation_required(packet) and packet.get("allowed_to_generate") is not False:
        unsafe_generation_flags.append(
            f"{packet_id}: {packet.get('intent')} must not allow generation"
        )

    return (
        missing_source_ids,
        invalid_source_metadata,
        unsafe_generation_flags,
        prohibited_content_fields_found,
        warnings,
    )


def build_report(registry: dict[str, dict[str, Any]], packets: list[dict[str, Any]]) -> dict[str, Any]:
    missing_source_ids: list[str] = []
    invalid_source_metadata: list[str] = []
    unsafe_generation_flags: list[str] = []
    prohibited_content_fields_found: list[str] = []
    warnings: list[str] = []
    passed = 0

    for packet in packets:
        before = (
            len(missing_source_ids),
            len(invalid_source_metadata),
            len(unsafe_generation_flags),
            len(prohibited_content_fields_found),
        )
        (
            packet_missing_ids,
            packet_invalid_metadata,
            packet_unsafe_flags,
            packet_prohibited_fields,
            packet_warnings,
        ) = validate_packet(packet, registry)
        missing_source_ids.extend(packet_missing_ids)
        invalid_source_metadata.extend(packet_invalid_metadata)
        unsafe_generation_flags.extend(packet_unsafe_flags)
        prohibited_content_fields_found.extend(packet_prohibited_fields)
        warnings.extend(packet_warnings)
        after = (
            len(missing_source_ids),
            len(invalid_source_metadata),
            len(unsafe_generation_flags),
            len(prohibited_content_fields_found),
        )
        if before == after:
            passed += 1

    total = len(packets)
    failed = total - passed
    pass_fail = "pass" if failed == 0 else "fail"

    if any(entry.get("risk_level") == "high" for entry in registry.values()):
        warnings.append(
            "High-risk registry sources still require field-level licensing and permission review before real retrieval."
        )

    return {
        "verifier_type": "metadata_only_citation_packet_contract",
        "real_apis_called": False,
        "real_llm_called": False,
        "religious_content_loaded": False,
        "total_packets": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / total, 4) if total else 0.0,
        "missing_source_ids": sorted(set(missing_source_ids)),
        "invalid_source_metadata": sorted(set(invalid_source_metadata)),
        "unsafe_generation_flags": sorted(set(unsafe_generation_flags)),
        "prohibited_content_fields_found": sorted(set(prohibited_content_fields_found)),
        "warnings": sorted(set(warnings)),
        "pass_fail": pass_fail,
    }


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        json.dump(value, handle, ensure_ascii=True, indent=2, sort_keys=True)
        handle.write("\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify DeenAI mock citation packets.")
    parser.add_argument("--registry", type=Path, default=DEFAULT_REGISTRY)
    parser.add_argument("--packets", type=Path, default=DEFAULT_PACKETS)
    parser.add_argument("--report-output", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    registry = registry_index(load_json(args.registry))
    packets = load_jsonl(args.packets)
    report = build_report(registry, packets)
    write_json(args.report_output, report)

    print(
        "Citation packet verification complete: "
        f"{report['passed']}/{report['total_packets']} passed "
        f"({report['pass_rate']:.2%})."
    )
    print(f"Report JSON: {args.report_output}")
    return 0 if report["pass_fail"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
