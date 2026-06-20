# DeenAI Pre-UI Safety Chain

## Purpose

DeenAI is ready for static methodology UI because its pre-UI safety contracts now exist as machine-readable artifacts.

This does not mean DeenAI has real LLM performance, production RAG accuracy, scholar approval, or fatwa capability. It means the project has a validated placeholder safety chain for source governance, guardrail routing, metadata-only retrieval, citation packet checks, and claim-to-citation render blocking.

All metrics below are rule-based contract validation metrics.

## Current Validation Chain

1. Source registry validation checks that pipeline source IDs exist in `sources/source_registry.json`.
2. Pipeline eval checks that the rule-based stub classifies 60 prompts into expected answer, refusal, escalation, risk, and citation states.
3. Mock retrieval packet verification checks metadata-only packets against source registry metadata.
4. Claim-citation verification checks placeholder claim IDs against verified source IDs before rendering.

## Artifact Inventory

| Layer | Artifact |
| --- | --- |
| Source registry | `sources/source_registry.json` |
| Source registry report | `evals/source_registry_validation_report.json` |
| Eval dataset | `evals/deenai_eval_prompts.jsonl` |
| Pipeline traces | `evals/pipeline_eval_traces.jsonl` |
| Pipeline summary | `evals/pipeline_eval_summary.json` |
| Retrieval packets | `evals/mock_retrieval_packets.jsonl` |
| Retrieval packet report | `evals/citation_verification_report.json` |
| Claim-citation cases | `evals/mock_claim_citation_cases.jsonl` |
| Claim-citation report | `evals/claim_citation_verification_report.json` |
| Pre-UI summary | `evals/deenai_pre_ui_safety_summary.json` |

## Key Metrics

| Metric | Value |
| --- | ---: |
| Source registry entries | 7 |
| Source registry validation | pass |
| Pipeline eval prompts | 60 |
| Pipeline eval passed | 60 |
| Pipeline eval failed | 0 |
| Pipeline eval pass rate | 100.00% |
| Mock retrieval packets | 22 |
| Citation packet verification | pass |
| Claim-citation cases | 28 |
| Claim-citation passed | 28 |
| Claim-citation failed | 0 |
| Blocked render cases | 19 |
| Prohibited content fields found | 0 |

## What The System Blocks Before Rendering

The current contract blocks these cases before normal answer rendering:

- Missing source IDs.
- Wrong source type mappings.
- Unsupported placeholder claims.
- Citation-required claims without source mappings.
- Citation-required answers without a citation panel.
- Fake citation requests.
- Invented hadith requests.
- Citation bypass requests.
- Source-missing requests that try to force memory-based answers.
- High-risk fiqh, divorce, inheritance, and finance requests.
- Sectarian bait and verdict requests.
- Any packet or claim case containing prohibited content fields such as Arabic, Quran text, hadith text, dua text, translation, transliteration, or ruling text.

## Why This Matters For Islamic AI Safety

Islamic AI safety depends on refusing to let fluency stand in for authority.

The safety chain ensures DeenAI can show its work before it shows an answer. A future answer must pass through source registry checks, retrieval metadata checks, claim-to-source mapping, and render-blocking rules. This prevents the UI from implying religious authority when the system only has placeholders, missing sources, unsafe requests, or unsupported claims.

The model is not treated as a source of Islamic knowledge.

## What Is Still Not Measured

The current artifacts do not measure:

- Real LLM quality.
- Production RAG accuracy.
- Semantic claim-source alignment.
- Citation precision on generated answer text.
- Hallucinated citation rate from a real model.
- Live API reliability.
- Source licensing clearance.
- Latency.
- Cost/request.
- Scholar review quality.

## Safe UI Placeholder Policy

The static UI may show only placeholder states:

- `answer_allowed_placeholder`
- `citation_panel_required`
- `refusal`
- `scholar_escalation`
- `source_missing`
- `verifier_failed`
- `retrieval_metadata_only`

The static UI must not display Quran text, hadith text, dua text, Arabic, translations, transliterations, or religious rulings.

The static UI must clearly label metrics as rule-based contract validation, not real LLM performance.

## Next Step

Build a static `How DeenAI Works` / `Evaluation Methodology` page.

That page should explain the safety chain visually and link the proof artifacts, while keeping all answer examples as placeholders until real source permissions, retrieval, citation verification, and LLM evaluation exist.
