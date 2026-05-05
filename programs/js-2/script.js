const choiceButtons = document.querySelectorAll(".choice-btn");
const resetButton = document.getElementById("resetButton");

const resultArea = document.getElementById("resultArea");

const winsCount = document.getElementById("winsCount");
const lossesCount = document.getElementById("lossesCount");
const tiesCount = document.getElementById("tiesCount");
const roundsCount = document.getElementById("roundsCount");

let wins = 0;
let losses = 0;
let ties = 0;
let rounds = 0;

const choices = ["rock", "paper", "scissors"];

choiceButtons.forEach(function (button) {
  button.addEventListener("click", function () {
    const userChoice = button.dataset.choice;
    playRound(userChoice);
  });
});

resetButton.addEventListener("click", function () {
  wins = 0;
  losses = 0;
  ties = 0;
  rounds = 0;

  updateScoreboard();

  resultArea.className = "border rounded p-4 bg-light text-muted";
  resultArea.innerHTML = "Make a choice to start the game.";
});

function playRound(userChoice) {
  const computerChoice = getComputerChoice();
  const result = determineWinner(userChoice, computerChoice);

  rounds++;

  if (result === "win") {
    wins++;
  } else if (result === "loss") {
    losses++;
  } else {
    ties++;
  }

  updateScoreboard();
  showResult(userChoice, computerChoice, result);
}

function getComputerChoice() {
  const randomIndex = Math.floor(Math.random() * choices.length);
  return choices[randomIndex];
}

function determineWinner(userChoice, computerChoice) {
  if (userChoice === computerChoice) {
    return "tie";
  }

  if (
    (userChoice === "rock" && computerChoice === "scissors") ||
    (userChoice === "paper" && computerChoice === "rock") ||
    (userChoice === "scissors" && computerChoice === "paper")
  ) {
    return "win";
  }

  return "loss";
}

function updateScoreboard() {
  winsCount.textContent = wins;
  lossesCount.textContent = losses;
  tiesCount.textContent = ties;
  roundsCount.textContent = rounds;
}

function showResult(userChoice, computerChoice, result) {
  let resultClass = "";
  let resultMessage = "";

  if (result === "win") {
    resultClass = "alert alert-success";
    resultMessage = "You win this round.";
  } else if (result === "loss") {
    resultClass = "alert alert-danger";
    resultMessage = "You lose this round.";
  } else {
    resultClass = "alert alert-warning";
    resultMessage = "This round is a tie.";
  }

  resultArea.className = resultClass;
  resultArea.innerHTML = `
    <h3 class="h5">${resultMessage}</h3>

    <p>
      You chose:
      <strong>${capitalize(userChoice)}</strong>
    </p>

    <p>
      Computer chose:
      <strong>${capitalize(computerChoice)}</strong>
    </p>

    <p class="mb-0">
      Current record:
      <strong>${wins}</strong> wins,
      <strong>${losses}</strong> losses,
      <strong>${ties}</strong> ties.
    </p>
  `;
}

function capitalize(word) {
  return word.charAt(0).toUpperCase() + word.slice(1);
}