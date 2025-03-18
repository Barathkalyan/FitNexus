document.addEventListener("DOMContentLoaded", function () {
    // Slideshow Logic
    const slides = document.querySelectorAll(".slide");
    let currentSlide = 0;

    function showSlide() {
        slides.forEach((slide, index) => {
            slide.classList.remove("active");
            if (index === currentSlide) {
                slide.classList.add("active");
            }
        });
        currentSlide = (currentSlide + 1) % slides.length;
    }

    setInterval(showSlide, 3000); // Change every 3 seconds

    // Get Started Button Logic
    document.getElementById("get-started").addEventListener("click", function () {
        fetch("/check-profile")
            .then(response => response.json())
            .then(data => {
                if (data.complete) {
                    window.location.href = "/workout-log";
                } else {
                    window.location.href = "/profile-setup";
                }
            })
            .catch(error => console.error("Error:", error));
    });
});
