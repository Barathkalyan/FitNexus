let currentStep = 1;
const totalSteps = 4;

const stepTitles = [
  "Step 1: Basic Info",
  "Step 2: Body Stats",
  "Step 3: Fitness Goals",
  "Step 4: Preferences"
];

// Handle logout
document.getElementById("logoutBtn").addEventListener("click", () => {
  window.location.href = "/auth/logout";
});

// Show the current step and hide the rest
function showStep(step) {
  for (let i = 1; i <= totalSteps; i++) {
    const stepDiv = document.getElementById(`step${i}`);
    if (stepDiv) {
      stepDiv.style.display = (i === step) ? 'block' : 'none';
    }
  }

  // Update the step title
  const titleElement = document.getElementById("stepTitle");
  if (titleElement) {
    titleElement.innerText = stepTitles[step - 1];
  }

  updateProgressBar(step);
}

// Update the progress bar
function updateProgressBar(stepIndex) {
  const steps = document.querySelectorAll('.progress-bar .step');
  steps.forEach((step, index) => {
    step.classList.toggle('active', index < stepIndex);
  });
}

// Placeholder validation function (to be replaced with real validation logic)
function validateCurrentStep() {
  // Placeholder: return false to block, true to continue
  return true;
}

// Navigate to the next step
function nextStep() {
  if (currentStep < totalSteps && validateCurrentStep()) {
    currentStep++;
    showStep(currentStep);
  }
}

// Navigate to the previous step
function prevStep() {
  if (currentStep > 1) {
    currentStep--;
    showStep(currentStep);
  }
}

// Form submission logic
document.addEventListener("DOMContentLoaded", () => {
  showStep(currentStep); // Display the first step on page load

  const form = document.getElementById("profileForm");
  const errorElement = document.getElementById("formError");

  if (form) {
    form.addEventListener("submit", async function (e) {
      e.preventDefault(); // Prevent default form submission

      const submitBtn = form.querySelector("button[type='submit']");
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerText = "Submitting...";
      }

      if (errorElement) errorElement.innerText = "";

      // Collect data from the form
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
          // Redirect to dashboard if the profile is saved successfully
          window.location.href = "/dashboard";
        } else {
          // Show error message if there was an issue
          if (errorElement) errorElement.innerText = result.error || "Something went wrong!";
        }
      } catch (err) {
        console.error("Error:", err);
        if (errorElement) errorElement.innerText = "Server error!";
      }

      // Re-enable the submit button after the request is complete
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.innerText = "Submit";
      }
    });
  }
});
