"use strict";
class Task {
    constructor(id, title, priority) {
        this.id = id;
        this.title = title;
        this.priority = priority;
        this.completed = false;
    }
    toggleComplete() {
        this.completed = !this.completed;
    }
    getStatusLabel() {
        return this.completed ? "Completed" : "In Progress";
    }
    getPriorityLabel() {
        return this.priority.charAt(0).toUpperCase() + this.priority.slice(1);
    }
}
class TaskManager {
    constructor() {
        this.tasks = [];
    }
    addTask(title, priority) {
        const id = Date.now() + Math.floor(Math.random() * 1000);
        const task = new Task(id, title, priority);
        this.tasks.push(task);
        return task;
    }
    deleteTask(id) {
        this.tasks = this.tasks.filter((task) => task.id !== id);
    }
    toggleTask(id) {
        const task = this.tasks.find((item) => item.id === id);
        if (task) {
            task.toggleComplete();
        }
    }
    getTasks() {
        return [...this.tasks];
    }
}
const taskManager = new TaskManager();
const taskForm = document.getElementById("task-form");
const taskTitleInput = document.getElementById("task-title");
const taskPriorityInput = document.getElementById("task-priority");
const taskList = document.getElementById("task-list");
const emptyState = document.getElementById("empty-state");
const taskFeedback = document.getElementById("task-feedback");
function getPriorityBadgeClass(priority) {
    if (priority === "high")
        return "text-bg-danger";
    if (priority === "medium")
        return "text-bg-warning";
    return "text-bg-success";
}
function getStatusBadgeClass(task) {
    return task.completed ? "text-bg-success" : "text-bg-secondary";
}
function renderTasks() {
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
function showFeedback(message) {
    taskFeedback.textContent = message;
    taskFeedback.classList.remove("d-none");
}
function clearFeedback() {
    taskFeedback.textContent = "";
    taskFeedback.classList.add("d-none");
}
taskForm.addEventListener("submit", (event) => {
    event.preventDefault();
    const title = taskTitleInput.value.trim();
    const priority = taskPriorityInput.value;
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
