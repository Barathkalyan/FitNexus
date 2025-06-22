document.addEventListener("DOMContentLoaded", () => {
    const saveBtn = document.getElementById("saveChangesBtn");
    const errorElement = document.getElementById("formError");

    if (saveBtn) {
        saveBtn.addEventListener("click", async () => {
            saveBtn.disabled = true;
            saveBtn.innerText = "Saving...";

            if (errorElement) errorElement.innerText = "";

            // Collect data from all input fields
            const data = {
                name: document.getElementById("name").value,
                email: document.getElementById("email").value,
                age: document.getElementById("age").value,
                gender: document.getElementById("gender").value,
                height: document.getElementById("height").value,
                weight: document.getElementById("weight").value,
                fitness_goal: document.getElementById("goal").value,
                target_weight: document.getElementById("target_weight").value,
                diet: document.getElementById("diet").value,
                workout_time: document.getElementById("workout_time").value,
                workout_days: document.getElementById("workout_days").value
            };

            try {
                const res = await fetch("/profile", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify(data)
                });

                const result = await res.json();
                if (res.ok) {
                    window.location.href = result.redirect;
                } else {
                    if (errorElement) errorElement.innerText = result.error || "Something went wrong!";
                }
            } catch (err) {
                console.error("Error:", err);
                if (errorElement) errorElement.innerText = "Server error!";
            }

            saveBtn.disabled = false;
            saveBtn.innerText = "Save Changes";
        });
    }

    // Profile Dropdown Toggle
    const profileBtn = document.getElementById("profileBtn");
    const dropdown = document.getElementById("profileDropdown");

    if (profileBtn && dropdown) {
        profileBtn.addEventListener("click", () => {
            dropdown.classList.toggle("show");
        });

        document.addEventListener("click", (event) => {
            if (!profileBtn.contains(event.target) && !dropdown.contains(event.target)) {
                dropdown.classList.remove("show");
            }
        });
    }

    // Logout Button
    const logoutBtn = document.getElementById("logoutBtn");
    if (logoutBtn) {
        logoutBtn.addEventListener("click", () => {
            window.location.href = "/auth/logout";
        });
    }
});