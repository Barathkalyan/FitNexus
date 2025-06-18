let supabase;
const SUPABASE_TIMEOUT_MS = 10000;

// Function to dynamically load the Supabase script if not already loaded
function loadSupabaseScript() {
    return new Promise((resolve, reject) => {
        if (typeof window !== 'undefined' && window.supabase) {
            resolve();
            return;
        }

        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.39.0/dist/umd/supabase.min.js';
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
        }, 100);
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
            .from('Workouts')
            .select('id, Title, Type, BodyPart, Level');
        if (error) {
            console.error('Error fetching workouts:', error);
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

async function fetchHistory() {
    if (!supabase) {
        console.error('Supabase client is not initialized, cannot fetch history');
        return;
    }
    try {
        const { data, error } = await supabase
            .from('workout_history')
            .select('id, type, date, sets, duration, sets_data')
            .order('date', { ascending: false });
        if (error) {
            console.error('Error fetching workout history:', error);
            renderHistory([]);
        } else {
            renderHistory(data || []);
        }
    } catch (e) {
        console.error('Unexpected error in fetchHistory:', e);
        renderHistory([]);
    }
}

function renderHistory(history) {
    const historyPanel = document.getElementById('historyList');
    historyPanel.innerHTML = '';
    if (history.length === 0) {
        const entry = document.createElement('div');
        entry.className = 'history-entry stat-card';
        entry.innerHTML = `
            <p class="stat-title">No Workouts Logged</p>
            <p class="stat-value">Start logging your workouts above!</p>
        `;
        historyPanel.appendChild(entry);
        return;
    }
    history.forEach(item => {
        const entry = document.createElement('div');
        entry.className = 'history-entry stat-card';
        const setsData = item.sets_data || [{ reps: 0, weight: 0.0 }];
        const progressWidth = Math.min((item.duration / 60) * 10, 100);
        entry.innerHTML = `
            <p class="stat-title">${item.date} - ${item.type}</p>
            <p>Sets: ${item.sets}</p>
            <p>Reps: ${setsData[0].reps}</p>
            <p>Weight: ${setsData[0].weight}kg</p>
            <p>Duration: ${item.duration}min</p>
            <div class="progress-bar" style="width: ${progressWidth}%;"></div>
        `;
        entry.addEventListener('click', () => showDetails(item));
        historyPanel.appendChild(entry);
    });
}

function showDetails(item) {
    const modal = document.createElement('div');
    modal.className = 'detail-modal';
    const setsData = item.sets_data || [{ reps: 0, weight: 0.0 }];
    modal.innerHTML = `
        <div class="detail-content">
            <h3>${item.date} - ${item.type}</h3>
            <p>Total Sets: ${item.sets}</p>
            <p>Duration: ${item.duration}min</p>
            ${setsData.map((set, index) => `
                <p>Set ${index + 1}: ${set.reps} reps @ ${set.weight}kg</p>
            `).join('')}
            <button class="close-btn">Close</button>
        </div>
    `;
    document.body.appendChild(modal);

    modal.querySelector('.close-btn').addEventListener('click', () => {
        document.body.removeChild(modal);
    });
}

function validateInput(workout) {
    return workout.date && !isNaN(workout.sets) && !isNaN(workout.duration) && Array.isArray(workout.sets_data) && workout.sets_data.length > 0 && workout.sets_data.every(set => !isNaN(set.reps) && !isNaN(set.weight));
}

document.addEventListener('DOMContentLoaded', () => {
    const workoutSearch = document.getElementById('workoutSearch');
    workoutSearch.addEventListener('input', filterWorkouts);

    const workoutForm = document.getElementById('workoutForm');
    workoutForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const submitBtn = workoutForm.querySelector('.log-btn');
        submitBtn.disabled = true;
        submitBtn.textContent = 'Logging...';

        const setsContainer = document.getElementById('setsContainer');
        const setGroups = setsContainer.querySelectorAll('.set-group');
        const setsData = Array.from(setGroups).map(group => ({
            reps: parseInt(group.querySelector('.set-reps').value) || 0,
            weight: parseFloat(group.querySelector('.set-weight').value) || 0.0
        }));

        const workout = {
            type: window.workouts.find(w => w.Title === workoutForm.workoutSearch.value)?.Type || workoutForm.workoutSearch.value,
            date: workoutForm.workoutDate.value,
            sets: setGroups.length,
            duration: parseInt(workoutForm.duration.value) || 0,
            sets_data: setsData
        };

        console.log('Submitting workout:', workout); // Debug log

        if (validateInput(workout)) {
            if (!supabase) {
                console.error('Supabase client is not available for insertion');
                submitBtn.disabled = false;
                submitBtn.textContent = 'Log Workout';
                return;
            }
            try {
                const { error } = await supabase
                    .from('workout_history')
                    .insert(workout);
                if (error) {
                    console.error('Error logging workout:', error.message, error.details);
                    alert(`Failed to log workout: ${error.message}`);
                } else {
                    console.log('Workout logged:', workout);
                    alert('Workout logged successfully!');
                    workoutForm.reset();
                    setsContainer.innerHTML = `
                        <div class="set-group" data-set="1">
                            <div class="input-group">
                                <label>Reps (Set 1)</label>
                                <input type="number" class="set-reps" placeholder="Reps" min="1" required>
                            </div>
                            <div class="input-group">
                                <label>Weight (kg)</label>
                                <input type="number" class="set-weight" placeholder="Weight (kg)" min="0" step="0.1">
                            </div>
                            <button type="button" class="remove-set">×</button>
                        </div>
                    `;
                    fetchHistory();
                }
            } catch (e) {
                console.error('Unexpected error during insertion:', e);
                alert('Unexpected error logging workout. Check console for details.');
            }
        } else {
            alert('Please fill all required fields with valid numbers.');
        }

        submitBtn.disabled = false;
        submitBtn.textContent = 'Log Workout';
    });

    fetchHistory();
});