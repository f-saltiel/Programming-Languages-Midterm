# Task Manager

## 1. Program Overview
This program lets the user add tasks with priority, toggle completion status, and delete tasks while keeping a live task list in the page.

## 2. Language / Tool Used
- Language: TypeScript (source)
- Browser runtime: compiled JavaScript
- UI: HTML + Bootstrap

## 3. Paradigm or Requirement Satisfied
This program satisfies the **Object-Oriented Programming** requirement.

## 4. Implementation Explanation
### Important files
- `main.ts`: TypeScript source with class definitions and app logic.
- `main.js`: Compiled JavaScript loaded by browser.
- `index.html`: Loads `main.js` (not `main.ts`) and provides form/list containers.

### Build note

The browser does not run TypeScript directly. The TypeScript source must be compiled into JavaScript.

From the `programs/typescript/` folder:

```bash
tsc main.ts --target ES2017
```
This generates main.js, which is the file loaded by index.html.

### Core classes
- `Task` class
  - Properties: `id`, `title`, `priority`, `completed`
  - Methods: `toggleComplete()`, `getStatusLabel()`, `getPriorityLabel()`
- `TaskManager` class
  - Stores a private `tasks` array
  - Methods to add/delete/toggle tasks and drive rendering/state checks

### Input flow
- User enters task title and selects priority in `#task-form`.
- Form submit event listener validates input then calls `TaskManager.addTask(...)`.
- Buttons in rendered task cards call toggle/delete methods through event listeners.

### Main processing
- Each new task gets an id, title, priority, and default incomplete status, then is stored as a `Task` object.
- Toggle updates `completed` state via class method.
- Delete removes by id from the task collection.

### Output flow
- Task list is rendered into DOM (`#task-list`) with status and priority labels.
- Empty-state and feedback alerts are shown/hidden depending on current task state and validation outcomes.

## 5. How It Demonstrates the Paradigm
This is object-oriented because:
- Tasks are modeled as objects (`Task`).
- Task behavior is encapsulated in Task methods.
- Collection/business behavior is grouped in `TaskManager`.
- State and behavior are managed through class properties and methods.

## 6. Input
- Task title (text)
- Priority level (`low`, `medium`, `high`)
- User actions: toggle complete, delete

## 7. Output
- Rendered task cards/list
- Status display (`Completed` / `In Progress`)
- Priority display labels
- Empty-state and feedback messages

## 8. Manual Testing
- Add tasks with each priority and verify they appear.
- Toggle a task and confirm status label changes.
- Delete a task and confirm it is removed.
- Delete all tasks and confirm empty-state message appears again.
- Submit blank/whitespace title and confirm validation feedback.
- Refresh the page and confirm tasks do not persist, since this version stores tasks in memory only.

## 9. Credits / References
- TypeScript documentation was referenced for class syntax, type annotations, access modifiers, and compiling TypeScript into JavaScript.
- Bootstrap documentation was referenced for layout, cards, buttons, forms, and responsive design.
- ChatGPT was used as a development assistant for planning, debugging, code review, and organization.