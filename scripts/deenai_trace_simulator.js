(function () {
  const riskWeights = {
    baseLearning: 10,
    citationRequiredButMissing: 15,
    sourceMissing: 35,
    unsupportedClaim: 40,
    inventedOrFakeCitation: 90,
    highRiskRuling: 75,
    sectarianBait: 70,
  };

  const traceCases = {
    dua: {
      promptType: "Dua recommendation",
      intent: "Islamic learning",
      citationRequired: true,
      citationRequiredButMissing: false,
      sourceMissing: false,
      unsupportedClaim: false,
      inventedOrFakeCitation: false,
      highRiskRuling: false,
      sectarianBait: false,
      citationBypass: false,
      verifiedSourceMetadata: true,
      correctSourceType: true,
      claimMappedToSourceId: true,
      sourcePacketStatus: "verified metadata",
      claimSupportStatus: "mapped to source ID",
      reason: "Risk is below threshold and citation score meets render requirements.",
    },
    quran: {
      promptType: "Quran explanation",
      intent: "Islamic learning",
      citationRequired: true,
      citationRequiredButMissing: true,
      sourceMissing: true,
      unsupportedClaim: false,
      inventedOrFakeCitation: false,
      highRiskRuling: false,
      sectarianBait: false,
      citationBypass: false,
      verifiedSourceMetadata: false,
      correctSourceType: true,
      claimMappedToSourceId: false,
      sourcePacketStatus: "missing verified metadata",
      claimSupportStatus: "blocked until source packet exists",
      reason: "Citation is required, but no verified source packet is available.",
    },
    invented: {
      promptType: "Invented Hadith request",
      intent: "source invention attempt",
      citationRequired: true,
      citationRequiredButMissing: true,
      sourceMissing: false,
      unsupportedClaim: true,
      inventedOrFakeCitation: true,
      highRiskRuling: false,
      sectarianBait: false,
      citationBypass: false,
      verifiedSourceMetadata: false,
      correctSourceType: false,
      claimMappedToSourceId: false,
      sourcePacketStatus: "blocked source invention",
      claimSupportStatus: "unsupported placeholder claim",
      reason: "Invented or fake religious source requests are refused before answer rendering.",
    },
    "high-risk": {
      promptType: "High-risk ruling request",
      intent: "high-risk fiqh category",
      citationRequired: true,
      citationRequiredButMissing: false,
      sourceMissing: false,
      unsupportedClaim: false,
      inventedOrFakeCitation: false,
      highRiskRuling: true,
      sectarianBait: false,
      citationBypass: false,
      verifiedSourceMetadata: true,
      correctSourceType: true,
      claimMappedToSourceId: true,
      sourcePacketStatus: "verified metadata",
      claimSupportStatus: "mapped, but normal answer blocked",
      reason: "High-risk ruling categories are escalated instead of rendered as normal answers.",
    },
    bypass: {
      promptType: "Citation bypass request",
      intent: "citation bypass attempt",
      citationRequired: true,
      citationRequiredButMissing: true,
      sourceMissing: false,
      unsupportedClaim: true,
      inventedOrFakeCitation: false,
      highRiskRuling: false,
      sectarianBait: false,
      citationBypass: true,
      verifiedSourceMetadata: false,
      correctSourceType: false,
      claimMappedToSourceId: false,
      sourcePacketStatus: "citation requirement bypassed",
      claimSupportStatus: "unsupported placeholder claim",
      reason: "Requests to bypass citation requirements are refused before answer rendering.",
    },
  };

  const elements = {
    decisionTitle: document.getElementById("trace-decision-title"),
    decisionBadge: document.getElementById("trace-decision-badge"),
    riskScore: document.getElementById("trace-risk-score"),
    citationScore: document.getElementById("trace-citation-score"),
    promptType: document.getElementById("trace-prompt-type"),
    intent: document.getElementById("trace-intent"),
    riskLevel: document.getElementById("trace-risk-level"),
    citationRequired: document.getElementById("trace-citation-required"),
    sourceStatus: document.getElementById("trace-source-status"),
    claimStatus: document.getElementById("trace-claim-status"),
    guardrailDecision: document.getElementById("trace-guardrail-decision"),
    renderDecision: document.getElementById("trace-render-decision"),
    reason: document.getElementById("trace-reason"),
    chain: document.getElementById("trace-chain"),
  };

  function calculateRiskScore(trace) {
    let score = riskWeights.baseLearning;

    if (trace.citationRequiredButMissing) {
      score += riskWeights.citationRequiredButMissing;
    }
    if (trace.sourceMissing) {
      score += riskWeights.sourceMissing;
    }
    if (trace.unsupportedClaim) {
      score += riskWeights.unsupportedClaim;
    }
    if (trace.inventedOrFakeCitation) {
      score += riskWeights.inventedOrFakeCitation;
    }
    if (trace.highRiskRuling) {
      score += riskWeights.highRiskRuling;
    }
    if (trace.sectarianBait) {
      score += riskWeights.sectarianBait;
    }

    return score;
  }

  function calculateCitationScore(trace) {
    let score = 0;

    if (trace.verifiedSourceMetadata) {
      score += 40;
    }
    if (trace.correctSourceType) {
      score += 30;
    }
    if (trace.claimMappedToSourceId) {
      score += 30;
    }

    return Math.min(score, 100);
  }

  function getRiskLevel(score) {
    if (score < 35) {
      return "low";
    }
    if (score < 70) {
      return "medium";
    }
    return "high";
  }

  function decide(trace, riskScore, citationScore) {
    if (trace.inventedOrFakeCitation || trace.citationBypass) {
      return {
        decision: "REFUSE",
        guardrail: "refuse",
        render: "blocked",
      };
    }

    if (trace.highRiskRuling) {
      return {
        decision: "ESCALATE",
        guardrail: "escalate",
        render: "blocked from normal answer",
      };
    }

    if (trace.citationRequired && trace.sourceMissing) {
      return {
        decision: "SOURCE_MISSING",
        guardrail: "source missing",
        render: "blocked",
      };
    }

    if (!trace.claimMappedToSourceId || !trace.correctSourceType) {
      return {
        decision: "VERIFIER_FAILED",
        guardrail: "verifier failed",
        render: "blocked",
      };
    }

    if (riskScore < 35 && citationScore >= 80) {
      return {
        decision: "ALLOW",
        guardrail: "allow",
        render: "allowed",
      };
    }

    return {
      decision: "VERIFIER_FAILED",
      guardrail: "verifier failed",
      render: "blocked",
    };
  }

  function formatDecisionClass(decision) {
    return `decision-badge decision-${decision.toLowerCase().replace(/_/g, "-")}`;
  }

  function renderChain(trace, decisionResult) {
    const steps = [
      ["Input", trace.promptType],
      ["Classifier", trace.intent],
      ["Retrieval Packet", trace.sourcePacketStatus],
      ["Citation Check", trace.claimSupportStatus],
      ["Guardrail", decisionResult.guardrail],
      ["Render Decision", decisionResult.render],
    ];

    elements.chain.innerHTML = steps
      .map(
        ([label, value]) => `
          <li>
            <span>${label}</span>
            <strong>${value}</strong>
          </li>
        `,
      )
      .join("");
  }

  function renderTrace(id) {
    const trace = traceCases[id] || traceCases.dua;
    const riskScore = calculateRiskScore(trace);
    const citationScore = calculateCitationScore(trace);
    const decisionResult = decide(trace, riskScore, citationScore);

    elements.decisionTitle.textContent = decisionResult.decision;
    elements.decisionBadge.textContent = decisionResult.decision;
    elements.decisionBadge.className = formatDecisionClass(decisionResult.decision);
    elements.riskScore.textContent = String(riskScore);
    elements.citationScore.textContent = String(citationScore);
    elements.promptType.textContent = trace.promptType;
    elements.intent.textContent = trace.intent;
    elements.riskLevel.textContent = getRiskLevel(riskScore);
    elements.citationRequired.textContent = trace.citationRequired ? "yes" : "no";
    elements.sourceStatus.textContent = trace.sourcePacketStatus;
    elements.claimStatus.textContent = trace.claimSupportStatus;
    elements.guardrailDecision.textContent = decisionResult.guardrail;
    elements.renderDecision.textContent = decisionResult.render;
    elements.reason.textContent = trace.reason;
    renderChain(trace, decisionResult);
  }

  function bindTraceChips() {
    const chips = document.querySelectorAll("[data-trace-prompt]");

    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        chips.forEach((item) => item.classList.remove("active"));
        chip.classList.add("active");
        renderTrace(chip.dataset.tracePrompt);
      });
    });
  }

  bindTraceChips();
  renderTrace("dua");
})();
