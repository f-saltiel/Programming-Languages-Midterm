
# Course Grade Planner

## 1. Program Overview
This extra program calculates the average grade needed on remaining coursework to reach a desired final grade.

## 2. Language / Tool Used
- Language: JavaScript
- UI: HTML + Bootstrap

## 3. Paradigm or Requirement Satisfied
This program satisfies the **Extra Program** requirement.

## 4. Implementation Explanation
### Important files
- `index.html`: Form fields for current grade, completed weight, desired final grade, plus result area.
- `script.js`: Input reading, numeric validation, weighted-grade calculation, and result messaging.

### Input flow
- Form collects:
  - current grade (%)
  - completed course weight (%)
  - desired final grade (%)
- Submit handler reads inputs and parses them as numbers.

### Main processing
- Script validates numeric ranges and required constraints.
- Converts percentage weights to decimals.
- Computes remaining weight.
- Applies weighted formula:

`needed grade = (desired final grade - current grade × completed weight decimal) / remaining weight decimal`

- Decides which message to display:
  - reachable target,
  - difficult target,
  - impossible target,
  - already secured target.

### Output flow
- Result text is inserted into the result area with contextual styling/message content.
- Reset clears form and returns result area to initial state.

## 5. How It Demonstrates the Requirement
This program demonstrates practical browser-side problem solving with user input, validation, numeric computation, and conditional result messaging.

## 6. Input
- Current grade (%)
- Completed weight (%)
- Desired final grade (%)

## 7. Output
- Needed average on remaining coursework
- Explanatory status message (reachable/difficult/impossible/already secured)

## 8. Manual Testing
- Use `current=80`, `completed=50`, `desired=90`; verify needed grade is `100.00%`.
- Use `current=86`, `completed=70`, `desired=90`; verify needed grade is about `99.33%`.
- Use `current=70`, `completed=70`, `desired=80`; verify needed grade is about `103.33%` and the impossible message appears.
- Use `current=100`, `completed=80`, `desired=75`; verify the already-secured message appears.
- Use `completed=100` with a desired grade higher than the current grade and confirm the course-completed warning appears.
- Enter invalid values, such as negative numbers or values over 100, and verify the validation response.
- Click reset and confirm the result area returns to the default prompt.

## 9. Credits / References
- JavaScript documentation was referenced for DOM interaction, form handling, numeric conversion, and event listeners.
- Bootstrap documentation was referenced for layout, cards, buttons, forms, and responsive design.
- ChatGPT was used as a development assistant for planning, debugging, code review, and organization.