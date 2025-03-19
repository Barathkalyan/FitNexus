document.addEventListener("DOMContentLoaded", function () {
    let slides = document.querySelectorAll(".slide");
    let index = 0;
    
    function showSlide() {
        slides.forEach(slide => slide.classList.remove("active"));
        slides[index].classList.add("active");
        index = (index + 1) % slides.length;
    }
    
    showSlide(); // Show first image
    setInterval(showSlide, 3000);
    
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
