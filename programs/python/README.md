# Air Force PFRA Score Calculator

## 1. Program Overview
This program estimates an Air Force PFRA score from user-entered fitness data (push-ups, sit-ups, 2-mile run) plus body composition data (waist and height).

## 2. Language / Tool Used
- Language: Python
- Browser tool: PyScript
- UI: HTML + Bootstrap

## 3. Paradigm or Requirement Satisfied
This program satisfies the **Imperative Programming** requirement.

## 4. Implementation Explanation
### Important files
- `index.html`: Contains the form inputs, calculate button, placeholder, and detailed result display sections.
- `main.py`: Connects UI events to Python logic, validates input, calls score calculation, and updates DOM output.
- `scoring_data.py`: Stores scoring tables and helper logic for repetition, run, WHtR, total score, category, and warnings.
- `pyscript.toml`: Configures PyScript files to load (`main.py`, `scoring_data.py`).

### Input flow
1. User fills the HTML form (`gender`, `age-group`, `pushups`, `situps`, `run-time`, `waist`, `height`).
2. Clicking `#calculate-button` triggers `handle_calculate` in `main.py` using `@when("click", "#calculate-button")`.
3. `form.reportValidity()` runs browser-level required/pattern checks before Python processing continues.

### Main processing flow
`main.py` then follows this sequence:
1. Read values from the DOM (`get_input_value`).
2. Convert/cast values into numeric types.
3. Validate constraints (non-negative reps, positive measurements, valid run time format with `validate_run_time`).
4. Call `calculate_pfra_score(...)` from `scoring_data.py`.

`scoring_data.py` handles scoring logic:
- `score_repetition_component(...)` matches push-up/sit-up reps to point tables.
- `score_run_component(...)` converts `MM:SS` to seconds and compares against run standards.
- `score_wht_component(...)` computes waist-to-height ratio and maps ratio to WHtR points/risk category.
- `calculate_pfra_score(...)` computes total score, category, and warnings, then returns a structured result dictionary.

### Output flow
- `display_results(...)` writes component points, total score, category, WHtR info, and warnings into result elements.
- `set_category_alert(...)` sets success/primary/danger alert style based on category/pass state.
- If any exception occurs, `display_error(...)` hides normal results and shows a single error alert.

## 5. How It Demonstrates the Paradigm
This is imperative because logic runs as a clear step-by-step sequence:
1. Read input
2. Validate input
3. Look up scores
4. Calculate totals
5. Display results

The implementation is state-driven and procedural, not rule-driven (logical) and not model-transform functional architecture.

## 6. Input
- Gender
- Age group
- 1-minute push-up count
- 1-minute sit-up count
- 2-mile run time (`MM:SS`)
- Waist measurement
- Height measurement

## 7. Output
- Push-up points
- Sit-up points
- Run points
- WHtR points
- Total PFRA score
- Score category (Excellent / Satisfactory / Unsatisfactory)
- WHtR ratio and risk category
- Component warnings and error messages (when applicable)

## 8. Manual Testing
- Enter a fully valid case (e.g., normal reps/time/measurements) and confirm all component scores and total are shown.
- Enter run time with invalid format (`15-00`, `15:75`, `abc`) and confirm validation error appears.
- Enter negative reps and confirm Python-side validation error is displayed.
- Enter waist or height as `0` and confirm the program blocks calculation with an error.
- Use values likely to trigger a zero component score and confirm warning list appears.
- Enter a valid case such as `male`, `25-29`, `55 push-ups`, `60 sit-ups`, `15:00 run`, `31 waist`, `63 height`, and confirm all component scores and total are shown.

## 9. Credits / References
- Python documentation was referenced for syntax, functions, data structures, exception handling, and validation logic.
- PyScript documentation was referenced for running Python in the browser and connecting Python code to HTML elements.
- The USAF PFRA scoring chart was referenced for component scoring values and score categories.
- Bootstrap documentation was referenced for layout, cards, buttons, forms, and responsive design.
- ChatGPT was used as a development assistant for planning, debugging, code review, and organization.