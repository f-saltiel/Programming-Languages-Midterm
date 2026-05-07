type Priority = "low" | "medium" | "high";

class Task {
  id: number;
  title: string;
  priority: Priority;
  completed: boolean;

  constructor(id: number, title: string, priority: Priority) {
    this.id = id;
    this.title = title;
    this.priority = priority;
    this.completed = false;
  }

  toggleComplete(): void {
    this.completed = !this.completed;
  }

  getStatusLabel(): string {
    return this.completed ? "Completed" : "In Progress";
  }

  getPriorityLabel(): string {
    return this.priority.charAt(0).toUpperCase() + this.priority.slice(1);
  }
}

class TaskManager {
  private tasks: Task[] = [];

  addTask(title: string, priority: Priority): Task {
    const id = Date.now() + Math.floor(Math.random() * 1000);
    const task = new Task(id, title, priority);
    this.tasks.push(task);
    return task;
  }

  deleteTask(id: number): void {
    this.tasks = this.tasks.filter((task) => task.id !== id);
  }

  toggleTask(id: number): void {
    const task = this.tasks.find((item) => item.id === id);
    if (task) {
      task.toggleComplete();
    }
  }

  getTasks(): Task[] {
    return [...this.tasks];
  }
}

const taskManager = new TaskManager();

const taskForm = document.getElementById("task-form") as HTMLFormElement;
const taskTitleInput = document.getElementById("task-title") as HTMLInputElement;
const taskPriorityInput = document.getElementById("task-priority") as HTMLSelectElement;
const taskList = document.getElementById("task-list") as HTMLDivElement;
const emptyState = document.getElementById("empty-state") as HTMLDivElement;
const taskFeedback = document.getElementById("task-feedback") as HTMLDivElement;

function getPriorityBadgeClass(priority: Priority): string {
  if (priority === "high") return "text-bg-danger";
  if (priority === "medium") return "text-bg-warning";
  return "text-bg-success";
}

function getStatusBadgeClass(task: Task): string {
  return task.completed ? "text-bg-success" : "text-bg-secondary";
}

function renderTasks(): void {
  const tasks = taskManager.getTasks();
  taskList.innerHTML = "";

  if (tasks.length === 0) {
    emptyState.classList.remove("d-none");
    return;
  }

  emptyState.classList.add("d-none");

  tasks.forEach((task) => {
    const card = document.createElement("div");
    card.className = "card shadow-sm";

    const cardBody = document.createElement("div");
    cardBody.className = "card-body d-flex flex-column flex-md-row justify-content-between align-items-md-center gap-3";

    const info = document.createElement("div");

    const title = document.createElement("h3");
    title.className = "h5 mb-2";
    title.textContent = task.title;
    if (task.completed) {
      title.classList.add("text-decoration-line-through", "text-muted");
    }

    const badges = document.createElement("div");
    badges.className = "d-flex flex-wrap gap-2";

    const priorityBadge = document.createElement("span");
    priorityBadge.className = `badge ${getPriorityBadgeClass(task.priority)}`;
    priorityBadge.textContent = `Priority: ${task.getPriorityLabel()}`;

    const statusBadge = document.createElement("span");
    statusBadge.className = `badge ${getStatusBadgeClass(task)}`;
    statusBadge.textContent = `Status: ${task.getStatusLabel()}`;

    badges.append(priorityBadge, statusBadge);
    info.append(title, badges);

    const actions = document.createElement("div");
    actions.className = "d-flex gap-2";

    const toggleButton = document.createElement("button");
    toggleButton.className = task.completed ? "btn btn-outline-secondary btn-sm" : "btn btn-success btn-sm";
    toggleButton.textContent = task.completed ? "Undo" : "Complete";
    toggleButton.addEventListener("click", () => {
      taskManager.toggleTask(task.id);
      renderTasks();
    });

    const deleteButton = document.createElement("button");
    deleteButton.className = "btn btn-danger btn-sm";
    deleteButton.textContent = "Delete";
    deleteButton.addEventListener("click", () => {
      taskManager.deleteTask(task.id);
      renderTasks();
    });

    actions.append(toggleButton, deleteButton);
    cardBody.append(info, actions);
    card.append(cardBody);
    taskList.append(card);
  });
}

function showFeedback(message: string): void {
  taskFeedback.textContent = message;
  taskFeedback.classList.remove("d-none");
}

function clearFeedback(): void {
  taskFeedback.textContent = "";
  taskFeedback.classList.add("d-none");
}

taskForm.addEventListener("submit", (event) => {
  event.preventDefault();
  const title = taskTitleInput.value.trim();
  const priority = taskPriorityInput.value as Priority;

  if (!title) {
    showFeedback("Task title is required.");
    return;
  }

  clearFeedback();
  taskManager.addTask(title, priority);
  taskForm.reset();
  taskPriorityInput.value = "medium";
  renderTasks();
});

renderTasks();