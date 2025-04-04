document.addEventListener("DOMContentLoaded", function () {
    // Slideshow logic
    let slides = document.querySelectorAll(".slide");
    let slideIndex = 0;

    function showSlide() {
        slides.forEach(slide => slide.classList.remove("active"));
        slides[slideIndex].classList.add("active");
        slideIndex = (slideIndex + 1) % slides.length;
    }

    showSlide();
    setInterval(showSlide, 3000);

    // Quote logic
    let quotes = document.querySelectorAll(".quote");
    let quoteIndex = 0;

    console.log("Quotes found:", quotes.length); // Debug: Check if quotes are found

    if (quotes.length === 0) {
        console.error("No quotes found in the DOM. Check the HTML and CSS.");
    }

    function showNextQuote() {
        quotes.forEach(quote => quote.classList.remove("active"));
        quoteIndex = (quoteIndex + 1) % quotes.length;
        quotes[quoteIndex].classList.add("active");
        console.log("Showing quote index:", quoteIndex); // Debug: Confirm cycling
    }

    showNextQuote();
    setInterval(showNextQuote, 4000);

    // Get Started button logic
    document.getElementById("get-started").addEventListener("click", function () {
        this.textContent = "Loading...";
        this.disabled = true;
    
        fetch("/auth/check_profile")  // Fixed URL
            .then(response => response.json())
            .then(data => {
                console.log("Profile Check Response:", data); // Debugging
                if (data.complete) {
                    window.location.href = "/dashboard";
                } else {
                    window.location.href = "/profile_complete.html";
                }
            })
            .catch(error => {
                console.error("Error:", error);
                this.textContent = "Get Started";
                this.disabled = false;
            });
    });
});
    