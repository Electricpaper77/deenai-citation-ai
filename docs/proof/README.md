# DeenAI Proof Package

Live demo: [https://deenai-citation-ai.vercel.app/](https://deenai-citation-ai.vercel.app/)

Deployed commit: `04f59a4c8e5a99825754492948f5959ccdf5421a`

## What This Proves

DeenAI is a fixture-only citation-gated reliability prototype. It demonstrates how an Islamic AI answer surface can require source IDs, citation requirements, claim mapping, render-blocking checks, and human escalation before an answer is shown.

It does not call a live LLM, run live RAG, use external religious APIs, generate rulings, render religious source content, or claim scholar approval.

## Reviewer Path

1. Open [the live site](https://deenai-citation-ai.vercel.app/).
2. Use the Ask DeenAI Contract Demo presets.
3. Verify `ALLOW`, `BLOCK`, and `ESCALATE` decisions.
4. Confirm the JSONL audit trace updates for each preset.
5. Open [Sources / Proof](https://deenai-citation-ai.vercel.app/sources.html).
6. Verify the Proof Chain and Trust Pattern Compiler cards.

## Validation Checklist

- [x] Live root route opens.
- [x] `/index.html` opens.
- [x] Ask Contract Demo supports `ALLOW`, `BLOCK`, and `ESCALATE`.
- [x] JSONL audit traces display.
- [x] Sources / Proof page shows six proof-chain cards.
- [x] Trust Pattern Compiler is visible and compact.
- [x] Public page does not expose a dense competitor matrix.
- [x] Mobile layout at 390px has no horizontal overflow.
- [x] No console errors were observed during live validation.
- [x] No external API calls were observed during live validation.
- [x] No live LLM, live RAG, religious content rendering, copied competitor content, or ruling generation was added.

## Screenshots

- [Homepage](../screenshots/deenai-proof-01-homepage.png)
- [Ask Contract Demo](../screenshots/deenai-proof-02-contract-demo.png)
- [Proof Chain](../screenshots/deenai-proof-03-proof-chain.png)
- [Trust Pattern Compiler](../screenshots/deenai-proof-04-trust-ux.png)

## Business Report

- [DeenAI business report](deenai_business_report.md)

## Known Limitation

This is a static fixture-only demo. It validates the safety contract and reviewer proof path, not live retrieval quality, model performance, scholar review, production latency, or real religious answer safety.

## Resume Bullet

Built and deployed DeenAI, a citation-gated Islamic AI reliability prototype with an interactive ALLOW/BLOCK/ESCALATE answer-contract demo, JSONL audit traces, 60 eval prompts, 28 claim-to-citation checks, and 19 render-blocking scenarios preventing unsupported answers before UI display.
