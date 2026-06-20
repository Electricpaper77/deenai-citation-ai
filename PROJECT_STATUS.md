# DeenAI Project Status

## Current Project Status

DeenAI is a static proof MVP for a citation-gated Islamic AI learning experience. The project now has planning docs, source governance metadata, rule-based evaluation artifacts, mock retrieval packet checks, claim-to-citation checks, static methodology UI, and placeholder-only Ask DeenAI UI states.

The current build is intentionally pre-production. It does not call a live LLM, does not call live APIs, does not render religious source text, and does not provide religious rulings.

## Pages Completed

- `index.html`: Static homepage and project positioning.
- `ask.html`: Placeholder-only Ask DeenAI preview with safe answer states.
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
- No model-performance measurement.
- No real religious content display.
- No scholar approval claimed.
- No fatwa capability claimed.
- No deployment.

## Remaining Risks

- Licensing and permission review is still required before any real source display.
- Source adapters need live integration tests once APIs are connected.
- Retrieval quality, latency, and cost are not measured yet.
- Human review workflows are not implemented yet.
- Static UI states still need visual QA across more devices.

## Next Roadmap

1. Add CI configuration for the validation command.
2. Add source adapter interfaces without fetching or displaying religious content.
3. Add mock screenshots or a recruiter-facing walkthrough.
4. Add live retrieval only after licensing, citation, and review policies are complete.
5. Add measured latency and cost checks once live services exist.
