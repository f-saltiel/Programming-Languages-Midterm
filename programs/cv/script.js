let cvData = null;

const statusMessageEl = document.getElementById('status-message');
const controlsContainerEl = document.getElementById('controls-container');
const resumePreviewEl = document.getElementById('resume-preview');
const downloadPdfBtn = document.getElementById('download-pdf-btn');

function showStatusMessage(message, type = 'info') {
  statusMessageEl.className = `alert alert-${type} mb-3`;
  statusMessageEl.textContent = message;
}

async function loadCvData() {
  try {
    showStatusMessage('Loading CV data...', 'info');

    const response = await fetch('../../cv.json');
    if (!response.ok) {
      throw new Error(`Failed to load cv.json (HTTP ${response.status}). Run this page with a local server instead of file://.`);
    }

    cvData = await response.json();

    if (!cvData || !Array.isArray(cvData.categories)) {
      throw new Error('Invalid CV format. Expected categories array in cv.json.');
    }

    renderControls();
    renderResume();
    showStatusMessage('CV loaded successfully. Toggle entries to customize the resume.', 'success');
  } catch (error) {
    console.error('Error loading CV data:', error);
    showStatusMessage(error.message || 'Unable to load CV data.', 'danger');
    controlsContainerEl.innerHTML = '';
    resumePreviewEl.innerHTML = '<p class="text-danger mb-0">Resume preview unavailable because cv.json could not be loaded.</p>';
  }
}

function renderControls() {
  if (!cvData || !Array.isArray(cvData.categories)) {
    return;
  }

  controlsContainerEl.innerHTML = cvData.categories.map((category) => {
    const entriesHtml = category.entries.map((entry) => {
      const checkboxId = `toggle-${entry.id}`;
      return `
        <div class="form-check mb-2">
          <input
            class="form-check-input"
            type="checkbox"
            id="${checkboxId}"
            data-category-id="${category.id}"
            data-entry-id="${entry.id}"
            ${entry.active ? 'checked' : ''}
          />
          <label class="form-check-label" for="${checkboxId}">
            ${entry.title}
          </label>
        </div>
      `;
    }).join('');

    return `
      <div class="col-12 col-md-6">
        <div class="border rounded p-3 h-100 bg-light">
          <h3 class="h6 mb-3">${category.title}</h3>
          ${entriesHtml}
        </div>
      </div>
    `;
  }).join('');

  controlsContainerEl.querySelectorAll('input[type="checkbox"]').forEach((checkbox) => {
    checkbox.addEventListener('change', handleEntryToggle);
  });
}

function createEntryHtml(entry) {
  const metaParts = [entry.organization, entry.location, entry.date].filter(Boolean);
  const metaLine = metaParts.length
    ? `<div class="text-muted small mb-1">${metaParts.join(" | ")}</div>`
    : "";

  const description = entry.description
    ? `<p class="mb-1">${entry.description}</p>`
    : "";

  const bullets = Array.isArray(entry.bullets) && entry.bullets.length
    ? `<ul class="mb-2">${entry.bullets.map((bullet) => `<li>${bullet}</li>`).join("")}</ul>`
    : "";

  return `
    <div class="resume-entry mb-3">
      <h4 class="h6 mb-1">${entry.title}</h4>
      ${metaLine}
      ${description}
      ${bullets}
    </div>
  `;
}

