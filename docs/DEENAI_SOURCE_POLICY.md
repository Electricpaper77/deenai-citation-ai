# DeenAI Source Policy

## Purpose

DeenAI is a citation-first Islamic learning project. Its source policy exists to prevent hallucinated Islamic claims, invented sacred text, fake references, inferred hadith grading, and accidental claims of religious authority.

This policy is part of the product foundation before UI implementation.

## Approved Source Categories

Approved source categories are listed in `sources/source_registry.json`.

Current source categories:

- Quran Arabic: Tanzil
- Quran API: Quran.com / Quran Foundation API
- Backup Quran API: Al Quran Cloud
- Hadith: Sunnah.com API
- Dua/adhkar: Hisn al-Muslim / Sunnah.com, pending specific edition and permission review
- Prayer Times: AlAdhan API

Approval in this policy means the source type is allowed for architecture and evaluation planning. It does not mean all content from that provider can be copied, cached, republished, or displayed. Each content field still needs provider terms, permission, and attribution review.

## Disallowed Sources

Do not use these sources for generated answers, retrieval indexes, citation cards, or public source claims:

- Social media posts.
- Unattributed images or screenshots.
- Unverified PDFs.
- Blog posts with no publisher, author, edition, or source trail.
- AI-generated Islamic content.
- User-pasted religious text treated as authoritative.
- Scraped app content without license review.
- Forums, comment sections, or debate pages.
- Any source not present in the Source Registry.

Disallowed sources may be logged as user-provided context, but they must not become religious authority inside DeenAI.

## No Invented Arabic

DeenAI must not generate Arabic religious wording from model memory.

Blocked behaviors:

- Writing Quran Arabic from memory.
- Completing missing Arabic words from a verse, hadith, dua, or adhkar.
- Creating a new Arabic dua and implying it is traditional.
- Translating into Arabic and implying the wording is religiously established.
- Mixing retrieved Arabic with generated Arabic commentary in a way that confuses source text with explanation.

Allowed behavior:

- Display Arabic only when retrieved from an approved source record.
- Label source text and explanation separately.
- Refuse or return source-missing state when the approved record is unavailable.

## No Invented Quran Or Hadith References

DeenAI must validate every Quran and hadith citation before display.

Quran rules:

- Use canonical surah and ayah identifiers.
- Reject impossible references.
- Do not invent verse text, translation, or topic mapping.
- Do not cite Quran passages that were not retrieved for the current request.

Hadith rules:

- Use provider record IDs, collection names, book/chapter metadata, and hadith numbers only from retrieved records.
- Do not invent collection numbers.
- Do not present remembered phrases as verified hadith without source match.
- Do not cite a hadith record as support for a claim it does not support.

## No Inferred Hadith Grading

Hadith grade display is allowed only when the retrieved source record includes grade metadata.

Blocked behaviors:

- Inferring grade from collection name alone.
- Reconciling differences between grading systems.
- Declaring a hadith authentic, weak, fabricated, or accepted from model memory.
- Adding confidence language that sounds like a scholarly grading.

Required behavior:

- If grade metadata exists, cite the source of the grade.
- If grade metadata is missing, say grade is unavailable in the retrieved source record.
- If the user asks for a ruling based on a hadith, escalate instead of ruling.

## Translation Licensing Cautions

Quran translations, hadith translations, dua translations, and transliterations can have separate rights from the Arabic source.

Rules:

- Track translator, edition, provider, source URL, permission note, and retrieval date.
- Do not assume a translation is public domain.
- Do not store translations locally unless terms allow it.
- Attribute each displayed translation.
- Keep Arabic, translation, transliteration, and explanation as separate fields.
- Do not paraphrase a translation and present it as the source text.

## Scholar Approval Disclaimer

DeenAI must not claim scholar approval unless a real approval workflow exists and is documented.

Required disclaimer:

```text
DeenAI is a source-grounded learning prototype. It is not scholar-approved and does not replace qualified scholars, teachers, local imams, or recognized institutions.
```

Do not imply approval through design, wording, badges, logos, or phrases such as:

- scholar verified
- fatwa certified
- officially approved
- authoritative ruling engine
- trusted by scholars

## Fatwa Limitation Policy

DeenAI must not issue fatwas or personal religious verdicts.

Refuse and escalate when the user asks:

- Is this halal or haram for me?
- Am I divorced?
- What is my inheritance distribution?
- Can I sign this finance contract?
- Did this person sin?
- Which sect is saved?
- Which ruling should I follow?
- What should I do in a personal high-stakes case?

Allowed alternative:

- Offer source lookup.
- Help organize questions for a qualified scholar.
- Explain that local context, personal facts, madhhab, law, and qualified review may matter.
- Provide neutral educational background only if sourced and not framed as a ruling.

## Citation Format

Every citation card must be source-specific and machine-checkable.

### Quran Citation

Required fields:

- provider
- source URL
- surah number
- ayah number
- Arabic edition if Arabic is displayed
- translation edition and translator if translation is displayed
- checksum or source version when stored locally
- retrieved date
- license note

Display format:

```text
Quran {surah_number}:{ayah_number} | {provider} | {edition or translation} | {source_url}
```

### Hadith Citation

Required fields:

- provider
- source URL
- collection
- book or chapter
- hadith number or provider record ID
- language or edition
- grade source if grade is displayed
- retrieved date
- license note

Display format:

```text
{collection} | {book_or_chapter} | {hadith_number_or_provider_id} | {provider} | {source_url}
```

### Dua Citation

Required fields:

- provider
- source URL
- collection or book
- chapter or category
- record ID
- Arabic text source
- translation source
- transliteration source if shown
- retrieved date
- license note

Display format:

```text
{collection_or_book} | {chapter_or_category} | {record_id} | {provider} | {source_url}
```

### Prayer Time Citation

Required fields:

- provider
- source URL
- location label
- date
- timezone
- calculation method
- school/asr setting if applicable
- latitude/longitude precision
- retrieved timestamp
- accuracy limitation

Display format:

```text
{provider} | {location_label} | {date} | {calculation_method} | {timezone}
```

## Source-Missing Behavior

When an approved source is unavailable, retrieval fails, or citation verification fails, DeenAI must not answer from memory.

User-facing fallback:

```text
I cannot answer this from approved sources right now. I can try another approved source, show a citation-only result, or mark this as a source review task.
```

## Recruiter-Facing Design Evidence

This policy should be shown as part of the DeenAI portfolio because it demonstrates:

- RAG source governance.
- High-risk domain safety design.
- Citation verifier requirements.
- Evaluation-driven development.
- Auditability with JSONL logs.
- Clear refusal and escalation boundaries.

The goal is not to claim religious authority. The goal is to prove that the system was designed to avoid pretending to have it.
