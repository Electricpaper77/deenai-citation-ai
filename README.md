# DeenAI

Live demo: [https://deenai-citation-ai.vercel.app/](https://deenai-citation-ai.vercel.app/)

GitHub repo: [https://github.com/Electricpaper77/deenai-citation-ai](https://github.com/Electricpaper77/deenai-citation-ai)

Proof artifacts: 7 source registry entries | 60 eval prompts | 60 pipeline traces | 22 mock retrieval packets | 28 claim-citation cases | 19 render-blocking scenarios | 0 prohibited UI content fields | Full validator: PASS

## 30-Second Recruiter Proof

Open the live demo: [https://deenai-citation-ai.vercel.app/](https://deenai-citation-ai.vercel.app/)

DeenAI proves a citation-gated answer contract for Islamic AI reliability. It shows how an answer surface can allow low-risk educational placeholders, block unsupported answers, or escalate personal/high-risk questions before any live religious answer is rendered.

What to verify:

- **ALLOW / BLOCK / ESCALATE flow:** the homepage contract demo renders deterministic fixture decisions.
- **JSONL audit traces:** each fixture result exposes a compact audit trail.
- **Proof Chain:** the Sources / Proof page summarizes registry, eval, retrieval packet, claim-citation, and render-blocking checks.
- **Trust Pattern Compiler:** public proof cards map UX, trust, citation, and safety patterns into DeenAI features.
- **Fixture-only boundary:** no live LLM, no live RAG, no external religious API calls, no rulings, and no scholar approval claims.

Reviewer path:

1. Open the [live site](https://deenai-citation-ai.vercel.app/).
2. Click the Ask DeenAI Contract Demo presets.
3. Test `ALLOW`, `BLOCK`, and `ESCALATE`.
4. Open [Sources / Proof](https://deenai-citation-ai.vercel.app/sources.html).
5. Verify the proof-chain cards and Trust Pattern Compiler section.

Proof package:

- [Proof README](docs/proof/README.md)
- [Business report](docs/proof/deenai_business_report.md)
- [Homepage screenshot](docs/screenshots/deenai-proof-01-homepage.png)
- [Ask Contract Demo screenshot](docs/screenshots/deenai-proof-02-contract-demo.png)
- [Proof Chain screenshot](docs/screenshots/deenai-proof-03-proof-chain.png)
- [Trust Pattern Compiler screenshot](docs/screenshots/deenai-proof-04-trust-ux.png)

Resume bullet:

> Built and deployed DeenAI, a citation-gated Islamic AI reliability prototype with an interactive ALLOW/BLOCK/ESCALATE answer-contract demo, JSONL audit traces, 60 eval prompts, 28 claim-to-citation checks, and 19 render-blocking scenarios preventing unsupported answers before UI display.

## Project Overview

DeenAI is a recruiter-facing Applied GenAI prototype for citation-first Islamic AI learning. The project focuses on the safety and evaluation foundation behind a future learning website for Quran, Sunnah, duas, hadith lookup, prayer basics, and general Islamic education.

The current implementation is intentionally pre-production: it uses static UI pages, metadata-only source governance, rule-based pipeline checks, mock retrieval packets, and claim-to-citation verifier cases. It does not call a live LLM, does not call live religious content APIs, and does not render religious source text.

Static UI pages now include a homepage, methodology page, sources/proof page, and Ask DeenAI preview page for placeholder-only answer states plus a deterministic safety trace simulator.

## Why DeenAI Exists

Islamic AI systems require stricter reliability controls than a generic chatbot. Unsupported claims, fabricated references, invented source text, and unsafe ruling-style answers can create real user harm.

DeenAI exists to demonstrate how an AI Solutions Engineer or LLM Evaluation engineer can design a grounded-answer architecture before generation is allowed:

- Source IDs must be approved before retrieval.
- Retrieval packets must remain metadata-only until licensing and source review pass.
- Claims must map to verified source IDs before rendering.
- High-risk requests must refuse or escalate instead of producing normal answers.
- UI states must expose limitations instead of hiding uncertainty.

## Safety Architecture

DeenAI models a citation-gated safety chain:

1. Source registry validation
2. Rule-based query classification
3. Pipeline contract evaluation
4. Metadata-only mock retrieval packets
5. Citation packet verification
6. Claim-to-citation verification
7. Render decision blocking
8. Deterministic safety trace simulation

The current pipeline is a contract stub, not deployed AI behavior. It simulates how future retrieval-augmented generation, source retrieval, citation verification, guardrails, and answer rendering would connect without generating religious content.

The Ask DeenAI page includes a client-side Safety Trace Simulator. It uses static prompt categories and deterministic scoring rules to show risk score, citation score, guardrail decision, and render decision. It does not call a live model or live religious content retrieval.

## Source Governance

The source registry defines approved source categories, provider metadata, storage policy, allowed use, restricted use, citation-required fields, and risk level.

Current source governance covers:

- Quran canonical text source strategy
- Quran API source strategy
- Backup Quran API source strategy
- Hadith source strategy
- Dua and adhkar source strategy
- Prayer time source strategy
- Local metadata and source policy controls

Source governance rules:

- No invented Quran, Hadith, dua, or religious references.
- No inferred hadith grading.
- No scholar approval claimed.
- No religious ruling capability claimed.
- Licensing review is required before real content display.
- Prayer time method and local-authority differences must be disclosed.

## Evaluation Artifacts

Key artifacts:

- `ask.html`
- `scripts/deenai_trace_simulator.js`
- `sources/source_registry.json`
- `evals/deenai_eval_prompts.jsonl`
- `evals/pipeline_eval_traces.jsonl`
- `evals/pipeline_eval_summary.json`
- `evals/mock_retrieval_packets.jsonl`
- `evals/citation_verification_report.json`
- `evals/mock_claim_citation_cases.jsonl`
- `evals/claim_citation_verification_report.json`
- `evals/deenai_pre_ui_safety_summary.json`

Documentation:

- `docs/DEENAI_SOURCE_POLICY.md`
- `docs/DEENAI_SOURCE_REGISTRY_VALIDATION.md`
- `docs/DEENAI_PIPELINE_CONTRACT.md`
- `docs/DEENAI_PIPELINE_EVAL_REPORT.md`
- `docs/DEENAI_CITATION_VERIFIER.md`
- `docs/DEENAI_CLAIM_CITATION_VERIFIER.md`
- `docs/DEENAI_PRE_UI_SAFETY_CHAIN.md`

## Screenshots

Screenshot placeholders:

- `docs/screenshots/deenai-01-home.png`
- `docs/screenshots/deenai-02-ask-preview.png`
- `docs/screenshots/deenai-03-how-it-works.png`
- `docs/screenshots/deenai-04-sources-proof.png`

## Live Page Verification

Verify these deployed routes after each packaging or deployment change:

- `/`
- `/ask.html`
- `/how-it-works.html`
- `/sources.html`

## How To Run Validation Scripts

Run these commands from the project root.

```bash
python scripts/validate_source_registry_usage.py
```

Validates source registry entries and checks emitted source IDs against `sources/source_registry.json`.

```bash
python scripts/run_deenai_pipeline_eval.py
```

Runs the 60-prompt eval dataset through the rule-based `DeenAIPipelineStub` and writes pipeline traces plus summary metrics.

```bash
python scripts/verify_citation_packets.py
```

Validates metadata-only retrieval packets, citation fields, source IDs, and unsafe generation flags.

```bash
python scripts/verify_claim_citations.py
```

Validates placeholder claim IDs against verified source IDs and blocks rendering when support is missing or unsafe.

Optional static UI shell validation:

```bash
python work/validate_static_shell.py
```

Checks the current static pages, navigation links, validation counts, CSS structure, responsive breakpoints, and overclaim/content-safety wording.

Full static proof MVP validation:

```bash
python work/validate_deenai_project.py
```

Checks required pages, proof artifacts, JSON/JSONL parsing, page links, Ask DeenAI safety states, proof metrics, overclaim wording, and prohibited UI display-content labels.
It also checks that the Safety Trace Simulator script exists, is referenced by `ask.html`, and exposes all five static simulator prompt labels.

## Current Rule-Based Validation Metrics

These metrics are rule-based contract validation only. They do not measure live LLM performance, real retrieval quality, deployed retrieval-generation performance, scholar review, or live answer safety.

| Metric | Count |
| --- | ---: |
| Source registry entries | 7 |
| Eval prompts | 60 |
| Pipeline traces | 60 |
| Mock retrieval packets | 22 |
| Claim-citation cases | 28 |
| Blocked render cases | 19 |
| Prohibited content fields | 0 |

## Limitations

- No live LLM is connected.
- No live API retrieval is connected.
- No deployed retrieval-generation system is implemented.
- No model-performance measurement is claimed.
- No measured production latency or cost is available.
- No scholar approval is claimed.
- No religious ruling capability is claimed.
- Real source display requires licensing and permission review.
- Religious content rendering remains blocked in the current prototype.

## Roadmap

Near-term:

- Add visual polish and copy review for the verifier-failed Ask DeenAI state.
- Add CI-style validation commands for all JSON, JSONL, and static UI checks.
- Expand source registry validation with stricter license and storage policy checks.

Future integration:

- Connect approved source APIs behind retrieval adapters.
- Add schema-validated retrieval packets from real metadata.
- Add claim extraction and source mapping around an LLM response draft.
- Add human review workflows for high-risk categories.
- Add latency, cost, and retrieval-quality measurement once live systems exist.

## Resume Bullet

Built DeenAI, a citation-gated Islamic AI reliability prototype with 7 source registry entries, 60 rule-based eval prompts, 60 pipeline traces, 22 mock retrieval packets, 28 claim-to-citation test cases, and 19 render-blocking scenarios to prevent unsupported religious answers before UI display.
