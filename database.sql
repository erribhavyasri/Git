CREATE DATABASE IF NOT EXISTS smart_city_db;
USE smart_city_db;

CREATE TABLE IF NOT EXISTS citizens(
 id INT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 email VARCHAR(120) UNIQUE NOT NULL,
 phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS services(
 id INT AUTO_INCREMENT PRIMARY KEY,
 name VARCHAR(120) NOT NULL,
 department VARCHAR(100) NOT NULL,
 status ENUM('Active','Inactive') DEFAULT 'Active'
);

CREATE TABLE IF NOT EXISTS complaints(
 id INT AUTO_INCREMENT PRIMARY KEY,
 citizen_id INT,
 title VARCHAR(200) NOT NULL,
 category VARCHAR(100) NOT NULL,
 description TEXT NOT NULL,
 status ENUM('Open','In Progress','Resolved') DEFAULT 'Open',
 created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(citizen_id) REFERENCES citizens(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS security_alerts(
 id INT AUTO_INCREMENT PRIMARY KEY,
 source_ip VARCHAR(45) NOT NULL,
 title VARCHAR(255) NOT NULL,
 severity ENUM('Low','Medium','High') NOT NULL,
 network_bytes FLOAT,
 failed_logins FLOAT,
 request_count FLOAT,
 cpu_usage FLOAT,
 status ENUM('Open','Closed') DEFAULT 'Open',
 created_at DATETIME
);

INSERT IGNORE INTO citizens(name,email,phone) VALUES
('Ravi Kumar','ravi@example.com','9876543210'),
('Priya Sharma','priya@example.com','9876501234');

INSERT IGNORE INTO services(name,department,status) VALUES
('Water Supply Complaint','Water Department','Active'),
('Street Light Request','Electrical Department','Active'),
('Waste Collection Request','Sanitation Department','Active');
