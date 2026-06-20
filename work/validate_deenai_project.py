from html.parser import HTMLParser
from pathlib import Path
import json
import re


ROOT = Path(__file__).resolve().parents[1]


REQUIRED_FILES = [
    "index.html",
    "ask.html",
    "how-it-works.html",
    "sources.html",
    "styles.css",
    "README.md",
    "PROJECT_STATUS.md",
]

REQUIRED_ARTIFACTS = [
    "sources/source_registry.json",
    "evals/deenai_eval_prompts.jsonl",
    "evals/pipeline_eval_traces.jsonl",
    "evals/pipeline_eval_summary.json",
    "evals/mock_retrieval_packets.jsonl",
    "evals/citation_verification_report.json",
    "evals/mock_claim_citation_cases.jsonl",
    "evals/claim_citation_verification_report.json",
    "evals/source_registry_validation_report.json",
]

UI_PAGES = [
    "index.html",
    "ask.html",
    "how-it-works.html",
    "sources.html",
]

USER_FACING_DOCS = UI_PAGES + [
    "README.md",
    "PROJECT_STATUS.md",
]

REQUIRED_LINKS = {
    "index.html": ["ask.html", "how-it-works.html", "sources.html"],
    "ask.html": ["index.html", "how-it-works.html", "sources.html"],
    "how-it-works.html": ["index.html", "ask.html", "sources.html"],
    "sources.html": ["index.html", "ask.html", "how-it-works.html"],
}

ASK_STATES = {
    "Citation-grounded": ["citation-grounded"],
    "Refusal": ["refusal"],
    "Scholar escalation": ["scholar escalation"],
    "Source-missing": ["source-missing"],
    "Verifier failed": ["verifier failed", "unsupported claim"],
}

REQUIRED_METRICS = {
    "60": "eval prompts",
    "22": "mock retrieval packets",
    "28": "claim-citation cases",
    "19": "blocked render cases",
    "0": "prohibited content fields",
}

OVERCLAIM_PATTERNS = [
    "scholar-approved",
    "fatwa engine",
    "production rag",
    "real model accuracy",
    "guaranteed authentic ruling",
]

PROHIBITED_UI_LABEL_PATTERNS = [
    r"\bquran_text\b",
    r"\bhadith_text\b",
    r"\bdua_text\b",
    r"\barabic\b",
    r"\btranslation\b",
    r"\btranslations\b",
    r"\btransliteration\b",
    r"\btransliterations\b",
    r"\bruling_text\b",
]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "a" and "href" in attrs:
            self.links.append(attrs["href"])


def read_text(path):
    return (ROOT / path).read_text(encoding="utf-8")


def parse_links(path):
    parser = LinkParser()
    parser.feed(read_text(path))
    return parser.links


def link_matches(links, target):
    return any(link == target or link.startswith(f"{target}#") for link in links)


def check_required_files():
    required = REQUIRED_FILES + REQUIRED_ARTIFACTS
    return [path for path in required if not (ROOT / path).exists()]


def collect_json_files():
    search_roots = ["sources", "evals", "schemas"]
    files = []
    for folder in search_roots:
        base = ROOT / folder
        if base.exists():
            files.extend(str(path.relative_to(ROOT)).replace("\\", "/") for path in base.rglob("*.json"))
    return sorted(set(files))


def collect_jsonl_files():
    files = []
    evals = ROOT / "evals"
    if evals.exists():
        files.extend(str(path.relative_to(ROOT)).replace("\\", "/") for path in evals.rglob("*.jsonl"))
    return sorted(set(files))


def validate_json_files(paths):
    errors = []
    for path in paths:
        try:
            json.loads(read_text(path))
        except Exception as exc:  # noqa: BLE001 - validator reports exact parse failure.
            errors.append(f"{path}: {exc}")
    return errors


def validate_jsonl_files(paths):
    errors = []
    for path in paths:
        file_path = ROOT / path
        try:
            with file_path.open("r", encoding="utf-8") as handle:
                for line_number, line in enumerate(handle, start=1):
                    if line.strip():
                        json.loads(line)
        except Exception as exc:  # noqa: BLE001 - validator reports exact parse failure.
            errors.append(f"{path}: line {locals().get('line_number', '?')}: {exc}")
    return errors


def check_links():
    broken = []
    missing_required = []

    for page, targets in REQUIRED_LINKS.items():
        links = parse_links(page)
        for target in targets:
            if not link_matches(links, target):
                missing_required.append(f"{page} -> {target}")

        for link in links:
            if link.startswith("#"):
                continue
            target = link.split("#", 1)[0]
            if target and not (ROOT / target).exists():
                broken.append(f"{page}: {link}")

    return missing_required, broken


def check_ask_states():
    text = read_text("ask.html").lower()
    missing = []
    for label, needles in ASK_STATES.items():
        if not all(needle in text for needle in needles):
            missing.append(label)
    return missing


def check_metrics():
    missing = []
    for page in UI_PAGES:
        text = read_text(page).lower()
        for number, label in REQUIRED_METRICS.items():
            if number not in text or label not in text:
                missing.append(f"{page}: {number} {label}")
    return missing


def check_overclaims():
    warnings = []
    for path in USER_FACING_DOCS:
        text = read_text(path).lower()
        for phrase in OVERCLAIM_PATTERNS:
            if phrase in text:
                warnings.append(f"{path}: {phrase}")
    return warnings


def check_prohibited_ui_labels():
    warnings = []
    for path in UI_PAGES:
        text = read_text(path).lower()
        for pattern in PROHIBITED_UI_LABEL_PATTERNS:
            if re.search(pattern, text):
                warnings.append(f"{path}: {pattern}")
    return warnings


def print_check(name, passed, detail=None):
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name}")
    if detail:
        for item in detail:
            print(f"  - {item}")


def main():
    missing_files = check_required_files()
    json_files = collect_json_files()
    jsonl_files = collect_jsonl_files()
    json_errors = validate_json_files(json_files)
    jsonl_errors = validate_jsonl_files(jsonl_files)
    missing_required_links, broken_links = check_links()
    missing_states = check_ask_states()
    missing_metrics = check_metrics()
    overclaim_warnings = check_overclaims()
    prohibited_ui_warnings = check_prohibited_ui_labels()

    print("DeenAI full static proof MVP validation")
    print("=" * 44)
    print_check("Required files exist", not missing_files, missing_files)
    print_check("JSON files parse", not json_errors, json_errors)
    print_check("JSONL files parse line-by-line", not jsonl_errors, jsonl_errors)
    print_check("Required page links exist", not missing_required_links, missing_required_links)
    print_check("No broken local links", not broken_links, broken_links)
    print_check("Ask DeenAI states exist", not missing_states, missing_states)
    print_check("Proof metrics appear consistently", not missing_metrics, missing_metrics)
    print_check("No prohibited overclaim phrases", not overclaim_warnings, overclaim_warnings)
    print_check("No prohibited UI content field labels", not prohibited_ui_warnings, prohibited_ui_warnings)

    print()
    print(f"JSON files checked: {len(json_files)}")
    print(f"JSONL files checked: {len(jsonl_files)}")

    failed = any(
        [
            missing_files,
            json_errors,
            jsonl_errors,
            missing_required_links,
            broken_links,
            missing_states,
            missing_metrics,
            overclaim_warnings,
            prohibited_ui_warnings,
        ]
    )

    print(f"Final result: {'FAIL' if failed else 'PASS'}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
