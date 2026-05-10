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
-- Coordinates: Blackrock DART (53.3015, -6.1775), Smurfit (53.3003, -6.1858), Belfield Village (53.3069, -6.2234)
INSERT INTO vehicles (license_plate, capacity, current_lat, current_lng, status) VALUES
    ('BUS-001', 30, 53.3015, -6.1775, 'active'),
    ('BUS-002', 30, 53.3003, -6.1858, 'idle'),
    ('BUS-003', 20, 53.3069, -6.2234, 'active');

-- Morning: DART 07:50 → Smurfit 08:00 → Belfield 08:20
-- Morning: DART 09:00 → Smurfit 09:10 → Belfield 09:30
-- Morning: DART 10:10 → Smurfit 10:20 → Belfield 10:40
-- Evening: Belfield 16:00 → Smurfit 16:20 → DART 16:30
-- Evening: Belfield 17:10 → Smurfit 17:30 → DART 17:40
-- Evening: Belfield 18:20 → Smurfit 18:40 → DART 18:50
INSERT INTO schedules (vehicle_id, route, departure_time, available_seats) VALUES
    (1, 'Blackrock DART → Belfield', CONCAT(CURDATE(), ' 07:50:00'), 28),
    (2, 'Blackrock DART → Belfield', CONCAT(CURDATE(), ' 09:00:00'), 30),
    (3, 'Blackrock DART → Belfield', CONCAT(CURDATE(), ' 10:10:00'), 20),
    (1, 'Belfield → Blackrock DART', CONCAT(CURDATE(), ' 16:00:00'), 28),
    (2, 'Belfield → Blackrock DART', CONCAT(CURDATE(), ' 17:10:00'), 30),
    (3, 'Belfield → Blackrock DART', CONCAT(CURDATE(), ' 18:20:00'), 20);
