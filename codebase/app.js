const terms = {
  token: {
    title: "Token",
    level: "Foundation",
    confidence: "high",
    definition:
      "A token is a small text unit that the model reads, such as a word, sub-word, punctuation mark, or special marker.",
    example: "In the phrase 'AI tutor', the model may split the text into tokens before doing any reasoning.",
    source: "Slide 12: 'A sentence is split into tokens.'",
    related: ["embedding"],
    reason: "Start here because embeddings and attention both operate on token representations.",
  },
  embedding: {
    title: "Embedding",
    level: "Intermediate",
    confidence: "high",
    definition:
      "An embedding is a numeric vector that represents a token so the model can compare meaning and context mathematically.",
    example: "The token 'student' becomes a vector before it is passed into the attention layer.",
    source: "Slide 12: 'Each token is mapped to an embedding.'",
    related: ["token", "attention"],
    reason: "Learn this after token because embeddings are created from tokens.",
  },
  attention: {
    title: "Attention",
    level: "Application",
    confidence: "high",
    definition:
      "Attention is the mechanism that lets a model compare each token representation with other token representations in the sequence.",
    example: "In 'the student asked because they were confused', attention helps connect 'they' back to 'student'.",
    source: "Slide 12: 'The model uses attention to compare context across the sequence.'",
    related: ["token", "embedding", "loss"],
    reason: "Learn this after token and embedding because attention uses their vector representations.",
  },
  loss: {
    title: "Loss",
    level: "Ambiguous",
    confidence: "low",
    definition:
      "In this topic, loss likely means the training signal that measures prediction error, but this slide does not define it directly.",
    example: "A lower loss usually means the model prediction is closer to the expected answer.",
    source: "Weak source: mentioned in nearby class discussion, not on Slide 12.",
    related: ["attention"],
    reason: "Low confidence: only show a limited explanation and ask the learner to verify with tutor/lecturer.",
  },
};

const learningOrder = ["token", "embedding", "attention"];
let selectedTerm = "token";

const termList = document.querySelector("#termList");
const termDetail = document.querySelector("#termDetail");
const learningOrderEl = document.querySelector("#learningOrder");
const toast = document.querySelector("#toast");
const customTerm = document.querySelector("#customTerm");

function confidenceLabel(value) {
  if (value === "high") return "High confidence";
  if (value === "low") return "Low confidence";
  return "No grounding";
}

function renderLearningOrder() {
  learningOrderEl.innerHTML = learningOrder
    .map((key, index) => {
      const term = terms[key];
      return `
        <li>
          <span class="step-index">${index + 1}</span>
          <span class="step-title">${term.title}</span>
          <span class="step-reason">${term.reason}</span>
        </li>
      `;
    })
    .join("");
}

function renderTermList() {
  termList.innerHTML = Object.entries(terms)
    .map(([key, term]) => {
      const activeClass = key === selectedTerm ? " active" : "";
      return `
        <button class="term-button${activeClass}" type="button" data-term="${key}">
          <strong>${term.title}</strong>
          <span>${term.level} · ${confidenceLabel(term.confidence)}</span>
        </button>
      `;
    })
    .join("");
}

function renderDetail(termKey) {
  const term = terms[termKey];

  if (!term) {
    termDetail.innerHTML = `
      <div class="detail-top">
        <div>
          <p class="eyebrow">No grounding</p>
          <h2>${escapeHtml(customTerm.value || "Unknown term")}</h2>
        </div>
        <span class="confidence none">No grounding</span>
      </div>
      <p class="definition">
        Chưa tìm thấy căn cứ trong slide/video/topic hiện tại. Prototype không tự bịa định nghĩa.
      </p>
      <div class="mini-card">
        <h3>Next step</h3>
        <p>Hỏi tutor/giảng viên hoặc chuyển sang tìm kiếm ngoài bài nếu được phép.</p>
      </div>
    `;
    return;
  }

  const confidenceClass = term.confidence === "high" ? "high" : "low";
  const relatedButtons = term.related
    .map((key) => `<button type="button" data-related="${key}">${terms[key].title}</button>`)
    .join("");

  termDetail.innerHTML = `
    <div class="detail-top">
      <div>
        <p class="eyebrow">${term.level}</p>
        <h2>${term.title}</h2>
      </div>
      <span class="confidence ${confidenceClass}">${confidenceLabel(term.confidence)}</span>
    </div>

    <p class="definition">${term.definition}</p>

    <div class="detail-grid">
      <div class="mini-card">
        <h3>Example in this lesson</h3>
        <p>${term.example}</p>
      </div>
      <div class="mini-card">
        <h3>Why this order</h3>
        <p>${term.reason}</p>
      </div>
    </div>

    <p class="source-line">Grounding: ${term.source}</p>

    <div class="related-list" aria-label="Related concepts">
      ${relatedButtons}
    </div>

    <div class="actions">
      <button class="action-button" type="button" data-action="correct">Đề xuất sửa</button>
      <button class="action-button secondary" type="button" data-action="hide">Ẩn thuật ngữ</button>
    </div>
  `;
}

function selectTerm(key) {
  selectedTerm = key;
  renderTermList();
  renderDetail(key);
}

function showToast(message) {
  toast.textContent = message;
  toast.classList.add("visible");
  window.clearTimeout(showToast.timer);
  showToast.timer = window.setTimeout(() => toast.classList.remove("visible"), 2600);
}

function escapeHtml(value) {
  return value.replace(/[&<>"']/g, (char) => {
    const map = {
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#039;",
    };
    return map[char];
  });
}

document.querySelector("#openGlossary").addEventListener("click", () => {
  document.querySelector(".glossary-pane").scrollIntoView({ behavior: "smooth", block: "start" });
  showToast("Glossary mở sẵn với thứ tự học đề xuất.");
});

termList.addEventListener("click", (event) => {
  const button = event.target.closest("[data-term]");
  if (!button) return;
  selectTerm(button.dataset.term);
});

termDetail.addEventListener("click", (event) => {
  const related = event.target.closest("[data-related]");
  if (related) {
    selectTerm(related.dataset.related);
    return;
  }

  const action = event.target.closest("[data-action]");
  if (!action) return;

  if (action.dataset.action === "correct") {
    showToast("Đã ghi nhận góp ý sửa định nghĩa ở trạng thái chờ kiểm tra.");
  }

  if (action.dataset.action === "hide") {
    showToast("Thuật ngữ đã được ẩn khỏi glossary cá nhân của bài học.");
  }
});

document.querySelector("#askTerm").addEventListener("click", () => {
  const value = customTerm.value.trim().toLowerCase();
  const matchedKey = Object.keys(terms).find((key) => key === value);
  if (matchedKey) {
    selectTerm(matchedKey);
  } else {
    selectedTerm = "";
    renderTermList();
    renderDetail(null);
  }
});

customTerm.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    document.querySelector("#askTerm").click();
  }
});

renderLearningOrder();
renderTermList();
renderDetail(selectedTerm);
