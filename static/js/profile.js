let currentStep = 1;
const totalSteps = 4;

function showStep(step) {
  for (let i = 1; i <= totalSteps; i++) {
    const stepDiv = document.getElementById(`step${i}`);
    stepDiv.style.display = i === step ? 'block' : 'none';
  }

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