function renderResume() {
  if (!cvData) {
    return;
  }

  const personal = cvData.personal || {};
  const categoriesHtml = cvData.categories.map((category) => {
    const activeEntries = category.entries.filter((entry) => entry.active);
    if (!activeEntries.length) {
      return '';
    }

    return `
      <section class="resume-section mb-4">
        <h3 class="resume-heading h5 border-bottom pb-1">${category.title}</h3>
        ${activeEntries.map((entry) => createEntryHtml(entry)).join("")}
      </section>
    `;
  }).join('');

  resumePreviewEl.innerHTML = `
    <article id="resume-content">
      <header class="mb-4">
        <h2 class="h3 mb-1">${personal.name || 'Name not provided'}</h2>
        <p class="mb-1 fw-semibold">${personal.title || ''}</p>
        <p class="mb-1">${personal.email || ''} ${personal.phone ? ' | ' + personal.phone : ''}</p>
        <p class="mb-1">${personal.location || ''}</p>
        <p class="mb-0">${personal.summary || ''}</p>
      </header>
      ${categoriesHtml || '<p class="text-muted">No active entries selected.</p>'}
    </article>
  `;
}

function handleEntryToggle(event) {
  const categoryId = event.target.dataset.categoryId;
  const entryId = event.target.dataset.entryId;
  const isActive = event.target.checked;

  const category = cvData.categories.find((item) => item.id === categoryId);
  if (!category) {
    return;
  }

  const entry = category.entries.find((item) => item.id === entryId);
  if (!entry) {
    return;
  }

  entry.active = isActive;
  renderResume();
}

function downloadPdf() {
  if (!window.html2pdf) {
    console.error("html2pdf library is not available.");
    showStatusMessage("PDF download failed because the html2pdf library did not load.", "danger");
    return;
  }

  const resumeContent = document.getElementById("resume-content");

  if (!resumeContent) {
    showStatusMessage("No resume content available for PDF export.", "warning");
    return;
  }

  const pdfWrapper = document.createElement("div");
  const pdfClone = resumeContent.cloneNode(true);

  pdfWrapper.style.position = "fixed";
  pdfWrapper.style.left = "-10000px";
  pdfWrapper.style.top = "0";
  pdfWrapper.style.width = "7.5in";
  pdfWrapper.style.backgroundColor = "#ffffff";
  pdfWrapper.style.color = "#212529";
  pdfWrapper.style.padding = "0";
  pdfWrapper.style.margin = "0";

  pdfClone.id = "resume-pdf-content";
  pdfClone.style.width = "7.5in";
  pdfClone.style.backgroundColor = "#ffffff";
  pdfClone.style.color = "#212529";
  pdfClone.style.padding = "0";
  pdfClone.style.margin = "0";
  pdfClone.style.fontSize = "11px";
  pdfClone.style.lineHeight = "1.35";

  pdfClone.querySelectorAll(".resume-section").forEach((section) => {
    section.style.breakInside = "auto";
    section.style.pageBreakInside = "auto";
  });

  pdfClone.querySelectorAll(".resume-entry").forEach((entry) => {
    entry.style.breakInside = "avoid";
    entry.style.pageBreakInside = "avoid";
  });

  pdfClone.querySelectorAll(".resume-heading").forEach((heading) => {
    heading.style.breakAfter = "avoid";
    heading.style.pageBreakAfter = "avoid";
  });

  pdfWrapper.appendChild(pdfClone);
  document.body.appendChild(pdfWrapper);

  const options = {
    margin: [0.5, 0.5, 0.5, 0.5],
    filename: "francisco-saltiel-resume.pdf",
    image: { type: "jpeg", quality: 0.98 },
    html2canvas: {
      scale: 2,
      useCORS: true,
      scrollX: 0,
      scrollY: 0
    },
    jsPDF: {
      unit: "in",
      format: "letter",
      orientation: "portrait"
    },
    pagebreak: {
      mode: ["css", "legacy"],
      avoid: [".resume-entry", ".resume-heading"]
    }
  };

  window.html2pdf()
    .set(options)
    .from(pdfClone)
    .save()
    .then(() => {
      showStatusMessage("PDF download started successfully.", "success");
    })
    .catch((error) => {
      console.error("Error generating PDF:", error);
      showStatusMessage("An error occurred while generating the PDF.", "danger");
    })
    .finally(() => {
      document.body.removeChild(pdfWrapper);
    });
}

downloadPdfBtn.addEventListener('click', downloadPdf);

loadCvData();