let currentStep = 1;
const totalSteps = 4;

const stepTitles = [
  "Step 1: Basic Info",
  "Step 2: Body Stats",
  "Step 3: Fitness Goals",
  "Step 4: Preferences"
];

document.getElementById("logoutBtn").addEventListener("click", () => {
  window.location.href = "/auth/logout";
});

function showStep(step) {
  for (let i = 1; i <= totalSteps; i++) {
    const stepDiv = document.getElementById(`step${i}`);
    if (stepDiv) {
      stepDiv.style.display = (i === step) ? 'block' : 'none';
    }
  }

  const titleElement = document.getElementById("stepTitle");
  if (titleElement) {
    titleElement.innerText = stepTitles[step - 1];
  }

  updateProgressBar(step);
}

function updateProgressBar(stepIndex) {
  const steps = document.querySelectorAll('.progress-bar .step');
  steps.forEach((step, index) => {
    step.classList.toggle('active', index < stepIndex);
  });
}

function validateCurrentStep() {
  // Placeholder: return false to block, true to continue
  return true;
}

function nextStep() {
  if (currentStep < totalSteps && validateCurrentStep()) {
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

  const form = document.getElementById("profileForm");
  const errorElement = document.getElementById("formError");

  if (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault();

      const submitBtn = form.querySelector("button[type='submit']");
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = "Submitting...";
      }
      if (errorElement) errorElement.innerText = "";

      const data = {
        age: form.age.value,
        gender: form.gender.value,
        height: form.height.value,
        weight: form.weight.value,
        fitness_goal: form.goal.value,
        target_weight: form.target.value,
        diet_preference: form.diet.value,
        workout_time: form.workout_time.value,
        workout_days: form.workout_days.value
      };

      try {
        const res = await fetch("/api/complete-profile", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify(data)
        });

        const result = await res.json();
        if (res.ok) {
          window.location.href = "/dashboard";
        } else {
          if (errorElement) errorElement.innerText = result.error || "Something went wrong!";
        }
      } catch (err) {
        console.error("Error:", err);
        if (errorElement) errorElement.innerText = "Server error!";
      }

      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerText = "Submit";
      }
    });
  }
});
