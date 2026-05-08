# CV / Resume Generator

## 1. Program Overview
This required CV program loads a full CV dataset from JSON, lets the user activate/deactivate entries, renders a tailored resume preview, and exports that preview to PDF.

## 2. Language / Tool Used
- Language: JavaScript
- Data file: JSON (`cv.json` at project root)
- Browser library: html2pdf.js
- UI: HTML + Bootstrap

## 3. Paradigm or Requirement Satisfied
This program satisfies the **Required CV Program** requirement.

## 4. Implementation Explanation
### Important files
- `../../cv.json` (project root): CV data source (personal info + categories + entries).
- `index.html`: Status area, toggle controls container, resume preview container, PDF button.
- `script.js`: Data loading, checkbox control rendering, active-entry filtering, preview rendering, and PDF export.

### Data structure and flow
- `cv.json` stores broad CV information.
- Categories contain entries.
- Each entry includes `active: true/false`.

### Input flow
- On page load, `loadCvData()` runs.
- `script.js` fetches `../../cv.json`.
- `renderControls()` creates checkbox controls for each entry.
- User toggles checkboxes to activate/deactivate entries.

### Main processing
- `handleEntryToggle` updates `entry.active` in in-memory CV data.
- `renderResume()` filters each category to active entries only.
- `createEntryHtml()` formats each active entry (title, metadata, description, bullets).
- `renderResume()` is the main function that prints the resume into HTML by building the preview from the currently active entries.

### Output flow
- Resume HTML is rendered in `#resume-preview`.
- If no entries are active in a category, that section is omitted.
- PDF button calls `downloadPdf()`:
  - clones resume content,
  - applies print-friendly sizing/page-break options,
  - uses html2pdf.js to generate and download the PDF file.

### CV vs Resume distinction
- `cv.json` is the **broader CV data source**.
- The resume preview is a **selected/tailored subset** made from currently active entries.

## 5. How It Demonstrates the Requirement
This program satisfies the CV requirement by storing CV data in `cv.json`, allowing entries to be activated or deactivated, rendering the selected entries as an HTML resume, and exporting that resume as a downloadable PDF.

## 6. Input
- Entry toggle choices (checkboxes)
- PDF download action

## 7. Output
- Dynamic resume preview HTML
- Status messages for load/export
- Downloaded resume PDF

## 8. Manual Testing
- Load page on local server and confirm `cv.json` loads successfully.
- Toggle multiple entries off/on and confirm resume preview updates immediately.
- Deactivate all entries in one category and confirm that section disappears.
- Click Download PDF and confirm file generation/download starts.
- Open page with `file://` (optional negative test) and confirm load error message explains local server requirement.

## 9. Credits / References
- JavaScript documentation was referenced for fetch, DOM manipulation, event handling, and JSON processing.
- html2pdf.js documentation was referenced for generating a PDF from HTML content.
- Bootstrap documentation was referenced for layout, cards, buttons, forms, and responsive design.
- ChatGPT was used as a development assistant for planning, debugging, code review, and organization.