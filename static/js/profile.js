let currentStep = 1;
const totalSteps = 4;

const stepTitles = [
  "Step 1: Basic Info",
  "Step 2: Body Stats",
  "Step 3: Fitness Goals",
  "Step 4: Preferences"
];

function showStep(step) {
  for (let i = 1; i <= totalSteps; i++) {
    document.getElementById(`step${i}`).style.display = (i === step) ? 'block' : 'none';
  }

  document.getElementById("stepTitle").innerText = stepTitles[step - 1];
  updateProgressBar(step);
}

function updateProgressBar(stepIndex) {
  const steps = document.querySelectorAll('.progress-bar .step');
  steps.forEach((step, index) => {
    step.classList.toggle('active', index < stepIndex);
  });
}

function nextStep() {
  if (currentStep < totalSteps) {
    currentStep++;
    showStep(currentStep);
  }
}

function prevStep() {
  if (currentStep > 1) {
    currentStep--;
    showStep(currentStep);
  }
}

document.addEventListener("DOMContentLoaded", () => {
  showStep(currentStep);
});
document.getElementById("profileForm").addEventListener("submit", function (e) {
  e.preventDefault();

  const data = {
    age: document.getElementById("age").value,
    gender: document.getElementById("gender").value,
    height: document.querySelector("input[name='height']").value,
    weight: document.querySelector("input[name='weight']").value,
    fitness_goal: document.getElementById("goal").value,
    target_weight: document.getElementById("target").value,
    diet_preference: document.getElementById("diet").value,
    workout_time: document.querySelector("input[name='workout_time']").value,
    workout_days: document.querySelector("input[name='workout_days']").value,
  };

  fetch("/auth/complete_profile", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(res => {
    if (res.redirect) {
      window.location.href = res.redirect;
    } else {
      alert(res.message || res.error || "Something went wrong!");
    }
  })
  .catch(err => console.error("Error:", err));
});

