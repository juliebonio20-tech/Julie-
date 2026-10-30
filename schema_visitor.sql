CREATE DATABASE IF NOT EXISTS visitor_log_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE visitor_log_db;

CREATE TABLE IF NOT EXISTS visitor_log (
  id INT AUTO_INCREMENT PRIMARY KEY,
  visitor_no VARCHAR(12) NOT NULL UNIQUE,
  full_name VARCHAR(150) NOT NULL,
  company_office VARCHAR(120) NULL,
  id_type VARCHAR(30) NOT NULL,
  id_no VARCHAR(40) NOT NULL,
  purpose VARCHAR(160) NOT NULL,
  person_to_visit VARCHAR(120) NOT NULL,
  contact_no VARCHAR(20) NULL,
  time_in TIME NOT NULL,
  time_out TIME NULL,
  guard_on_duty VARCHAR(100) NOT NULL,
  remarks VARCHAR(255) NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'Nasa Loob',
  logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

#pwedi alidan