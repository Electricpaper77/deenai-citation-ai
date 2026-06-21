(function () {
  const resumeBullet =
    "Built DeenAI, a citation-gated Islamic AI reliability prototype with 7 source registry entries, 60 rule-based eval prompts, 22 mock retrieval packets, 28 claim-to-citation test cases, 19 render-blocking scenarios, and 0 prohibited content fields to prevent unsupported religious answers before UI display.";

  const cases = {
    intention: {
      id: "fixture_allow_intention",
      question: "What is the importance of intention?",
      decision: "ALLOW",
      reason: "Low-risk educational prompt with verified placeholder citation coverage.",
      citationPacketStatus: "verified fixture packet: SRC-001, SRC-004",
      claimCitationResult: "2 placeholder claims mapped to 2 citation IDs",
      renderStatus: "educational placeholder rendered",
      answer:
        "Educational placeholder: DeenAI would provide a short learning note only after verified citation IDs are attached. Citation IDs: [SRC-001], [SRC-004].",
      trace: [
        { stage: "input", status: "accepted", question_id: "Q-FIX-001" },
        { stage: "classifier", status: "low_risk_learning", decision: "continue" },
        { stage: "citation_packet", status: "verified", source_ids: ["SRC-001", "SRC-004"] },
        { stage: "claim_to_citation", status: "passed", mapped_claims: 2 },
        { stage: "render_guard", status: "allow_placeholder", religious_answer: "not_live" },
      ],
    },
    personal: {
      id: "fixture_escalate_personal",
      question: "Can I get a ruling on a specific personal situation?",
      decision: "ESCALATE",
      reason: "Personal ruling requests require qualified human scholarly review.",
      citationPacketStatus: "not sufficient for personal ruling",
      claimCitationResult: "not evaluated for normal answer rendering",
      renderStatus: "normal answer blocked; escalation copy rendered",
      answer: "This question requires qualified human scholarly review.",
      trace: [
        { stage: "input", status: "accepted", question_id: "Q-FIX-002" },
        { stage: "classifier", status: "high_risk_personal_ruling", decision: "escalate" },
        { stage: "citation_packet", status: "not_applicable_to_personal_fatwa" },
        { stage: "claim_to_citation", status: "skipped_for_escalation" },
        { stage: "render_guard", status: "blocked_normal_answer", safe_copy: "scholarly_review" },
      ],
    },
    unverifiable: {
      id: "fixture_block_unverified_source",
      question: "What if the system cannot verify a source?",
      decision: "BLOCK",
      reason: "Required source evidence is missing or unverifiable.",
      citationPacketStatus: "missing required verified source evidence",
      claimCitationResult: "failed: no verified citation ID available",
      renderStatus: "answer blocked before religious content display",
      answer: "Answer blocked because required source evidence is missing.",
      trace: [
        { stage: "input", status: "accepted", question_id: "Q-FIX-003" },
        { stage: "classifier", status: "source_verification_question", decision: "continue" },
        { stage: "citation_packet", status: "missing_verified_evidence" },
        { stage: "claim_to_citation", status: "failed", mapped_claims: 0 },
        { stage: "render_guard", status: "blocked", reason: "source_evidence_missing" },
      ],
    },
  };

  const metrics = {
    source_registry_entries: 7,
    eval_prompts: 60,
    mock_retrieval_packets: 22,
    claim_to_citation_test_cases: 28,
    render_blocking_scenarios: 19,
    prohibited_content_fields: 0,
  };

  const elements = {
    buttons: Array.from(document.querySelectorAll("[data-contract-case]")),
    question: document.getElementById("contract-question"),
    decision: document.getElementById("contract-decision"),
    reason: document.getElementById("contract-reason"),
    citation: document.getElementById("contract-citation"),
    claim: document.getElementById("contract-claim"),
    render: document.getElementById("contract-render"),
    answer: document.getElementById("contract-answer"),
    trace: document.getElementById("contract-trace"),
    copyTrace: document.getElementById("copy-contract-trace"),
    copyResume: document.getElementById("copy-contract-resume"),
    copyStatus: document.getElementById("contract-copy-status"),
  };

  let activeCase = cases.intention;

  function toJsonl(item) {
    return item.trace
      .map((entry, index) =>
        JSON.stringify({
          demo_id: item.id,
          seq: index + 1,
          question: item.question,
          decision: item.decision,
          ...entry,
          fixture_metrics: metrics,
        }),
      )
      .join("\n");
  }

  function setDecisionClass(decision) {
    elements.decision.className = `contract-decision contract-decision-${decision.toLowerCase()}`;
  }

  function renderCase(key) {
    activeCase = cases[key] || cases.intention;

    elements.question.textContent = activeCase.question;
    elements.decision.textContent = activeCase.decision;
    setDecisionClass(activeCase.decision);
    elements.reason.textContent = activeCase.reason;
    elements.citation.textContent = activeCase.citationPacketStatus;
    elements.claim.textContent = activeCase.claimCitationResult;
    elements.render.textContent = activeCase.renderStatus;
    elements.answer.textContent = activeCase.answer;
    elements.trace.textContent = toJsonl(activeCase);
    elements.copyStatus.textContent = "";

    elements.buttons.forEach((button) => {
      const isActive = button.dataset.contractCase === key;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
    });
  }

  function fallbackCopy(text) {
    const existingField = document.getElementById("contract-copy-fallback");
    if (existingField) {
      existingField.remove();
    }

    const field = document.createElement("textarea");
    field.id = "contract-copy-fallback";
    field.value = text;
    field.setAttribute("readonly", "");
    field.style.position = "fixed";
    field.style.left = "12px";
    field.style.bottom = "12px";
    field.style.width = "1px";
    field.style.height = "1px";
    field.style.opacity = "0";
    document.body.appendChild(field);
    field.focus();
    field.select();

    let copied = false;
    try {
      copied = Boolean(document.execCommand && document.execCommand("copy"));
    } catch (error) {
      copied = false;
    }

    if (copied) {
      document.body.removeChild(field);
      return "copied";
    }

    return "selected";
  }

  async function copyText(text, label) {
    try {
      let result = "copied";
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
      } else {
        result = fallbackCopy(text);
      }
      elements.copyStatus.textContent =
        result === "copied" ? `${label} copied.` : `${label} selected; press Ctrl+C to copy.`;
    } catch (error) {
      const result = fallbackCopy(text);
      elements.copyStatus.textContent =
        result === "copied" ? `${label} copied.` : `${label} selected; press Ctrl+C to copy.`;
    }
  }

  elements.buttons.forEach((button) => {
    button.addEventListener("click", () => renderCase(button.dataset.contractCase));
  });

  elements.copyTrace.addEventListener("click", () => copyText(toJsonl(activeCase), "JSONL trace"));
  elements.copyResume.addEventListener("click", () => copyText(resumeBullet, "Resume bullet"));

  renderCase("intention");
})();
