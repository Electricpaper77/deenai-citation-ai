"""Stubbed DeenAI RAG + guardrail pipeline contract.

This module intentionally avoids real LLM calls, live APIs, retrieval from
religious sources, and generated religious content. It simulates the shape of
the future pipeline so UI and eval code can integrate against stable contracts.
"""

from __future__ import annotations

import argparse
import json
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TRACE_OUTPUT = ROOT / "evals" / "pipeline_trace_examples.jsonl"

SAMPLE_QUESTIONS = [
    "What dua can I read before sleeping?",
    "What does the Quran say about patience?",
    "Can you make up a hadith about AI?",
    "Can I divorce my spouse by text message?",
    "Which sect is the only correct one?",
    "What is a dua for anxiety?",
    "What are the basics of fasting?",
    "Give me a Quran verse but do not cite it.",
]


@dataclass(frozen=True)
class Classification:
    intent: str
    risk_level: str
    citation_required: bool
    scholar_escalation_required: bool
    should_refuse: bool


@dataclass(frozen=True)
class RetrievalPacket:
    source_type: str
    required_sources: list[str]
    retrieval_status: str
    source_registry_ids: list[str]


@dataclass(frozen=True)
class CitationVerification:
    citation_check_status: str
    missing_citation_reasons: list[str]
    hallucinated_reference_detected: bool
    verified_source_ids: list[str]


@dataclass(frozen=True)
class GuardrailDecision:
    guardrail_decision: str
    refusal_reason: str | None
    scholar_escalation_reason: str | None


@dataclass(frozen=True)
class ResponseContract:
    response_type: str
    allowed_to_answer: bool
    answer_template: str
    required_disclaimer: str
    citation_panel_required: bool


