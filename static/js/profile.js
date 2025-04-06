let currentStep = 1;
const totalSteps = 4;

function showStep(step) {
  for (let i = 1; i <= totalSteps; i++) {
    const stepDiv = document.getElementById(`step${i}`);
    stepDiv.style.display = i === step ? 'block' : 'none';
  }

  // Update progress dots if needed
  const dots = document.querySelectorAll('.step');
  dots.forEach((dot, index) => {
    dot.classList.toggle('active', index < step);
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

// Show initial step
document.addEventListener("DOMContentLoaded", () => {
  showStep(currentStep);
});
