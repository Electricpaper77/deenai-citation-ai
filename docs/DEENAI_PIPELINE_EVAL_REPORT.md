# DeenAI Pipeline Eval Report

## Purpose

This report documents the result of running the 60-prompt DeenAI eval dataset through `DeenAIPipelineStub`.

The purpose is rule-based pipeline contract validation. It checks whether the current stubbed pipeline produces the expected risk labels, refusal behavior, citation requirements, scholar escalation flags, and answer/refusal posture for the planned DeenAI safety taxonomy.

This is not production AI evaluation and not a claim of real model accuracy.

## What Is Measured

The runner compares each eval prompt against these expected fields:

- `risk_level`
- `should_refuse`
- `scholar_escalation_required`
- `citation_required`
- `should_answer`

It also records:

- guardrail decision
- response type
- category-level pass/fail counts
- risk-level pass/fail counts
- expected-vs-actual matrices for refusal, escalation, and citation requirements
- mismatch reasons

## What Is Not Measured

This run does not measure:

- LLM quality
- RAG retrieval quality
- source coverage
- Quran, hadith, dua, or Arabic correctness
- real citation precision
- hallucinated citation rate for generated answers
- latency
- token cost
- live API reliability
- scholar review quality

No real LLM, live API, vector database, or religious content source was called.

## Summary Metrics

Source file: `evals/pipeline_eval_summary.json`

| Metric | Value |
| --- | ---: |
| Runner type | rule-based pipeline contract validation |
| Total prompts | 60 |
| Passed | 60 |
| Failed | 0 |
| Pass rate | 100.00% |
| Real LLM called | false |
| Real live APIs called | false |
| Religious content generated | false |

## Guardrail Decision Breakdown

| Guardrail decision | Count |
| --- | ---: |
| allow | 21 |
| escalate | 15 |
| refuse | 24 |

## Expected Vs Actual Checks

### Refusal

| Case | Count |
| --- | ---: |
| expected true, actual true | 36 |
| expected true, actual false | 0 |
| expected false, actual true | 0 |
| expected false, actual false | 24 |

### Scholar Escalation

| Case | Count |
| --- | ---: |
| expected true, actual true | 15 |
| expected true, actual false | 0 |
| expected false, actual true | 0 |
| expected false, actual false | 45 |

### Citation Required

| Case | Count |
| --- | ---: |
| expected true, actual true | 29 |
| expected true, actual false | 0 |
| expected false, actual true | 0 |
| expected false, actual false | 31 |

## Category Breakdown

| Category | Total | Passed | Failed |
| --- | ---: | ---: | ---: |
| Arabic hallucination test | 5 | 5 | 0 |
| Divorce/inheritance/finance escalation | 5 | 5 | 0 |
| Dua recommendation | 5 | 5 | 0 |
| Fake citation request | 5 | 5 | 0 |
| General Islamic learning | 5 | 5 | 0 |
| Hadith lookup | 5 | 5 | 0 |
| High-risk fiqh | 5 | 5 | 0 |
| Invented hadith request | 5 | 5 | 0 |
| Prayer basics | 5 | 5 | 0 |
| Quran explanation | 5 | 5 | 0 |
| Sectarian bait | 5 | 5 | 0 |
| Source-missing refusal | 5 | 5 | 0 |

## Risk-Level Breakdown

| Expected risk level | Total | Passed | Failed |
| --- | ---: | ---: | ---: |
| blocked | 25 | 25 | 0 |
| high | 9 | 9 | 0 |
| low | 8 | 8 | 0 |
| medium | 18 | 18 | 0 |

## Top Failure Modes

No mismatch reasons were recorded in this run.

This only means the deterministic stub matched the deterministic eval labels. It does not mean the future model-backed DeenAI system will pass the same cases.

## Known Limitations

- The classifier is still rule-based and keyword-driven.
- The retrieval packet contains metadata and source registry IDs only.
- Citation verification does not inspect generated claims because no generation occurs.
- The response contract uses placeholder templates only.
- The pass rate is contract alignment, not model accuracy.
- The trace file does not include real latency, token count, model cost, source API errors, or retrieval confidence.
- The dataset is useful but small; it needs adversarial expansion before live model integration.

## Next Steps Before Real RAG/LLM Integration

1. Add a source registry validator that checks every emitted `source_registry_id` exists in `sources/source_registry.json`.
2. Add a mock retrieval packet schema with citation metadata fields but no religious text.
3. Add a citation verifier stub that accepts claim IDs and source IDs.
4. Add latency and cost placeholders to trace logs.
5. Expand eval prompts with paraphrases, multilingual queries, prompt injection, and ambiguous requests.
6. Keep all real Quran, hadith, dua, Arabic, translation, and prayer-time integrations blocked until licensing and citation policy are implemented.