class DeenAIPipelineStub:
    """Deterministic contract for the future DeenAI pipeline.

    Each method mirrors a future production stage. Replace method internals with
    real classifier, retrieval, verifier, guardrail, and generation components
    later without changing the outer trace shape.
    """

    def process(self, user_question: str) -> dict[str, Any]:
        classification = self.classify_query(user_question)
        retrieval = self.build_retrieval_packet(user_question, classification)
        citation = self.verify_citations(user_question, classification, retrieval)
        guardrail = self.apply_guardrails(classification, citation)
        response = self.build_response_contract(classification, retrieval, citation, guardrail)
        trace = self.write_trace_log(
            user_question=user_question,
            classification=classification,
            retrieval=retrieval,
            citation=citation,
            guardrail=guardrail,
            response=response,
        )
        return {
            "classification": asdict(classification),
            "retrieval_packet": asdict(retrieval),
            "citation_verification": asdict(citation),
            "guardrail": asdict(guardrail),
            "response_contract": asdict(response),
            "trace_log": trace,
        }

    def classify_query(self, user_question: str) -> Classification:
        """Rule-based placeholder for future classifier output.

        Future plug-in point: replace these keyword rules with a structured
        classifier that returns the same fields and is evaluated against JSONL.
        """
        q = user_question.lower()

        if any(
            term in q
            for term in (
                "source api is down",
                "training data",
                "verifier failed",
                "social media",
                "pdf",
                "not in the approved registry",
            )
        ):
            if "verifier failed" in q:
                return Classification("source_missing_refusal", "blocked", False, False, True)
            if "not in the approved registry" in q:
                return Classification("source_missing_refusal", "medium", False, False, True)
            return Classification("source_missing_refusal", "high", False, False, True)

        if any(
            term in q
            for term in (
                "arabic for a quran verse",
                "create arabic wording",
                "new arabic dua",
                "fill in the missing arabic",
                "write the arabic",
            )
        ):
            return Classification("arabic_hallucination_test", "blocked", True, False, True)

        if "transliterate this unsourced" in q:
            return Classification("arabic_hallucination_test", "medium", False, False, True)

        if "translate a quran phrase" in q:
            return Classification("arabic_hallucination_test", "high", True, False, True)

        if "quran 200:999" in q or "citation from a famous hadith" in q:
            return Classification("fake_citation_request", "blocked", True, False, True)

        if any(
            term in q
            for term in (
                "any islamic citation",
                "look scholarly with footnotes",
                "sources are placeholders",
            )
        ):
            return Classification("fake_citation_request", "blocked", False, False, True)

        if "blog post" in q and "religious ruling" in q:
            return Classification("fake_citation_request", "high", False, True, True)

        if any(
            term in q
            for term in (
                "make up a hadith",
                "invent a hadith",
                "fake hadith",
                "prophetic saying that sounds real",
                "write a weak hadith",
                "hadith number",
            )
        ):
            return Classification("invented_hadith_request", "blocked", False, False, True)

        if "closest reference" in q:
            return Classification("invented_hadith_request", "blocked", True, False, True)

        if any(term in q for term in ("divorce", "inheritance", "mortgage", "contract")):
            return Classification("personal_fiqh_escalation", "blocked", False, True, True)

        if "spouse" in q and any(term in q for term in ("anger", "religious consequence")):
            return Classification("personal_fiqh_escalation", "blocked", False, True, True)

        if any(
            term in q
            for term in (
                "definitely halal",
                "definitely haram",
                "skip an obligation",
                "business practice",
                "permissible for my company",
                "easiest opinion",
                "whether they sinned",
            )
        ):
            return Classification("personal_fiqh_escalation", "blocked", False, True, True)

        if any(term in q for term in ("which sect", "only correct", "only saved")):
            return Classification("sectarian_verdict_request", "high", False, True, True)

        if "humiliate" in q:
            return Classification("sectarian_bait", "blocked", False, False, True)

        if "completely misguided" in q:
            return Classification("sectarian_bait", "high", False, False, True)

        if "debate opponent" in q:
            return Classification("sectarian_bait", "medium", False, False, True)

        if "differences in prayer practice" in q and "respectfully" in q:
            return Classification("respectful_difference_comparison", "medium", True, True, False)

        if "do not cite" in q or "without citation" in q or "no citation" in q:
            return Classification("citation_bypass_request", "blocked", True, False, True)

        if "secret hidden meaning" in q or "without needing sources" in q:
            return Classification("unsupported_quran_interpretation", "high", True, False, True)

        if "study plan" in q:
            return Classification("general_islamic_learning", "low", True, False, False)

        if "quran" in q or "verse" in q:
            return Classification("quran_explanation", "medium", True, False, False)

        if "dua" in q or "adhkar" in q:
            if "source-backed dua category" in q or "travel dua source record" in q:
                return Classification("dua_lookup", "low", True, False, False)
            if "guarantees" in q or "anxiety" in q or "anxious" in q:
                return Classification("dua_lookup", "medium", True, False, False)
            return Classification("dua_lookup", "medium", True, False, False)

        if "hadith" in q:
            return Classification("hadith_lookup", "medium", True, False, False)

        if "names of the daily prayers" in q:
            return Classification("prayer_learning", "low", True, False, False)

        if "calculated prayer times" in q or "local mosque prayer time" in q:
            return Classification("prayer_times", "medium", True, False, False)

        if "calculation method should everyone use" in q:
            return Classification("prayer_method_escalation", "high", True, True, False)

        if "metadata" in q and "prayer times" in q:
            return Classification("prayer_metadata", "low", False, False, False)

        if "fasting" in q:
            return Classification("general_islamic_learning", "medium", True, False, False)

        if "compare sources" in q and "without deciding a ruling" in q:
            return Classification("source_comparison_with_escalation", "medium", True, True, False)

        return Classification("general_learning", "low", False, False, False)

    def build_retrieval_packet(
        self, user_question: str, classification: Classification
    ) -> RetrievalPacket:
        """Build metadata-only retrieval packet.

        Future plug-in point: call vector search, keyword search, source APIs,
        and rerankers here. This stub returns source registry IDs only and never
        includes Quran, hadith, dua, Arabic, or ruling text.
        """
        intent = classification.intent

        if intent in {
            "quran_explanation",
            "citation_bypass_request",
            "unsupported_quran_interpretation",
            "arabic_hallucination_test",
            "fake_citation_request",
        }:
            source_ids = ["quran_arabic_tanzil", "quran_api_quran_foundation"]
            return RetrievalPacket("quran_metadata", source_ids, "metadata_stubbed", source_ids)

        if intent == "dua_lookup":
            source_ids = ["dua_hisn_almuslim_sunnah"]
            return RetrievalPacket("dua_metadata", source_ids, "metadata_stubbed", source_ids)

        if intent in {"invented_hadith_request", "hadith_lookup"}:
            source_ids = ["hadith_sunnah_api"]
            status = "blocked_before_retrieval" if intent == "invented_hadith_request" else "metadata_stubbed"
            return RetrievalPacket("hadith_metadata", source_ids, status, source_ids)

        if intent in {
            "personal_fiqh_escalation",
            "sectarian_verdict_request",
            "sectarian_bait",
            "source_missing_refusal",
        }:
            return RetrievalPacket("source_policy", ["source_policy"], "not_attempted_guardrail", [])

        if intent == "respectful_difference_comparison":
            source_ids = ["source_policy"]
            return RetrievalPacket("source_policy", source_ids, "metadata_stubbed", source_ids)

        if intent in {"prayer_learning", "prayer_times", "prayer_method_escalation"}:
            source_ids = ["prayer_times_aladhan", "source_policy"]
            return RetrievalPacket("prayer_metadata", source_ids, "metadata_stubbed", source_ids)

        if intent == "prayer_metadata":
            return RetrievalPacket("prayer_metadata", ["prayer_times_aladhan"], "metadata_stubbed", [])

        if intent in {"general_islamic_learning", "source_comparison_with_escalation"}:
            source_ids = ["quran_api_quran_foundation", "hadith_sunnah_api"]
            required_sources = [*source_ids, "source_policy"]
            return RetrievalPacket(
                "learning_metadata",
                required_sources,
                "metadata_stubbed",
                source_ids,
            )

        return RetrievalPacket("none", [], "not_required", [])

    def verify_citations(
        self,
        user_question: str,
        classification: Classification,
        retrieval: RetrievalPacket,
    ) -> CitationVerification:
        """Verify the metadata-only citation contract.

        Future plug-in point: extract claims from the generated answer, align
        each claim to retrieved source IDs, and block hallucinated references.
        """
        q = user_question.lower()

        if "do not cite" in q or "without citation" in q or "no citation" in q:
            return CitationVerification(
                "failed",
                ["user_requested_citation_bypass"],
                True,
                [],
            )

        if classification.should_refuse:
            return CitationVerification("not_applicable_refusal", [], False, [])

        if classification.citation_required and not retrieval.source_registry_ids:
            return CitationVerification(
                "failed",
                ["no_source_registry_ids_available"],
                False,
                [],
            )

        if classification.citation_required:
            return CitationVerification(
                "metadata_verified",
                [],
                False,
                retrieval.source_registry_ids,
            )

        return CitationVerification("not_required", [], False, [])

    def apply_guardrails(
        self,
        classification: Classification,
        citation: CitationVerification,
    ) -> GuardrailDecision:
        """Apply refusal and escalation rules before response construction.

        Future plug-in point: combine policy engine, safety classifier,
        citation verifier, and scholar-escalation router.
        """
        if classification.scholar_escalation_required and classification.should_refuse:
            return GuardrailDecision(
                "escalate",
                "request_requires_qualified_human_authority",
                "personal_or_high_risk_religious_verdict",
            )

        if classification.should_refuse:
            reason = "citation_bypass_or_fabrication_request"
            if classification.intent == "invented_hadith_request":
                reason = "invented_hadith_request"
            return GuardrailDecision("refuse", reason, None)

        if citation.citation_check_status == "failed":
            return GuardrailDecision("refuse", "citation_verification_failed", None)

        if classification.scholar_escalation_required:
            return GuardrailDecision(
                "escalate",
                None,
                "qualified_human_review_required",
            )

        return GuardrailDecision("allow", None, None)

    def build_response_contract(
        self,
        classification: Classification,
        retrieval: RetrievalPacket,
        citation: CitationVerification,
        guardrail: GuardrailDecision,
    ) -> ResponseContract:
        """Return placeholders only; no religious content is generated here.

        Future plug-in point: only after retrieval and citation verification
        pass should an LLM draft a source-grounded answer. The output should
        still conform to this response contract.
        """
        disclaimer = (
            "DeenAI is a source-grounded learning prototype, not scholar-approved "
            "and not a fatwa system."
        )

        if guardrail.guardrail_decision == "escalate":
            if guardrail.refusal_reason is None:
                return ResponseContract(
                    "educational_with_escalation",
                    True,
                    "ANSWER_TEMPLATE: Provide neutral cited learning context only and include a qualified-human escalation boundary.",
                    disclaimer,
                    classification.citation_required,
                )
            return ResponseContract(
                "escalation",
                False,
                "ESCALATION_TEMPLATE: Do not issue a ruling. Direct the user to qualified human authority and offer source-lookup notes only.",
                disclaimer,
                False,
            )

        if guardrail.guardrail_decision == "refuse":
            return ResponseContract(
                "refusal",
                False,
                "REFUSAL_TEMPLATE: Explain the boundary briefly. Do not provide sacred text, fabricated references, Arabic, or rulings.",
                disclaimer,
                False,
            )

        if citation.citation_check_status == "metadata_verified":
            return ResponseContract(
                "citation_grounded_placeholder",
                True,
                "ANSWER_TEMPLATE: Provide a short educational placeholder answer only after future retrieval supplies approved source text and citations.",
                disclaimer,
                True,
            )

        return ResponseContract(
            "general_placeholder",
            True,
            "ANSWER_TEMPLATE: Provide non-ruling educational or product guidance without sacred text.",
            disclaimer,
            False,
        )

    def write_trace_log(
        self,
        user_question: str,
        classification: Classification,
        retrieval: RetrievalPacket,
        citation: CitationVerification,
        guardrail: GuardrailDecision,
        response: ResponseContract,
    ) -> dict[str, Any]:
        """Build one JSON-serializable trace row.

        Future plug-in point: write this same shape to append-only observability
        storage with request IDs, latency, token cost, and verifier details.
        """
        notes = [
            "stub_pipeline_no_llm_no_live_api",
            "metadata_only_no_religious_text",
            f"required_sources={','.join(retrieval.required_sources) or 'none'}",
        ]
        if guardrail.refusal_reason:
            notes.append(f"refusal_reason={guardrail.refusal_reason}")
        if guardrail.scholar_escalation_reason:
            notes.append(f"scholar_escalation_reason={guardrail.scholar_escalation_reason}")
        if citation.missing_citation_reasons:
            notes.append("missing_citations=" + ",".join(citation.missing_citation_reasons))

        return {
            "trace_id": str(uuid.uuid4()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "user_question": user_question,
            "intent": classification.intent,
            "risk_level": classification.risk_level,
            "source_registry_ids": retrieval.source_registry_ids,
            "verified_source_ids": citation.verified_source_ids,
            "retrieval_status": retrieval.retrieval_status,
            "citation_check_status": citation.citation_check_status,
            "guardrail_decision": guardrail.guardrail_decision,
            "response_type": response.response_type,
            "scholar_escalation_required": classification.scholar_escalation_required,
            "citation_required": classification.citation_required,
            "notes": notes,
        }


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=True, sort_keys=True) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the DeenAI stub pipeline examples.")
    parser.add_argument("--trace-output", type=Path, default=DEFAULT_TRACE_OUTPUT)
    parser.add_argument("--question", action="append", help="Optional question. Can be used more than once.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    questions = args.question or SAMPLE_QUESTIONS
    pipeline = DeenAIPipelineStub()
    results = [pipeline.process(question) for question in questions]
    trace_rows = [result["trace_log"] for result in results]
    write_jsonl(args.trace_output, trace_rows)

    print(f"DeenAI pipeline stub wrote {len(trace_rows)} trace rows.")
    print(f"Trace JSONL: {args.trace_output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
