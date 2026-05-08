# Rock Paper Scissors

## 1. Program Overview
This extra program lets the user play rock-paper-scissors against a computer opponent and keeps a running scoreboard.

## 2. Language / Tool Used
- Language: JavaScript
- UI: HTML + Bootstrap

## 3. Paradigm or Requirement Satisfied
This program satisfies the **Extra Program** requirement.

## 4. Implementation Explanation
### Important files
- `index.html`: Choice buttons, reset button, result area, and scoreboard counters.
- `script.js`: Game logic, random computer move generation, winner evaluation, counter updates, and DOM rendering.

### Input flow
- User clicks one of three buttons (`rock`, `paper`, `scissors`).
- Click listeners read `data-choice` and trigger game round processing.

### Main processing
- Computer choice is generated randomly.
- Conditional logic compares user choice vs computer choice.
- Round result is classified as win, loss, or tie.
- Counters (`wins`, `losses`, `ties`, `rounds`) are updated.

### Output flow
- Scoreboard values are written to `winsCount`, `lossesCount`, `tiesCount`, `roundsCount`.
- Result area displays round outcome + both choices + current record.
- Reset button zeroes all counters and restores initial prompt.

## 5. How It Demonstrates the Requirement
This program demonstrates interactive event-driven JavaScript with randomization, decision logic, and live DOM updates.

## 6. Input
- Player move selection (rock/paper/scissors)
- Reset action

## 7. Output
- Round winner/loser/tie message
- Player and computer choices
- Updated wins/losses/ties/total rounds

## 8. Manual Testing
- Play at least 5 rounds and confirm round count increments each time.
- Confirm the selected player choice matches the clicked button.
- Confirm the computer choice displays as rock, paper, or scissors.
- Verify that the result follows the correct rules: rock beats scissors, scissors beats paper, and paper beats rock.
- Verify scoreboard updates after win/loss/tie outcomes.
- Click reset and verify all counters return to zero.
- Play again after reset and confirm state starts fresh.

## 9. Credits / References
- JavaScript documentation was referenced for DOM interaction, event listeners, arrays, random number generation, and conditional logic.
- Bootstrap documentation was referenced for layout, cards, buttons, forms, and responsive design.
- ChatGPT was used as a development assistant for planning, debugging, code review, and organization.