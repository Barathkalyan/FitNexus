document.addEventListener('DOMContentLoaded', () => {
    const workoutForm = document.getElementById('workoutForm');
    const historyPanel = document.getElementById('historyPanel');

    let history = [];

    // Simulated Supabase fetch
    function fetchHistory() {
        // Replace with real Supabase fetch
        history = [
            { id: 1, type: 'Cardio', date: '2025-04-17', sets: 3, reps: 15, weight: 0, duration: 30 },
            { id: 2, type: 'Strength', date: '2025-04-16', sets: 4, reps: 10, weight: 50, duration: 45 }
        ];
        renderHistory();
    }

    // Render history cards
    function renderHistory() {
        historyPanel.innerHTML = '';
        history.forEach(item => {
            const card = document.createElement('div');
            card.className = 'history-card';
            card.innerHTML = `
                <p>Type: ${item.type}</p>
                <p>Date: ${item.date}</p>
                <p>Sets: ${item.sets}</p>
                <p>Reps: ${item.reps}</p>
                <p>Weight: ${item.weight}kg</p>
                <p>Duration: ${item.duration}min</p>
            `;
            historyPanel.appendChild(card);
        });
    }

    // Form submission
    workoutForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const workout = {
            id: history.length + 1,
            type: document.getElementById('workoutType').value,
            date: document.getElementById('date').value,
            sets: parseInt(document.getElementById('sets').value),
            reps: parseInt(document.getElementById('reps').value),
            weight: parseInt(document.getElementById('weight').value) || 0,
            duration: parseInt(document.getElementById('duration').value)
        };

        if (validateInput(workout)) {
            history.push(workout);
            // Simulate Supabase save
            console.log('Workout logged:', workout);
            renderHistory();
            workoutForm.reset();
        } else {
            alert('Please fill all required fields with valid numbers.');
        }
    });

    // Input validation
    function validateInput(workout) {
        return workout.date && !isNaN(workout.sets) && !isNaN(workout.reps) && !isNaN(workout.duration);
    }

    fetchHistory();
});