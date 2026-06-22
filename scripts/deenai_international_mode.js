(function () {
  const translations = {
    en: {
      askPreview: "Ask DeenAI Preview",
      safetyTraceSimulator: "Safety Trace Simulator",
      allow: "ALLOW",
      refuse: "REFUSE",
      escalate: "ESCALATE",
      sourceMissing: "SOURCE MISSING",
      verifierFailed: "VERIFIER FAILED",
      citationRequired: "Citation required",
      sourcePacketVerified: "Source packet verified",
      claimMapped: "Claim mapped to source ID",
      blockedBeforeDisplay: "Blocked before answer display",
      placeholderOnly: "Placeholder only",
      noLiveBoundary: "No live LLM / no live RAG / no religious ruling",
      chipUiOnly: "UI localization only",
      chipNoFatwa: "No live fatwa",
      chipNoLlm: "No live LLM",
      chipLicensing: "Source licensing required",
      chipCitationGate: "Citation gate required",
      localizedDisclaimer:
        "This multilingual preview localizes the interface only. It does not translate religious source content, issue rulings, or generate Islamic answers.",
      terms: {
        islam: "Islam",
        quran: "Quran",
        hadith: "Hadith",
        dua: "Dua",
        fatwa: "Fatwa",
        scholar: "Scholar",
        citation: "Citation",
        sourceVerification: "Source verification",
      },
    },
    ja: {
      askPreview: "Ask DeenAI プレビュー",
      safetyTraceSimulator: "安全性トレース・シミュレーター",
      allow: "許可",
      refuse: "拒否",
      escalate: "エスカレーション",
      sourceMissing: "出典未確認",
      verifierFailed: "検証失敗",
      citationRequired: "引用が必要",
      sourcePacketVerified: "出典パケット確認済み",
      claimMapped: "主張を出典IDに対応付け",
      blockedBeforeDisplay: "回答表示前にブロック",
      placeholderOnly: "プレースホルダーのみ",
      noLiveBoundary: "ライブLLMなし / ライブRAGなし / 宗教判断なし",
      chipUiOnly: "UI翻訳のみ",
      chipNoFatwa: "ライブ・ファトワーなし",
      chipNoLlm: "ライブLLMなし",
      chipLicensing: "出典ライセンスが必要",
      chipCitationGate: "引用ゲートが必要",
      localizedDisclaimer:
        "この多言語プレビューはインターフェースのみを翻訳します。宗教的な原典の翻訳、宗教判断、またはイスラム回答の生成は行いません。",
      terms: {
        islam: "イスラム",
        quran: "クルアーン",
        hadith: "ハディース",
        dua: "ドゥアー",
        fatwa: "ファトワー",
        scholar: "学者",
        citation: "引用",
        sourceVerification: "出典確認",
      },
    },
    "zh-Hans": {
      askPreview: "Ask DeenAI 预览",
      safetyTraceSimulator: "安全追踪模拟器",
      allow: "允许",
      refuse: "拒绝",
      escalate: "升级处理",
      sourceMissing: "来源缺失",
      verifierFailed: "验证失败",
      citationRequired: "需要引用",
      sourcePacketVerified: "来源包已验证",
      claimMapped: "声明已映射到来源 ID",
      blockedBeforeDisplay: "在答案显示前阻止",
      placeholderOnly: "仅占位",
      noLiveBoundary: "无实时 LLM / 无实时 RAG / 无宗教裁决",
      chipUiOnly: "仅 UI 翻译",
      chipNoFatwa: "无实时法特瓦",
      chipNoLlm: "无实时 LLM",
      chipLicensing: "需要来源许可",
      chipCitationGate: "需要引用门控",
      localizedDisclaimer:
        "此多语言预览仅本地化界面内容。它不翻译宗教原文、不发布宗教裁决，也不生成伊斯兰教义回答。",
      terms: {
        islam: "伊斯兰",
        quran: "古兰经",
        hadith: "圣训",
        dua: "杜阿",
        fatwa: "法特瓦",
        scholar: "学者",
        citation: "引用",
        sourceVerification: "来源验证",
      },
    },
  };

  const decisionKeyByClass = [
    ["decision-allow", "allow"],
    ["decision-refuse", "refuse"],
    ["decision-escalate", "escalate"],
    ["decision-source-missing", "sourceMissing"],
    ["decision-verifier-failed", "verifierFailed"],
  ];

  const buttons = document.querySelectorAll("[data-lang]");
  const decisionTitle = document.getElementById("trace-decision-title");
  const decisionBadge = document.getElementById("trace-decision-badge");
  let currentLanguage = "en";
  let translatingDecision = false;

  function getSupportedLanguage(language) {
    return Object.prototype.hasOwnProperty.call(translations, language) ? language : "en";
  }

  function getDecisionTranslationKey() {
    if (!decisionBadge) {
      return null;
    }

    const matched = decisionKeyByClass.find(([className]) => decisionBadge.classList.contains(className));
    return matched ? matched[1] : null;
  }

  function translateDecisionElement(element, translationKey) {
    if (!element) {
      return;
    }

    const languagePack = translations[currentLanguage];
    if (!translationKey) {
      return;
    }

    const translatedText = languagePack[translationKey];
    if (element.textContent !== translatedText) {
      element.textContent = translatedText;
    }
  }

  function translateDecision() {
    const translationKey = getDecisionTranslationKey();

    translatingDecision = true;
    translateDecisionElement(decisionTitle, translationKey);
    translateDecisionElement(decisionBadge, translationKey);
    translatingDecision = false;
  }

  function applyTranslations(language) {
    const languagePack = translations[language];

    document.documentElement.lang = language;
    document.querySelectorAll("[data-i18n]").forEach((element) => {
      const key = element.dataset.i18n;
      if (languagePack[key]) {
        element.textContent = languagePack[key];
      }
    });

    document.querySelectorAll("[data-term]").forEach((element) => {
      const key = element.dataset.term;
      if (languagePack.terms[key]) {
        element.textContent = languagePack.terms[key];
      }
    });

    buttons.forEach((button) => {
      const isActive = button.dataset.lang === language;
      button.classList.toggle("active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
    });

    translateDecision();
  }

  function syncUrl(language) {
    const url = new URL(window.location.href);
    if (language === "en") {
      url.searchParams.delete("lang");
    } else {
      url.searchParams.set("lang", language);
    }
    window.history.replaceState({}, "", url);
  }

  function setLanguage(language, shouldSyncUrl) {
    currentLanguage = getSupportedLanguage(language);
    applyTranslations(currentLanguage);
    if (shouldSyncUrl) {
      syncUrl(currentLanguage);
    }
  }

  buttons.forEach((button) => {
    button.addEventListener("click", () => {
      setLanguage(button.dataset.lang, true);
    });
  });

  [decisionTitle, decisionBadge].forEach((element) => {
    if (!element) {
      return;
    }

    const observer = new MutationObserver(() => {
      if (!translatingDecision) {
        translateDecision();
      }
    });
    observer.observe(element, { attributes: true, childList: true, subtree: true });
  });

  document.querySelectorAll("[data-trace-prompt]").forEach((button) => {
    button.addEventListener("click", () => {
      window.setTimeout(translateDecision, 0);
    });
  });

  const urlLanguage = new URLSearchParams(window.location.search).get("lang");
  setLanguage(urlLanguage || "en", false);
})();
