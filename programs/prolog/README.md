# Movie Recommendation System

## 1. Program Overview
This program recommends movies based on selected genre, mood, and pace. It tries exact matches first, then relaxed matches when needed.

## 2. Language / Tool Used
- Language: Prolog
- Browser tool: Tau Prolog
- UI + glue logic: HTML with embedded JavaScript

## 3. Paradigm or Requirement Satisfied
This program satisfies the **Logical Programming** requirement.

## 4. Implementation Explanation
### Important files
- `index.html`: Contains the full implementation (form UI, Prolog knowledge base, rule predicates, Tau Prolog session logic, result rendering).

### Knowledge base and rules
- The movie database is declared as Prolog facts (`movie(...)`) with genre, mood, pace, and display title.
- Predicates define query behavior for:
  - exact matching by all selected attributes,
  - relaxed matching rules for close alternatives when exact matches are not available.

### Input flow
- User selects `genre`, `mood`, and `pace` in the form.
- JavaScript reads selected values on submit.
- JavaScript builds and submits a Prolog query into a Tau Prolog session running in browser.

### Main processing
- Tau Prolog evaluates the query against the facts/rules.
- Prolog performs the logical search/unification to find valid movie titles.
- JavaScript reads returned answers and formats display lists.

### Output flow
- Recommendations are rendered into the `#results` container.
- The UI indicates whether output came from exact matches or relaxed alternatives.
- Clear button resets recommendation output state.

## 5. How It Demonstrates the Paradigm
This implementation is logical because:
- The program is written around **facts + rules**.
- User preferences become a **query**.
- Prolog infers answers by satisfying predicates.
- Main recommendation logic is not written as manual imperative loops over every movie.

## 6. Input
- Genre selection
- Mood selection
- Pace selection

## 7. Output
- Exact recommendation list (when matches exist)
- Relaxed/close recommendation list (fallback behavior)
- Empty/no-match messaging when applicable

## 8. Manual Testing
- Select `action / intense / fast` and confirm exact matches appear, such as *Mad Max: Fury Road*, *John Wick*, or *The Matrix*.
- Select `sci_fi / thoughtful / slow` and confirm exact matches appear, such as *Arrival*, *Interstellar*, or *Blade Runner 2049*.
- Select a restrictive combination, such as `romance / intense / fast`, and confirm the no-match or relaxed behavior works correctly.
- Change one preference at a time and verify recommendations change logically.
- Click **Clear** and confirm the results area resets.

## 9. Credits / References
- Tau Prolog documentation was referenced for creating browser-based Prolog sessions, consulting facts/rules, running queries, and reading answers.
- Prolog documentation was referenced for facts, predicates, rules, and query structure.
- Bootstrap documentation was referenced for layout, cards, buttons, forms, and responsive design.
- ChatGPT was used as a development assistant for planning, debugging, code review, and organization.