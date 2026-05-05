const gradePlannerForm = document.getElementById("gradePlannerForm");
const resultArea = document.getElementById("resultArea");
const resetButton = document.getElementById("resetButton");

gradePlannerForm.addEventListener("submit", function (event) {
  event.preventDefault();

  const currentGrade = Number(document.getElementById("currentGrade").value);
  const completedWeight = Number(document.getElementById("completedWeight").value);
  const desiredGrade = Number(document.getElementById("desiredGrade").value);

  if (!isValidInput(currentGrade, completedWeight, desiredGrade)) {
    showError("Please enter valid numbers between 0 and 100.");
    return;
  }

  const remainingWeight = 100 - completedWeight;

  if (remainingWeight === 0) {
    handleCompletedCourse(currentGrade, desiredGrade);
    return;
  }

  const completedDecimal = completedWeight / 100;
  const remainingDecimal = remainingWeight / 100;

  const currentWeightedPoints = currentGrade * completedDecimal;
  const neededGrade = (desiredGrade - currentWeightedPoints) / remainingDecimal;

  showResult({
    currentGrade,
    completedWeight,
    remainingWeight,
    desiredGrade,
    currentWeightedPoints,
    neededGrade
  });
});

resetButton.addEventListener("click", function () {
  resultArea.className = "border rounded p-4 bg-light text-muted";
  resultArea.innerHTML = "Enter your information above and click Calculate Needed Grade.";
});

function isValidInput(currentGrade, completedWeight, desiredGrade) {
  return (
    Number.isFinite(currentGrade) &&
    Number.isFinite(completedWeight) &&
    Number.isFinite(desiredGrade) &&
    currentGrade >= 0 &&
    currentGrade <= 100 &&
    completedWeight >= 0 &&
    completedWeight <= 100 &&
    desiredGrade >= 0 &&
    desiredGrade <= 100
  );
}

function handleCompletedCourse(currentGrade, desiredGrade) {
  if (currentGrade >= desiredGrade) {
    resultArea.className = "alert alert-success";
    resultArea.innerHTML = `
      <h3 class="h5">Course Already Completed</h3>
      <p class="mb-0">
        Your current grade is <strong>${currentGrade.toFixed(2)}%</strong>, which already meets
        or exceeds your desired final grade of <strong>${desiredGrade.toFixed(2)}%</strong>.
      </p>
    `;
  } else {
    resultArea.className = "alert alert-danger";
    resultArea.innerHTML = `
      <h3 class="h5">Course Already Completed</h3>
      <p class="mb-0">
        Your current grade is <strong>${currentGrade.toFixed(2)}%</strong>, which is below your
        desired final grade of <strong>${desiredGrade.toFixed(2)}%</strong>. Since there is no
        remaining coursework, the desired grade cannot be reached.
      </p>
    `;
  }
}

function showResult(data) {
  const neededGrade = data.neededGrade;
  let resultClass = "alert alert-info";
  let message = "";

  if (neededGrade > 100) {
    resultClass = "alert alert-danger";
    message = "This desired grade is not realistically possible unless extra credit is available.";
  } else if (neededGrade <= 0) {
    resultClass = "alert alert-success";
    message = "You have already secured the desired final grade based on the completed coursework.";
  } else if (neededGrade <= 70) {
    resultClass = "alert alert-success";
    message = "This target is very reachable if you keep performing consistently.";
  } else if (neededGrade <= 85) {
    resultClass = "alert alert-primary";
    message = "This target is realistic, but you still need solid performance on the remaining work.";
  } else if (neededGrade <= 100) {
    resultClass = "alert alert-warning";
    message = "This target is possible, but it requires strong performance on the remaining work.";
  }

  resultArea.className = resultClass;
  resultArea.innerHTML = `
    <h3 class="h5">Grade Calculation Result</h3>

    <p>
      Current grade:
      <strong>${data.currentGrade.toFixed(2)}%</strong>
    </p>

    <p>
      Completed course weight:
      <strong>${data.completedWeight.toFixed(2)}%</strong>
    </p>

    <p>
      Remaining course weight:
      <strong>${data.remainingWeight.toFixed(2)}%</strong>
    </p>

    <p>
      Desired final grade:
      <strong>${data.desiredGrade.toFixed(2)}%</strong>
    </p>

    <hr>

    <p>
      Current weighted points earned:
      <strong>${data.currentWeightedPoints.toFixed(2)}</strong>
    </p>

    <p class="fs-5">
      Needed average on remaining coursework:
      <strong>${neededGrade.toFixed(2)}%</strong>
    </p>

    <p class="mb-0">
      ${message}
    </p>
  `;
}

function showError(message) {
  resultArea.className = "alert alert-danger";
  resultArea.innerHTML = `
    <h3 class="h5">Input Error</h3>
    <p class="mb-0">${message}</p>
  `;
}