CREATE DATABASE IF NOT EXISTS shuttle_tracking CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE shuttle_tracking;

CREATE TABLE vehicles (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    license_plate   VARCHAR(20)  NOT NULL UNIQUE,
    capacity        INT          NOT NULL,
    current_lat     DOUBLE       NOT NULL DEFAULT 0.0,
    current_lng     DOUBLE       NOT NULL DEFAULT 0.0,
    status          ENUM('active', 'idle', 'maintenance') NOT NULL DEFAULT 'idle',
    updated_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE schedules (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    vehicle_id      INT          NOT NULL,
    route           VARCHAR(100) NOT NULL,
    departure_time  DATETIME     NOT NULL,
    available_seats INT          NOT NULL,
    created_at      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(id) ON DELETE CASCADE,
    INDEX idx_route_departure (route, departure_time)
);

CREATE TABLE demand_records (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    route           VARCHAR(100) NOT NULL,
    timestamp       DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    passenger_count INT          NOT NULL,
    INDEX idx_route_timestamp (route, timestamp)
);

-- Seed data
INSERT INTO vehicles (license_plate, capacity, current_lat, current_lng, status) VALUES
    ('BUS-001', 30, 31.2304, 121.4737, 'active'),
    ('BUS-002', 30, 31.2315, 121.4750, 'idle'),
    ('BUS-003', 20, 31.2290, 121.4720, 'active');

INSERT INTO schedules (vehicle_id, route, departure_time, available_seats) VALUES
    (1, 'Main Gate → Library', DATE_ADD(NOW(), INTERVAL 10 MINUTE), 28),
    (1, 'Main Gate → Dorm A',  DATE_ADD(NOW(), INTERVAL 40 MINUTE), 30),
    (2, 'Library → Lab Building', DATE_ADD(NOW(), INTERVAL 15 MINUTE), 25),
    (3, 'Dorm A → Cafeteria', DATE_ADD(NOW(), INTERVAL 5 MINUTE), 18);
