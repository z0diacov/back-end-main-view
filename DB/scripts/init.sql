CREATE DATABASE db;
USE db;

CREATE TABLE programs (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    author_user_id BIGINT UNSIGNED NOT NULL,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    duration_weeks MEDIUMINT NOT NULL,
    cycle_number MEDIUMINT NOT NULL,
    picture BLOB NULL,
    private_comments TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE workouts (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    author_user_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    approx_duration_minutes MEDIUMINT NOT NULL,
    picture BLOB NULL,
    private_comments TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

ALTER TABLE workouts ADD INDEX workouts_author_user_id_index(author_user_id);
ALTER TABLE workouts ADD INDEX workouts_approx_duration_minutes_index(approx_duration_minutes);

CREATE TABLE program_workouts (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    program_id BIGINT UNSIGNED NOT NULL,
    workout_id BIGINT UNSIGNED NOT NULL,
    week_index MEDIUMINT NOT NULL,
    week_day ENUM('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday') NOT NULL,
    min_rest_hours MEDIUMINT NOT NULL,
    order_in_day TINYINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

ALTER TABLE program_workouts ADD INDEX program_workouts_program_id_workout_id_week_day_index(program_id, workout_id, week_day);
ALTER TABLE program_workouts ADD INDEX program_workouts_program_id_index(program_id);
ALTER TABLE program_workouts ADD INDEX program_workouts_workout_id_index(workout_id);
ALTER TABLE program_workouts ADD INDEX program_workouts_week_index_index(week_index);
ALTER TABLE program_workouts ADD INDEX program_workouts_week_day_index(week_day);
ALTER TABLE program_workouts ADD INDEX program_workouts_order_in_day_index(order_in_day);

CREATE TABLE workout_exercises (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    exercise_id BIGINT UNSIGNED NOT NULL,
    workout_id BIGINT UNSIGNED NOT NULL,
    sets TINYINT NOT NULL,
    reps TINYINT NOT NULL,
    rest_seconds_min MEDIUMINT NOT NULL,
    rest_seconds_max MEDIUMINT NOT NULL,
    order_in_workout MEDIUMINT NOT NULL,
    load_type ENUM('weight_kg', 'max_weight_percentage', 'rpe', 'rir', 'time_seconds') NOT NULL,
    load_amount MEDIUMINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(255) NOT NULL,
    name VARCHAR(200) NULL,
    password VARCHAR(64),
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);


ALTER TABLE users ADD INDEX users_email_index(email);
ALTER TABLE users ADD UNIQUE users_username_unique(username);
ALTER TABLE users ADD UNIQUE users_email_unique(email);

CREATE TABLE trainer_profiles (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    bio TEXT NOT NULL,
    balance BIGINT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

ALTER TABLE trainer_profiles ADD INDEX trainer_profiles_user_id_index(user_id);

CREATE TABLE calendar_workouts (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    workout_id BIGINT UNSIGNED NOT NULL,
    date DATETIME NOT NULL,
    status ENUM('planned', 'completed', 'skipped', 'completed_in_other_day') NOT NULL
);

ALTER TABLE calendar_workouts ADD INDEX calendar_workouts_user_id_workout_id_date_index(user_id, workout_id, date);
ALTER TABLE calendar_workouts ADD INDEX calendar_workouts_user_id_index(user_id);
ALTER TABLE calendar_workouts ADD INDEX calendar_workouts_workout_id_index(workout_id);
ALTER TABLE calendar_workouts ADD INDEX calendar_workouts_status_index(status);

CREATE TABLE subscriptions (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    author_user_id BIGINT UNSIGNED NOT NULL,
    description TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

ALTER TABLE subscriptions ADD INDEX subscriptions_author_user_id_index(author_user_id);

CREATE TABLE exercise_pictures (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    exercise_id BIGINT UNSIGNED NOT NULL,
    picture BLOB NOT NULL
);

ALTER TABLE exercise_pictures ADD INDEX exercise_pictures_exercise_id_index(exercise_id);

CREATE TABLE exercises (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    author_user_id BIGINT UNSIGNED NOT NULL,
    name VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    private_comments TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE package (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    author_user_id BIGINT UNSIGNED NOT NULL,
    description TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, 
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

ALTER TABLE package ADD INDEX package_author_user_id_index(author_user_id);

CREATE TABLE subscription_owners (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    subscription_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED  NOT NULL,
    owner_from DATETIME NOT NULL,
    owner_until DATETIME NOT NULL
);

ALTER TABLE subscription_owners ADD INDEX subscription_owners_subscription_id_index(subscription_id);
ALTER TABLE subscription_owners ADD INDEX subscription_owners_user_id_index(user_id);
ALTER TABLE subscription_owners ADD INDEX subscription_owners_owner_from_index(owner_from);
ALTER TABLE subscription_owners ADD INDEX subscription_owners_owner_until_index(owner_until);

CREATE TABLE package_owners (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    packet_id BIGINT UNSIGNED NOT NULL,
    user_id BIGINT UNSIGNED NOT NULL,
    owner_from DATETIME NOT NULL
);

ALTER TABLE package_owners ADD INDEX package_owners_packet_id_index(packet_id);
ALTER TABLE package_owners ADD INDEX package_owners_user_id_index(user_id);
ALTER TABLE package_owners ADD INDEX package_owners_owner_from_index(owner_from);

CREATE TABLE subscription_programs (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    subscription_id BIGINT UNSIGNED NOT NULL,
    program_id BIGINT UNSIGNED NOT NULL,
    price INT NOT NULL,
    added_at DATETIME NOT NULL
);

ALTER TABLE subscription_programs ADD INDEX subscriprion_programs_subscription_id_index(subscription_id);
ALTER TABLE subscription_programs ADD INDEX subscriprion_programs_program_id_index(program_id);
ALTER TABLE subscription_programs ADD INDEX subscriprion_programs_price_index(price);

CREATE TABLE package_programs (
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    package_id BIGINT UNSIGNED NOT NULL,
    program_id BIGINT UNSIGNED NOT NULL,
    price INT NOT NULL,
    added_at DATETIME NOT NULL
);

ALTER TABLE package_programs ADD INDEX package_programs_package_id_index(package_id);
ALTER TABLE package_programs ADD INDEX package_programs_program_id_index(program_id);
ALTER TABLE package_programs ADD INDEX package_programs_price_index(price);


CREATE TABLE reset_password_activity (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED,
    is_used BOOLEAN,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    reset_at DATETIME
);
ALTER TABLE reset_password_activity ADD INDEX reset_password_activity_id_index(id);
ALTER TABLE reset_password_activity ADD INDEX reset_password_activity_user_id_index(user_id);

CREATE TABLE login_activity (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED,
    login_status ENUM('google', 'classic'),
    logout_status ENUM('self', 'extra', 'strange', 'expired'),
    login_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    logout_at DATETIME
);
ALTER TABLE login_activity ADD INDEX login_activity_id_index(id);
ALTER TABLE login_activity ADD INDEX login_activity_user_id_index(user_id);

CREATE TABLE location_activity (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    activity_type ENUM('login', 'verify_email', 'reset_password') NOT NULL,
    activity_id BIGINT UNSIGNED NOT NULL,
    ip VARCHAR(45),
    os VARCHAR(255),
    browser VARCHAR(255),
    device VARCHAR(255),
    location_country VARCHAR(255),
    location_region VARCHAR(255),
    location_city VARCHAR(255),
    location_lat DECIMAL(9,6),
    location_lon DECIMAL(9,6)
);

ALTER TABLE location_activity ADD INDEX location_activity_id_index(id);
ALTER TABLE location_activity ADD INDEX location_activity_activity_type_index(activity_type);
ALTER TABLE location_activity ADD INDEX location_activity_activity_id_index(activity_id);
ALTER TABLE location_activity ADD INDEX location_activity_ip_index(ip);
ALTER TABLE location_activity ADD INDEX location_activity_location_country_index(location_country);

CREATE TABLE verify_email_activity (
    id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    verified_at DATETIME
);

ALTER TABLE verify_email_activity ADD INDEX verify_email_activity_id_index(id);
ALTER TABLE verify_email_activity ADD INDEX verify_email_activity_user_id_index(user_id);

ALTER TABLE workout_exercises ADD CONSTRAINT workout_exercises_exercise_id_foreign FOREIGN KEY(exercise_id) REFERENCES exercises(id);
ALTER TABLE program_workouts ADD CONSTRAINT program_workouts_program_id_foreign FOREIGN KEY(program_id) REFERENCES programs(id);
ALTER TABLE programs ADD CONSTRAINT programs_author_user_id_foreign FOREIGN KEY(author_user_id) REFERENCES users(id);
ALTER TABLE package ADD CONSTRAINT package_author_user_id_foreign FOREIGN KEY(author_user_id) REFERENCES users(id);
ALTER TABLE calendar_workouts ADD CONSTRAINT calendar_workouts_workout_id_foreign FOREIGN KEY(workout_id) REFERENCES workouts(id);
ALTER TABLE exercise_pictures ADD CONSTRAINT exercise_pictures_exercise_id_foreign FOREIGN KEY(exercise_id) REFERENCES exercises(id);
ALTER TABLE subscriptions ADD CONSTRAINT subscriptions_author_user_id_foreign FOREIGN KEY(author_user_id) REFERENCES users(id);
ALTER TABLE subscription_owners ADD CONSTRAINT subscription_owners_subscription_id_foreign FOREIGN KEY(subscription_id) REFERENCES subscriptions(id);
ALTER TABLE calendar_workouts ADD CONSTRAINT calendar_workouts_user_id_foreign FOREIGN KEY(user_id) REFERENCES users(id);
ALTER TABLE program_workouts ADD CONSTRAINT program_workouts_workout_id_foreign FOREIGN KEY(workout_id) REFERENCES workouts(id);
ALTER TABLE exercises ADD CONSTRAINT exercises_author_user_id_foreign FOREIGN KEY(author_user_id) REFERENCES users(id);
ALTER TABLE package_programs ADD CONSTRAINT package_programs_program_id_foreign FOREIGN KEY(program_id) REFERENCES programs(id);
ALTER TABLE workouts ADD CONSTRAINT workouts_author_user_id_foreign FOREIGN KEY(author_user_id) REFERENCES users(id);
ALTER TABLE package_programs ADD CONSTRAINT package_programs_package_id_foreign FOREIGN KEY(package_id) REFERENCES package(id);
ALTER TABLE subscription_programs ADD CONSTRAINT subscriprion_programs_subscription_id_foreign FOREIGN KEY(subscription_id) REFERENCES subscriptions(id);
ALTER TABLE package_owners ADD CONSTRAINT package_owners_packet_id_foreign FOREIGN KEY(packet_id) REFERENCES package(id);
ALTER TABLE package_owners ADD CONSTRAINT package_owners_user_id_foreign FOREIGN KEY(user_id) REFERENCES users(id);
ALTER TABLE workout_exercises ADD CONSTRAINT workout_exercises_workout_id_foreign FOREIGN KEY(workout_id) REFERENCES workouts(id);
ALTER TABLE trainer_profiles ADD CONSTRAINT trainer_profiles_user_id_foreign FOREIGN KEY(user_id) REFERENCES users(id);
ALTER TABLE subscription_owners ADD CONSTRAINT subscription_owners_user_id_foreign FOREIGN KEY(user_id) REFERENCES users(id);
ALTER TABLE subscription_programs ADD CONSTRAINT subscriprion_programs_program_id_foreign FOREIGN KEY(program_id) REFERENCES programs(id);
ALTER TABLE reset_password_activity ADD CONSTRAINT reset_password_activity_user_id_foreign FOREIGN KEY (user_id) REFERENCES users(id);
ALTER TABLE login_activity ADD CONSTRAINT login_activity_id_foreign FOREIGN KEY (user_id) REFERENCES users(id);