const API = "http://localhost:5000/analyze";

// Sample texts
const SAMPLE_TEXTS = {
  1: `Malaysia\nFrom Wikipedia, the free encyclopedia\nMalaysia is a federal constitutional monarchy located in Southeast Asia. It consists of thirteen states and three federal territories and has a total landmass of 329,847 square kilometres (127,350 sq mi) separated by the South China Sea into two similarly sized regions, Peninsular Malaysia and East Malaysia (Malaysian Borneo). Peninsular Malaysia shares a land and maritime border with Thailand and maritime borders with Singapore, Vietnam, and Indonesia. East Malaysia shares land and maritime borders with Brunei and Indonesia and a maritime border with the Philippines. The capital city is Kuala Lumpur, while Putrajaya is the seat of the federal government. By 2015, with a population of over 30 million, Malaysia became 43rd most populous country in the world. The southernmost point of continental Eurasia, Tanjung Piai, is in Malaysia, located in the tropics. It is one of 17 megadiverse countries on earth, with large numbers of endemic species.\n\nMalaysia has its origins in the Malay kingdoms present in the area which, from the 18th century, became subject to the British Empire. The first British territories were known as the Straits Settlements, whose establishment was followed by the Malay kingdoms becoming British protectorates. The territories on Peninsular Malaysia were first unified as the Malayan Union in 1946. Malaya was restructured as the Federation of Malaya in 1948, and achieved independence on 31 August 1957. Malaya united with North Borneo, Sarawak, and Singapore on 16 September 1963, with is being added to give the new country the name Malaysia. Less than two years later in 1965, Singapore was expelled from the federation.\n\nSince its independence, Malaysia has had one of the best economic records in Asia, with its GDP growing at an average of 6.5% per annum for almost 50 years. The economy has traditionally been fuelled by its natural resources, but is expanding in the sectors of science, tourism, commerce and medical tourism. Today, Malaysia has a newly industrialised market economy, ranked third largest in Southeast Asia and 29th largest in the world. It is a founding member of the Association of Southeast Asian Nations, the East Asia Summit and the Organisation of Islamic Cooperation, and a member of Asia-Pacific Economic Cooperation, the Commonwealth of Nations, and the Non-Aligned Movement.`,
  2: `The 3rd International Workshop on Machine Learning and Knowledge Graphs (MLKgraphs2021)\nSeptember 27 - 30, 2021 - Linz, Austria\nhttp://www.dexa.org/mlkgraphs2021\nemail: dexa@iiwas.org\nPapers submission: https://easychair.org/conferences/?conf=mlkgraphs2021\n\n**** IMPORTANT DATES ****\nPaper submission: April 23, 2021 (SHARP)\nNotification of acceptance: June 1, 2021\nCamera-ready copies due: June 30, 2021\n\n*** PUBLICATION ***\nAll accepted papers will be published by Springer in "Communications in Computer and Information Science".\n\n*** SCOPE ***\nKnowledge Graphs are becoming a key technology for large-scale information processing systems containing massive collections of interrelated facts. Specifically, Knowledge Graphs provide the means for development of the newest data methods for data management, data fusion, data merging, and graph optimization and modeling, serving as a source of high quality data and a base for web-scale information integration.\n\nThe 3rd International Workshop on Machine Learning and Knowledge Graphs aims to be a meeting point for researchers and practitioners working on the latest advances in the intersection of machine learning technologies and knowledge graphs. Therefore, we welcome submissions of novel research that brings together the two topics of Machine Learning (ML) and Knowledge Graphs (KGs) either applying ML models for semantic data management structures (like KGs or ontologies), or by presenting newly assembled Knowledge Graphs that support the task of Machine Learning for certain application domains. Examples areas are Business Analytics, Customer Relationship Management, Fault Detection, Industry 4.0, or Social Networking.`,
  3: `Overall, the experience is fair for the price you pay. What makes it meaningful to me is that more than 10 years ago, there weren't many Japanese food options around, and Sushi King was one of the first places I tried. It became the go-to spot for sushi when choices were limited, and it introduced many of us to simple, affordable Japanese cuisine.\n\nThe quality of the food is decent, though not exceptional compared to today's wide variety of Japanese restaurants. Still, their menu has been consistent over the years, and the pricing is reasonable for casual dining. Service is usually quick, and the environment feels approachable for both families and groups of friends.`,
};

const inputText = document.getElementById("inputText");
const processBtn = document.getElementById("processBtn");
const backBtn = document.getElementById("backBtn");
const countBadge = document.getElementById("countBadge");
const totalHighlight = document.getElementById("totalHighlight");
const statusInline = document.getElementById("statusInline");
const statusMessage = document.getElementById("statusMessage");
const statsChips = document.getElementById("statsChips");
const visualisedText = document.getElementById("visualisedText");
const detailedTbody = document.querySelector("#detailedTable tbody");
const traceBody = document.getElementById("traceBody");

