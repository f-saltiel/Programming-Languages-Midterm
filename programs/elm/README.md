# Run Pace & Distance Converter

## 1. Program Overview
This program converts running distance and pace values and also calculates race pace from total race time and race distance.

## 2. Language / Tool Used
- Language: Elm
- Browser output: compiled JavaScript (`elm.js`)
- UI host: HTML + Bootstrap

## 3. Paradigm or Requirement Satisfied
This program satisfies the **Functional Programming** requirement.

## 4. Implementation Explanation
### Important files
- `src/Main.elm`: Elm source code for model, messages, update logic, view, and conversion functions.
- `elm.js`: Compiled Elm JavaScript used by the browser.
- `index.html`: Loads `elm.js` and initializes `Elm.Main.init` into `#elm-app`.

### Build note

The browser does not run Elm source code directly. The Elm source file must be compiled into JavaScript.

From the `programs/elm/` folder:

```bash
elm make src/Main.elm --output=elm.js
```

### Input flow
- User types values for miles, kilometers, pace per mile, pace per kilometer, race distance, race unit, and race time.
- Each input triggers an Elm `Msg` (`UpdateMiles`, `UpdatePaceMile`, etc.) through `onInput` handlers.
- `update : Msg -> Model -> Model` returns a **new model** with updated fields.

### Main processing
- Conversion functions (`milesToKilometers`, `kilometersToMiles`, `pacePerMileToPerKilometer`, `pacePerKilometerToPerMile`) compute direct conversions.
- `parseTimeString` accepts `MM:SS` or `HH:MM:SS` and validates time components.
- `calculatePaceFromDistance` computes per-mile pace and derives per-kilometer pace from total seconds and distance.
- Parsing helpers (`parsePositiveFloat`) and formatting helpers (`formatNumber`, `formatPace`) produce user-facing output.

### Output flow
- `view` derives display results from model values and parser/conversion results.
- `viewConversion` renders success values or validation error messages in the UI.
- The page is updated through Elm rendering (compiled to JS), not manual DOM mutation from custom JavaScript.

## 5. How It Demonstrates the Paradigm
This program demonstrates functional programming because:
- Conversion logic is pure input-to-output functions.
- Model data is immutable; update returns new state.
- Architecture follows `Model`, `Msg`, `update`, `view`.
- UI updates happen by rendering from model state, not direct shared-state mutation.

## 6. Input
- Miles value
- Kilometers value
- Pace per mile time
- Pace per kilometer time
- Race distance
- Race distance unit (miles/kilometers)
- Race total time (`MM:SS` or `HH:MM:SS`)

## 7. Output
- Converted distance values
- Converted pace values
- Calculated pace per mile and pace per kilometer from race distance/time
- Validation errors for invalid inputs/time formats

## 8. Manual Testing
- Enter `1` mile and confirm output is about `1.61 km`.
- Enter `5` kilometers and confirm output is about `3.11 mi`.
- Enter pace per mile `08:00` and confirm the pace per kilometer is about `04:58`.
- Enter pace per kilometer `05:00` and confirm the pace per mile is about `08:03`.
- Enter race distance `10` km and race time `00:50:00`, and confirm calculated pace is about `05:00/km` and `08:03/mi`.
- Enter invalid time (`12:65` or `abc`) and confirm a validation message appears.

## 9. Credits / References
- Elm documentation was referenced for Elm architecture, pure functions, input handling, and compiling Elm to JavaScript.
- Bootstrap documentation was referenced for layout, cards, buttons, forms, and responsive design.
- ChatGPT was used as a development assistant for planning, debugging, code review, and organization.