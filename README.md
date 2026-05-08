# Programming Languages Midterm

## Project Overview
This project is a front-end personal website for a Programming Languages midterm. It includes **7 browser-based programs** that demonstrate multiple programming languages and programming paradigms/requirements in one site.

## Assignment Requirement Mapping

| Program | Language / Tool | Paradigm / Requirement | Folder | Short Purpose |
|---|---|---|---|---|
| Air Force PFRA Score Calculator | Python + PyScript | Imperative | `programs/python/` | Estimate PFRA score from fitness and body composition inputs |
| Run Pace & Distance Converter | Elm (compiled to JS) | Functional | `programs/elm/` | Convert distance/pace and compute race pace from time |
| Movie Recommendation System | Prolog + Tau Prolog | Logical | `programs/prolog/` | Query movie recommendations from preference facts/rules |
| Task Manager | TypeScript (compiled to JS) | Object-Oriented | `programs/typescript/` | Create, complete, and delete prioritized tasks |
| Course Grade Planner | JavaScript | Extra Program | `programs/js-1/` | Calculate needed average on remaining coursework |
| Rock Paper Scissors Game | JavaScript | Extra Program | `programs/js-2/` | Play against random computer choice and track score |
| CV / Resume Generator | JavaScript + html2pdf.js | Required CV Program | `programs/cv/` | Toggle CV entries, render resume preview, export PDF |

## Technologies Used
- HTML
- CSS
- Bootstrap
- JavaScript
- Python / PyScript
- Elm
- Prolog / Tau Prolog
- TypeScript
- html2pdf.js
- Git / GitHub

## How to Run Locally
Use a local server (not `file://`) so fetch requests and browser integrations work correctly.

```bash
python -m http.server 8000
```

Then open:

```text
http://localhost:8000/index.html
```

## Build / Compiled File Notes
- Elm source (`programs/elm/src/Main.elm`) is compiled to JavaScript (`programs/elm/elm.js`).
- TypeScript source (`programs/typescript/main.ts`) is compiled to JavaScript (`programs/typescript/main.js`).
- Browsers execute the compiled JavaScript files, not raw Elm or raw TypeScript.
- JavaScript programs (`js-1`, `js-2`, and `cv`) run directly in the browser.
- PyScript loads and runs the Python program in the browser, while Tau Prolog provides a JavaScript-based Prolog interpreter for running Prolog facts, rules, and queries in the browser.

### Elm Build Command

From `programs/elm/`:

```bash
elm make src/Main.elm --output=elm.js
```

### TypeScript Build Command

From `programs/typescript/`:

```bash
tsc main.ts --target ES2017
```

## CV Requirement Summary
- `cv.json` is located at the project root.
- The CV page (`programs/cv/`) loads this JSON file.
- Entries in each category can be activated/deactivated.
- Active entries are rendered as an HTML resume preview.
- The rendered resume can be downloaded as a PDF.

## Credits / References
- Official documentation was referenced for language syntax, browser integration, and implementation details.
- Bootstrap documentation was referenced for layout, cards, forms, buttons, and responsive design.
- ChatGPT was used as a development assistant for planning, debugging, code review, and organization.