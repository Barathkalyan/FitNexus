document.addEventListener("DOMContentLoaded", function () {
    let slides = document.querySelectorAll(".slide");
    let index = 0;
    
    function showSlide() {
        slides.forEach(slide => slide.style.display = "none");
        slides[index].style.display = "block";
        index = (index + 1) % slides.length;
    }
    
    showSlide();
    setInterval(showSlide, 3000); // Changes image every 3 seconds
    

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
