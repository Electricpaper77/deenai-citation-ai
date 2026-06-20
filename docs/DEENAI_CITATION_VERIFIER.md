# DeenAI Citation Verifier

## Purpose

The mock citation verifier checks that DeenAI retrieval packets can carry source provenance safely before any UI, real RAG, live API, or LLM generation exists.

This layer is metadata-only. It does not load Quran text, hadith text, dua text, Arabic text, translations, transliterations, or rulings.

## Retrieval Packet Contract

Schema:

```bash
schemas/retrieval_packet.schema.json
```

Mock packets:

```bash
evals/mock_retrieval_packets.jsonl
```

Each packet includes:

- `packet_id`
- `eval_id`
- `user_question`
- `intent`
- `risk_level`
- `source_registry_ids`
- `retrieved_sources`
- `citation_required`
- `retrieval_status`
- `allowed_to_generate`
- `notes`

Each retrieved source includes metadata only:

- `source_registry_id`
- `source_type`
- `provider`
- `source_url`
- `citation_fields`
- `content_available: false`
- `content_placeholder: true`
- `licensing_review_required`
- `allowed_use`

## Citation Verification Checks

Script:

```bash
scripts/verify_citation_packets.py
```

The verifier checks:

- Every packet parses as JSONL.
- Every source ID exists in `sources/source_registry.json`.
- Retrieved source `source_type`, `provider`, and `source_url` match the registry.
- Citation-required packets include non-empty `citation_fields`.
- High-risk fiqh, invented hadith, fake citation, citation bypass, source-missing, Arabic hallucination, and sectarian bait cases do not allow generation.
- Packets do not contain prohibited religious content fields:
  - `arabic`
  - `quran_text`
  - `hadith_text`
  - `dua_text`
  - `translation`
  - `transliteration`
  - `ruling_text`

## Safety Boundaries

The verifier is designed to keep DeenAI in a safe pre-RAG state:

- No live APIs.
- No real LLM calls.
- No copied religious text.
- No generated Arabic.
- No generated hadith.
- No dua wording.
- No inferred hadith grading.
- No religious rulings.
- No claims of institutional or scholarly endorsement.

The only thing being verified is whether metadata can safely move through the retrieval and citation layers.

## Current Results

Report:

```bash
evals/citation_verification_report.json
```

Current result:

| Metric | Value |
| --- | ---: |
| Total packets | 22 |
| Passed | 22 |
| Failed | 0 |
| Pass rate | 100.00% |
| Missing source IDs | 0 |
| Invalid source metadata | 0 |
| Unsafe generation flags | 0 |
| Prohibited content fields found | 0 |
| Pass/fail | pass |

Warning:

- High-risk registry sources still require field-level licensing and permission review before real retrieval.

## Limitations

- The verifier does not validate real source text.
- It does not prove claim-source alignment because no answer text exists yet.
- It does not measure hallucination rate from an LLM.
- It does not validate provider licensing beyond registry metadata.
- It does not test latency, cost, retrieval ranking, or API behavior.
- The JSON schema is a contract artifact; the Python verifier performs the current executable checks.

## Next Step Before UI

Add a claim-to-citation verifier stub.

The next artifact should define placeholder claim IDs and map them to verified source IDs without generating answer text. That will create the final contract needed before UI work: a future answer can only be displayed if every claim maps to retrieved, registry-valid source metadata.
