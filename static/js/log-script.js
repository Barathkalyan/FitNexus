const supabaseUrl = 'https://vnnnswgavj1supidggp.supabase.co';
const supabaseKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ2bm53c3ZnYXZqbHN1cGlkcGdwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUwMzY0NDYsImV4cCI6MjA2MDYxMjQ0Nn0.bf_65Q6wz1-brtfIjF13UuP6F1_X_GSyb8d-K2lXSxU'; // Replace with full key
const supabase = supabase.createClient(supabaseUrl, supabaseKey);

document.addEventListener('DOMContentLoaded', () => {
    const workoutForm = document.getElementById('workoutForm');
    const historyPanel = document.getElementById('historyList');
    const workoutSearch = document.getElementById('workoutSearch');
    const workoutDatalist = document.getElementById('workouts');
    let history = [];
    let workouts = [];

    // Fetch workouts from Supabase
    async function fetchWorkouts() {
        console.log('Fetching workouts from:', supabaseUrl);
        const { data, error } = await supabase
            .from('workouts')
            .select('Title');
        if (error) console.error('Error fetching workouts:', error);
        else {
            workouts = data.map(item => item.Title);
            console.log('Fetched workouts:', workouts);
            populateDatalist(workouts);
        }
    }

    // Populate datalist with workouts
    function populateDatalist(workoutList) {
        workoutDatalist.innerHTML = '';
        workoutList.forEach(workout => {
            const option = document.createElement('option');
            option.value = workout;
            workoutDatalist.appendChild(option);
        });
    }

    // Filter workouts based on search input
    function filterWorkouts() {
        const searchTerm = workoutSearch.value.toLowerCase();
        const filteredWorkouts = workouts.filter(workout =>
            workout.toLowerCase().includes(searchTerm)
        );
        populateDatalist(filteredWorkouts);
    }

    // Simulated Supabase fetch for history
    function fetchHistory() {
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
    workoutForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const workout = {
            id: history.length + 1,
            type: workoutSearch.value,
            date: document.getElementById('workoutDate').value,
            sets: parseInt(document.getElementById('sets').value),
            reps: parseInt(document.getElementById('reps').value),
            weight: parseInt(document.getElementById('weight').value) || 0,
            duration: parseInt(document.getElementById('duration').value)
        };

        if (validateInput(workout)) {
            const { error } = await supabase
                .from('workout_history')
                .insert(workout);
            if (error) console.error('Error logging workout:', error);
            else {
                history.push(workout);
                console.log('Workout logged:', workout);
                renderHistory();
                workoutForm.reset();
            }
        } else {
            alert('Please fill all required fields with valid numbers.');
        }
    });

    // Input validation
    function validateInput(workout) {
        return workout.date && !isNaN(workout.sets) && !isNaN(workout.reps) && !isNaN(workout.duration);
    }

    fetchWorkouts();
    fetchHistory();
});