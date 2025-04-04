CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    profile_completed BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS profile (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    age INT,
    gender ENUM('Male', 'Female', 'Other'),
    height FLOAT,
    weight FLOAT,
    fitness_goal TEXT,
    target_weight FLOAT,
    diet_preference TEXT,
    workout_time INT,
    workout_days INT,
    FOREIGN KEY (email) REFERENCES users(email) ON DELETE CASCADE
);