function escapeHtml(str = "") {
  return str.replace(
    /[&<>]/g,
    (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" })[c],
  );
}

function getPreviewHtml(text, start, end) {
  const ps = Math.max(0, start - 25),
    pe = Math.min(text.length, end + 25);
  const before = (ps > 0 ? "…" : "") + text.substring(ps, start);
  const word = text.substring(start, end + 1);
  const after = text.substring(end + 1, pe) + (pe < text.length ? "…" : "");
  return `${escapeHtml(before)}<span class="preview-highlight">${escapeHtml(word)}</span>${escapeHtml(after)}`;
}

function highlightAllMatches(text, matches) {
  if (!matches.length) return escapeHtml(text);
  let html = "",
    last = 0;
  for (const m of [...matches].sort((a, b) => a.start - b.start)) {
    html += escapeHtml(text.substring(last, m.start));
    html += `<span class="highlight">${escapeHtml(m.word)}</span>`;
    last = m.end + 1;
  }
  return html + escapeHtml(text.substring(last));
}

// Page navigation
function showPage(id) {
  document
    .querySelectorAll(".page")
    .forEach((p) => p.classList.remove("active"));
  document.getElementById(id).classList.add("active");
}

// Tab switching
document.querySelectorAll(".tab-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const tab = btn.dataset.tab;
    document
      .querySelectorAll(".tab-btn")
      .forEach((b) => b.classList.remove("active"));
    btn.classList.add("active");
    document
      .querySelectorAll(".tab-content")
      .forEach((t) => t.classList.remove("active"));
    document.getElementById(tab + "Tab").classList.add("active");
  });
});

document.querySelectorAll(".sample-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    const txt = SAMPLE_TEXTS[btn.dataset.sample];
    if (txt) {
      inputText.value = txt;
      // Clear the file selection UI when sample is chosen
      clearFileSelection();
    }
  });
});

// File drag-and-drop
let currentFileName = null;

function clearFileSelection() {
  const dragContent = document.getElementById("dragDropContent");
  const fileInfo = document.getElementById("selectedFileInfo");
  const fileInput = document.getElementById("fileUpload");

  dragContent.style.display = "block";
  fileInfo.style.display = "none";
  fileInput.value = "";
  currentFileName = null;
}

function showFileSelection(name) {
  const dragContent = document.getElementById("dragDropContent");
  const fileInfo = document.getElementById("selectedFileInfo");
  const fileNameSpan = document.getElementById("fileNameDisplay");

  dragContent.style.display = "none";
  fileInfo.style.display = "flex";
  fileNameSpan.textContent = name;
  currentFileName = name;
}

(function setupFileDrop() {
  const dropZone = document.getElementById("dropZone");
  const fileInput = document.getElementById("fileUpload");
  const clearBtn = document.getElementById("clearFileBtn");

  function loadFile(file) {
    if (!file || !file.name.endsWith(".txt")) {
      alert("Please use a .txt file");
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      inputText.value = e.target.result;
      showFileSelection(file.name);
    };
    reader.readAsText(file);
  }

  clearBtn.addEventListener("click", () => {
    clearFileSelection();
    inputText.value = "";
  });

  fileInput.addEventListener("change", (e) => {
    if (e.target.files[0]) loadFile(e.target.files[0]);
  });

  dropZone.addEventListener("dragover", (e) => {
    e.preventDefault();
    dropZone.classList.add("drag-over");
  });

  dropZone.addEventListener("dragleave", () => {
    dropZone.classList.remove("drag-over");
  });

  dropZone.addEventListener("drop", (e) => {
    e.preventDefault();
    dropZone.classList.remove("drag-over");
    if (e.dataTransfer.files[0]) loadFile(e.dataTransfer.files[0]);
  });
})();

// Results
function renderResults(text, data) {
  const { status, total, matches, trace, counts } = data;

  // Badge & totals
  countBadge.textContent = total;
  totalHighlight.textContent = total;

  // Status
  const accepted = status === "ACCEPTED";
  statusInline.textContent = status;
  statusInline.className = "status-inline " + (accepted ? "accept" : "reject");
  statusMessage.textContent = accepted
    ? "It contains stop words."
    : "It contains no stop words.";

  // Per-word chips
  statsChips.innerHTML = counts.length
    ? counts
        .map(
          ({ word, count }) =>
            `<div class="stat-chip"><span class="stat-word">${escapeHtml(word)}</span><span class="stat-count">${count}</span></div>`,
        )
        .join("")
    : '<span class="trace-note">No stop words found</span>';

  // Boldface visualisation
  visualisedText.innerHTML = highlightAllMatches(text, matches);

  // Detail table – pattern, position, occurrences
  detailedTbody.innerHTML = matches.length
    ? matches
        .map(
          (m, i) =>
            `<tr>
          <td>${i + 1}</td>
          <td><strong>${escapeHtml(m.lower)}</strong></td>
          <td>${m.start} – ${m.end}</td>
          <td class="preview-text">${getPreviewHtml(text, m.start, m.end)}</td>
        </tr>`,
        )
        .join("")
    : '<tr><td colspan="4" style="text-align:center">No stop words found</td></tr>';

  // DFA trace table
  traceBody.innerHTML = trace
    .map(
      (t) =>
        `<tr>
        <td>${escapeHtml(t.char)}</td>
        <td>${t.fromState} → ${t.toState}</td>
        <td>${escapeHtml(t.action)}</td>
      </tr>`,
    )
    .join("");
}

// Call backend
async function analyzeText() {
  const text = inputText.value;
  if (!text.trim()) {
    alert("Please enter some text to analyze.");
    return;
  }

  processBtn.disabled = true;
  processBtn.textContent = "Analyzing…";

  try {
    const res = await fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    if (!res.ok) throw new Error(`Server error ${res.status}`);
    const data = await res.json();

    renderResults(text, data);
    showPage("resultsPage");

    // reset to first tab
    document.querySelector('.tab-btn[data-tab="main"]').click();
  } catch (err) {
    alert(
      "Could not reach the backend.\nMake sure the Flask server is running:\n\ncd backend && python app.py",
    );
    console.error(err);
  } finally {
    processBtn.disabled = false;
    processBtn.textContent = "Analyze Text";
  }
}

processBtn.addEventListener("click", analyzeText);
backBtn.addEventListener("click", () => {
  inputText.value = "";
  clearFileSelection();
  showPage("inputPage");
});

window.addEventListener("DOMContentLoaded", () => {
  inputText.value = "";
});
