# DeenAI Claim-Citation Verifier

## Purpose

The claim-citation verifier is the final pre-UI safety contract before answer rendering.

It validates placeholder claim IDs against verified source registry IDs. This proves that DeenAI can block unsupported, unmapped, or incorrectly mapped claims before any generated answer appears in the interface.

This verifier does not call live APIs, call an LLM, load religious content, infer hadith grading, claim endorsement, or render UI.

## Claim-To-Source Mapping Contract

Schema:

```bash
schemas/claim_citation.schema.json
```

Mock cases:

```bash
evals/mock_claim_citation_cases.jsonl
```

Each case includes:

- `case_id`
- `eval_id`
- `user_question`
- `intent`
- `risk_level`
- `guardrail_decision`
- `allowed_to_answer`
- `citation_panel_present`
- `retrieved_source_ids`
- `placeholder_claims`
- `expected_verification_result`
- `expected_render_decision`
- `notes`

Each placeholder claim includes:

- `claim_id`
- `claim_type`
- `claim_text_placeholder`
- `required_source_type`
- `mapped_source_registry_id`
- `citation_required`
- `support_status`

The `claim_text_placeholder` field must stay as a label only. It must not contain Quran text, hadith text, dua text, Arabic, translation, transliteration, or ruling text.

## Render-Blocking Rules

The verifier blocks rendering when:

- A citation-required claim has no mapped source ID.
- The mapped source ID does not exist in `sources/source_registry.json`.
- The mapped source was not retrieved for the case.
- The mapped source type does not match the claim's required source type.
- A claim is marked unsupported.
- A normal answer is allowed for a blocked, fake citation, invented hadith, sectarian, source-missing, or ruling-like case.
- A citation-required normal answer has no citation panel.
- Any prohibited content field appears.

Refusal and escalation placeholders can pass without a citation panel when they do not render a normal answer.

## Safety Boundaries

The verifier enforces these boundaries:

- No real LLM calls.
- No live source APIs.
- No Quran text.
- No hadith text.
- No dua text.
- No Arabic text.
- No translations or transliterations.
- No religious ruling text.
- No inferred hadith grading.
- No claim of scholar approval.

Only source IDs, placeholder claim labels, and metadata are allowed.

## Current Results

Report:

```bash
evals/claim_citation_verification_report.json
```

Current result:

| Metric | Value |
| --- | ---: |
| Total cases | 28 |
| Passed | 28 |
| Failed | 0 |
| Pass rate | 100.00% |
| Supported claims | 17 |
| Unsupported claims | 1 |
| Blocked render cases | 19 |
| Prohibited content fields found | 0 |
| Pass/fail | pass |

Intentional blocked cases detected:

- Missing source mapping: `CCC-023/CLAIM-MISSING-SOURCE-001`
- Missing registry source ID: `CCC-027/CLAIM-MISSING-REGISTRY-001`
- Wrong source type mapping: `CCC-022/CLAIM-WRONG-SOURCE-001`
- Unsupported claim: `CCC-024/CLAIM-UNSUPPORTED-001`
- Missing citation panel: `CCC-025`
- Unsafe normal answer for fake citation case: `CCC-026`

Warning:

- High-risk registry sources still require licensing and permission review before real retrieval: `dua_hisn_almuslim_sunnah`, `hadith_sunnah_api`, `quran_api_quran_foundation`.

## Limitations

- The verifier checks placeholder claims, not natural-language answer claims.
- It does not perform semantic claim-source alignment.
- It does not validate real source text.
- It does not measure hallucinated citation rate from a model.
- It does not check live provider availability or permissions beyond registry metadata.
- It does not render UI states.

## Next Step Before UI

Create a pre-UI contract summary page or README section that links the full safety chain:

1. Source registry validation.
2. Pipeline eval traces.
3. Mock retrieval packet verification.
4. Claim-to-citation verification.

After that, DeenAI can begin static UI work with safe placeholder states: answer allowed, citation panel required, refusal, escalation, verifier failure, and source-missing.
