CREATE TABLE qb_user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(100)
);

CREATE TABLE hotel (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE hotel_room (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hotel_id INT NOT NULL,
    type VARCHAR(50) NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotel(id) ON DELETE CASCADE
);

CREATE TABLE hotel_room_reservation (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hotel_id INT NOT NULL,
    room_id INT NOT NULL,
    from_date DATE NOT NULL,
    to_date DATE NOT NULL,
    user_id INT NOT NULL,
    contact VARCHAR(100) NOT NULL,
    FOREIGN KEY (hotel_id) REFERENCES hotel(id) ON DELETE CASCADE,
    FOREIGN KEY (room_id) REFERENCES hotel_room(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES qb_user(id) ON DELETE CASCADE
);

-- Insert 2 sample hotels
INSERT INTO hotel (name) VALUES ('Ocean View Resort'), ('Mountain Escape Lodge');

-- Assuming hotel IDs are auto-incremented as 1 and 2, insert 5 rooms for each
INSERT INTO hotel_room (hotel_id, type) VALUES
-- Rooms for hotel ID 1
(1, 'Deluxe'),
(1, 'Standard'),
(1, 'Suite'),
(1, 'Standard'),
(1, 'Deluxe'),

-- Rooms for hotel ID 2
(2, 'Standard'),
(2, 'Deluxe'),
(2, 'Suite'),
(2, 'Standard'),
(2, 'Deluxe');

-- Insert 2 sample users
INSERT INTO qb_user (name, contact) VALUES
('Alice Johnson', 'alice@example.com'),
('Bob Smith', 'bob@example.com');


INSERT INTO hotel_room_reservation (hotel_id, room_id, from_date, to_date, user_id) VALUES
(1, 1, '2025-05-10', '2025-05-12', 1),  -- Alice books room 1 in Hotel 1
(1, 2, '2025-05-11', '2025-05-13', 2),  -- Bob books room 2 in Hotel 1
(2, 6, '2025-05-15', '2025-05-18', 1);  -- Alice books room 6 in Hotel 2

