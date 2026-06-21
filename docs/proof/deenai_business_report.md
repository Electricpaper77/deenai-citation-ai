# DeenAI Business Report

## Business Position

DeenAI is a citation-gated Islamic AI reliability prototype for recruiters, technical reviewers, and product evaluators. It demonstrates how a sensitive-domain AI product can prove answer safety before rendering, without using live LLM calls, live RAG, external religious APIs, religious content, rulings, or scholar approval claims.

The public site is a static fixture-only proof surface. The business value is not religious answer generation; it is the reliability architecture around source governance, refusal, escalation, audit traces, and render blocking.

## Market Gap

Islamic learning products often optimize for reading, search, courses, utility tools, or question-answer workflows. Recruiters reviewing an AI prototype need a different proof: can the system explain what it will not answer, show why an answer is blocked, and make source constraints inspectable in seconds?

DeenAI fills that gap by turning trust patterns into visible product controls:

- Clear boundary copy before users interact.
- Citation-gated rendering before an answer surface appears.
- JSONL trace visibility for reviewer inspection.
- Human escalation for personal or high-risk questions.

## Trust Pattern Analysis

The internal competitive research reviewed public Islamic learning, Quran, Hadith, fatwa, utility, and education websites at a high level. The analysis extracted broad product patterns only: navigation, trust signals, source handling, disclaimers, mobile review, proof surfaces, and conversion paths.

The research did not copy competitor content, religious text, translations, rulings, branding, icons, CSS, or proprietary wording. The full internal matrix remains in `docs/research/competitive_ux_patterns.md`.

## Pattern-To-Feature Mapping

| Pattern | DeenAI Feature | Reviewer Proof |
| --- | --- | --- |
| UX Pattern | 30-second reviewer path from demo to proof artifacts | Homepage demo and Sources / Proof page |
| Trust Pattern | Clear non-fatwa and fixture-only boundary | Visible disclaimers across Ask and proof surfaces |
| Citation Pattern | Source IDs, claim mapping, and JSONL trace | Contract demo result panel and audit trace |
| Safety Pattern | Block or escalate before rendering | `BLOCK` and `ESCALATE` fixture states |

## What DeenAI Proves

- A sensitive-domain AI prototype can be evaluated without generating live religious answers.
- Reliability claims can be backed by fixture metrics and inspectable artifacts.
- Unsupported answers can be blocked before UI display.
- Personal or high-risk questions can route to qualified human review instead of simulated authority.

## Known Limits

- Static fixture-only demo.
- No live retrieval or live model evaluation.
- No scholar review workflow implemented.
- No real religious source content display.
- No production latency, cost, or retrieval-quality measurements.

## Final Resume Bullet

Built and deployed DeenAI, a citation-gated Islamic AI reliability prototype with an interactive ALLOW/BLOCK/ESCALATE answer-contract demo, JSONL audit traces, source governance, trust-pattern mapping, 60 eval prompts, 28 claim-to-citation checks, and 19 render-blocking scenarios preventing unsupported answers before UI display.
