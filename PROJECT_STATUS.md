# DeenAI Project Status

## Current Project Status

DeenAI is a static proof MVP for a citation-gated Islamic AI learning experience. The project now has planning docs, source governance metadata, rule-based evaluation artifacts, mock retrieval packet checks, claim-to-citation checks, static methodology UI, placeholder-only Ask DeenAI UI states, and a deterministic Safety Trace Simulator.

The current build is intentionally pre-production. It does not call a live LLM, does not call live APIs, does not render religious source text, and does not provide religious rulings.

GitHub push: Complete.

Vercel deployment: Complete.

Live demo: [https://deenai-citation-ai.vercel.app/](https://deenai-citation-ai.vercel.app/)

## Pages Completed

- `index.html`: Static homepage and project positioning.
- `ask.html`: Placeholder-only Ask DeenAI preview with safe answer states.
- `scripts/deenai_trace_simulator.js`: Client-side deterministic risk/citation scoring simulator.
- `how-it-works.html`: Evaluation methodology and safety chain page.
- `sources.html`: Source governance and proof artifact inventory.

## Validation Artifacts Completed

- Source registry metadata.
- Source registry usage validation report.
- 60-prompt rule-based eval dataset.
- Pipeline eval traces and summary.
- Mock retrieval packet dataset and citation verification report.
- Mock claim-citation cases and claim verification report.
- Pre-UI safety summary.
- Static UI shell validation.
- Full static proof MVP validation.
- Safety Trace Simulator validation.

## Current Proof Metrics

Label: Rule-Based Contract Validation

| Metric | Count |
| --- | ---: |
| Source registry entries | 7 |
| Eval prompts | 60 |
| Pipeline traces | 60 |
| Mock retrieval packets | 22 |
| Claim-citation cases | 28 |
| Blocked render cases | 19 |
| Prohibited content fields | 0 |

## Intentionally Not Implemented Yet

- No live LLM.
- No live API retrieval.
- No deployed retrieval-generation system.
- No live simulator backend.
- No model-performance measurement.
- No real religious content display.
- No scholar approval claimed.
- No religious ruling capability claimed.
- No deployment.

## Remaining Risks

- Licensing and permission review is still required before any real source display.
- Source adapters need live integration tests once APIs are connected.
- Retrieval quality, latency, and cost are not measured yet.
- Human review workflows are not implemented yet.
- Static UI states still need visual QA across more devices.

## Next Roadmap

1. Capture screenshots, including the Safety Trace Simulator.
2. Add screenshots to `docs/screenshots`.
3. Update portfolio card.
4. Post LinkedIn launch.
5. Do not add live LLM or live retrieval-generation until source licensing is reviewed.
6. Add CI configuration for the validation command.
