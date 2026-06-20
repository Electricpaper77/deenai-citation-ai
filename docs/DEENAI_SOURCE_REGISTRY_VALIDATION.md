# DeenAI Source Registry Validation

## Purpose

This document explains the source registry validation step for DeenAI.

The validator checks whether source IDs emitted by the stubbed pipeline are actually present in `sources/source_registry.json`, and whether each registry entry has the minimum metadata needed before moving toward mock retrieval packets.

This is a metadata-only safety check. It does not call real APIs, load Quran text, load hadith text, load dua text, generate Arabic, infer religious authenticity, or issue rulings.

## Validation Checks

Script:

```bash
scripts/validate_source_registry_usage.py
```

Inputs:

```bash
sources/source_registry.json
evals/pipeline_eval_traces.jsonl
```

Output:

```bash
evals/source_registry_validation_report.json
```

The validator checks:

- Every `source_registry_id` or `verified_source_id` emitted by pipeline traces exists in the source registry.
- Every registry entry includes:
  - `source_id`
  - `content_type`
  - `provider`
  - `url`
  - `storage_policy`
  - `citation_required_fields`
  - `allowed_use`
  - `restricted_use`
  - `risk_level`
  - `notes`
- `risk_level` is one of `low`, `medium`, or `high`.
- Quran, hadith, dua, and prayer-time sources have non-empty `citation_required_fields`.
- Registry entries do not make prohibited positive claims about institutional endorsement, ruling capability, model-generated hadith grading, or broad copied religious text use.

## Why This Matters

For Islamic AI safety, source IDs are not just implementation details. They are the spine of the product's trust model.

If the pipeline can emit a source ID that is missing from the registry, the system can drift into unsupported citations. If registry entries are missing citation fields or storage rules, the UI could display content without enough provenance. If a source entry overstates allowed use, the system could accidentally imply religious authority or licensing clearance that does not exist.

This validation step keeps DeenAI aligned with its core rule: the model is not the source of Islamic knowledge.

## Current Results

Source report:

```bash
evals/source_registry_validation_report.json
```

Current result:

| Field | Value |
| --- | ---: |
| Total registry entries | 7 |
| Pipeline source IDs referenced | 6 |
| Missing source references | 0 |
| Invalid registry entries | 0 |
| Pass/fail | pass |

Valid referenced source IDs:

- `dua_hisn_almuslim_sunnah`
- `hadith_sunnah_api`
- `prayer_times_aladhan`
- `quran_api_quran_foundation`
- `quran_arabic_tanzil`
- `source_policy`

Warning:

- High-risk source entries require field-level licensing and permission review: `dua_hisn_almuslim_sunnah`, `hadith_sunnah_api`, `quran_api_quran_foundation`.

## Remaining Licensing Risks

- Quran translations may have separate rights from Arabic source text.
- Hadith API access does not automatically mean copied text or bulk storage is allowed.
- Dua and adhkar content requires a specific edition, translation, transliteration policy, and permission review.
- Prayer-time output must remain clearly framed as calculated provider data, not a universal local authority.
- Audio, tafsir, transliteration, and derived content should remain out of scope until separately reviewed.

## Next Step

Add a mock retrieval packet schema that uses validated `source_registry_id` values and citation metadata only.

The next contract should prove that a retrieval packet can carry source provenance without carrying copied Quran, hadith, dua, Arabic, or ruling text. Once that is stable, DeenAI can add a citation verifier stub that checks claim IDs against mock source IDs before any real RAG or LLM integration.
