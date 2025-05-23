let supabase;
const SUPABASE_TIMEOUT_MS = 10000; // Increase timeout to 10 seconds for slower networks

// Function to dynamically load the Supabase script if not already loaded
function loadSupabaseScript() {
    return new Promise((resolve, reject) => {
        if (typeof window !== 'undefined' && window.supabase) {
            resolve();
            return;
        }

        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.39.0/dist/umd/supabase.min.js'; // Use a specific version
        script.async = true;
        script.onload = () => resolve();
        script.onerror = () => reject(new Error('Failed to load Supabase script'));
        document.head.appendChild(script);
    });
}

function initializeSupabase() {
    return new Promise((resolve, reject) => {
        const startTime = Date.now();
        console.log('Checking for Supabase library...');

        const checkInterval = setInterval(() => {
            if (typeof window !== 'undefined' && window.supabase && typeof window.supabase.createClient === 'function') {
                clearInterval(checkInterval);
                supabase = window.supabase.createClient('https://vvnnwsvgavjlsupidpgp.supabase.co', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZ2bm53c3ZnYXZqbHN1cGlkcGdwIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDUwMzY0NDYsImV4cCI6MjA2MDYxMjQ0Nn0.bf_65Q6wz1-brtfIjF13UuP6F1_X_GSyb8d-K2lXSxU');
                console.log('Supabase client initialized successfully');
                resolve(supabase);
            } else if (Date.now() - startTime > SUPABASE_TIMEOUT_MS) {
                clearInterval(checkInterval);
                console.error('Global scope dump:', Object.keys(window).join(', '));
                const scripts = document.getElementsByTagName('script');
                for (let script of scripts) {
                    console.log('Script src:', script.src);
                }
                reject(new Error('Supabase library not loaded or incompatible within timeout'));
            }
        }, 100); // Check every 100ms
    });
}

// Load the Supabase script and then initialize the client
loadSupabaseScript()
    .then(() => {
        console.log('Supabase script loaded successfully');
        return initializeSupabase();
    })
    .then((client) => {
        console.log('Supabase initialization completed');
        fetchWorkouts();
    })
    .catch(error => {
        console.error('Failed to initialize Supabase client:', error);
        // Fallback: Populate with mock data if Supabase fails to initialize
        window.workouts = [
            { id: 1, Title: 'Push-ups', Type: 'Strength', BodyPart: 'Chest', Level: 'Beginner' },
            { id: 2, Title: 'Squats', Type: 'Strength', BodyPart: 'Legs', Level: 'Intermediate' },
            { id: 3, Title: 'Running', Type: 'Cardio', BodyPart: 'Full Body', Level: 'Beginner' }
        ];
        populateDatalist(window.workouts.map(w => w.Title));
        alert('Failed to connect to the database. Using sample workout data instead.');
    });

window.workouts = [];

function filterWorkouts() {
    const workoutSearch = document.getElementById('workoutSearch');
    const workoutDatalist = document.getElementById('workouts');
    if (!window.workouts || !Array.isArray(window.workouts)) {
        console.warn('workouts is not an array:', window.workouts);
        return;
    }
    const searchTerm = workoutSearch.value.trim().toLowerCase();
    if (searchTerm.length === 0) {
        populateDatalist(window.workouts.map(w => w.Title));
        return;
    }
    const filteredWorkouts = window.workouts.filter(workout => {
        const title = workout.Title ? workout.Title.toLowerCase() : '';
        const type = workout.Type ? workout.Type.toLowerCase() : '';
        const bodyPart = workout.BodyPart ? workout.BodyPart.toLowerCase() : '';
        const level = workout.Level ? workout.Level.toLowerCase() : '';
        return title.includes(searchTerm) || type.includes(searchTerm) || bodyPart.includes(searchTerm) || level.includes(searchTerm);
    });
    populateDatalist(filteredWorkouts.map(w => w.Title));
}

function populateDatalist(workoutList) {
    const workoutDatalist = document.getElementById('workouts');
    workoutDatalist.innerHTML = '';
    workoutList.forEach(workout => {
        const option = document.createElement('option');
        option.value = workout;
        workoutDatalist.appendChild(option);
    });
}

async function fetchWorkouts() {
    if (!supabase) {
        console.error('Supabase client is not initialized, cannot fetch workouts');
        return;
    }
    try {
        console.log('Fetching workouts from:', 'https://vvnnwsvgavjlsupidpgp.supabase.co');
        const { data, error } = await supabase
            .from('Workouts') // Updated to match the confirmed table name
            .select('id, Title, Type, BodyPart, Level');
        if (error) {
            console.error('Error fetching workouts:', error);
            // Fallback to mock data if fetch fails
            window.workouts = [
                { id: 1, Title: 'Push-ups', Type: 'Strength', BodyPart: 'Chest', Level: 'Beginner' },
                { id: 2, Title: 'Squats', Type: 'Strength', BodyPart: 'Legs', Level: 'Intermediate' },
                { id: 3, Title: 'Running', Type: 'Cardio', BodyPart: 'Full Body', Level: 'Beginner' }
            ];
            console.log('Using mock data due to fetch error:', window.workouts);
            alert('Failed to fetch workouts from the database. Using sample data instead.');
        } else {
            window.workouts = data || [];
            console.log('Fetched workouts:', window.workouts);
        }
        populateDatalist(window.workouts.map(w => w.Title));
    } catch (e) {
        console.error('Unexpected error in fetchWorkouts:', e);
        // Fallback to mock data on unexpected error
        window.workouts = [
            { id: 1, Title: 'Push-ups', Type: 'Strength', BodyPart: 'Chest', Level: 'Beginner' },
            { id: 2, Title: 'Squats', Type: 'Strength', BodyPart: 'Legs', Level: 'Intermediate' },
            { id: 3, Title: 'Running', Type: 'Cardio', BodyPart: 'Full Body', Level: 'Beginner' }
        ];
        console.log('Using mock data due to unexpected error:', window.workouts);
        alert('Unexpected error fetching workouts. Using sample data instead.');
        populateDatalist(window.workouts.map(w => w.Title));
    }
}

function fetchHistory() {
    const history = [
        { id: 1, type: 'Cardio', date: '2025-04-17', sets: 3, reps: 15, weight: 0, duration: 30 },
        { id: 2, type: 'Strength', date: '2025-04-16', sets: 4, reps: 10, weight: 50, duration: 45 }
    ];
    renderHistory(history);
}

function renderHistory(history) {
    const historyPanel = document.getElementById('historyList');
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

function validateInput(workout) {
    return workout.date && !isNaN(workout.sets) && !isNaN(workout.reps) && !isNaN(workout.duration);
}

document.addEventListener('DOMContentLoaded', () => {
    const workoutForm = document.getElementById('workoutForm');
    let history = [];

    workoutForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const workoutSearch = document.getElementById('workoutSearch');
        const selectedWorkout = window.workouts.find(w => w.Title === workoutSearch.value);
        const workout = {
            id: history.length + 1,
            type: selectedWorkout ? selectedWorkout.Type : workoutSearch.value,
            date: document.getElementById('workoutDate').value,
            sets: parseInt(document.getElementById('sets').value),
            reps: parseInt(document.getElementById('reps').value),
            weight: parseInt(document.getElementById('weight').value) || 0,
            duration: parseInt(document.getElementById('duration').value)
        };

        if (validateInput(workout)) {
            if (!supabase) {
                console.error('Supabase client is not available for insertion');
                return;
            }
            const { error } = await supabase
                .from('workout_history')
                .insert(workout);
            if (error) console.error('Error logging workout:', error);
            else {
                history.push(workout);
                console.log('Workout logged:', workout);
                renderHistory(history);
                workoutForm.reset();
            }
        } else {
            alert('Please fill all required fields with valid numbers.');
        }
    });

    fetchHistory();

    const workoutSearch = document.getElementById('workoutSearch');
    workoutSearch.addEventListener('input', filterWorkouts);
});