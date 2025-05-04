CREATE TABLE qb_user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    contact VARCHAR(100)
);

CREATE TABLE hotel (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    imageUrl VARCHAR(255),
    description TEXT,
    rating DECIMAL(2,1),
    price DECIMAL(10,2),
    amenities TEXT,
    location VARCHAR(100)
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

INSERT INTO hotel (id, name, imageUrl, description, rating, price, amenities, location) VALUES
(1, 'Grand Hotel',
 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
 'Experience luxury in the heart of the city. This 5-star hotel offers spectacular views and world-class service.',
 4.8, 299,
 'Free WiFi,Spa,Pool,Restaurant,Gym',
 'Downtown'
);

INSERT INTO hotel (id, name, imageUrl, description, rating, price, amenities, location) VALUES
(2, 'Seaside Resort',
 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
 'Escape to paradise with our beachfront resort. Wake up to stunning ocean views and pristine beaches.',
 4.6, 399,
 'Beach Access,Pool,Spa,Water Sports,Bar',
 'Beachfront'
);

INSERT INTO hotel (id, name, imageUrl, description, rating, price, amenities, location) VALUES
(3, 'Mountain Lodge',
 'https://images.unsplash.com/photo-1517840901100-8179e982acb7?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
 'A cozy retreat nestled in the mountains. Perfect for nature lovers and adventure seekers.',
 4.7, 249,
 'Hiking Trails,Fireplace,Restaurant,Parking',
 'Mountain Range'
);

INSERT INTO hotel (id, name, imageUrl, description, rating, price, amenities, location) VALUES
(4, 'City Center Hotel',
 'https://images.unsplash.com/photo-1496417263034-38ec4f0b665a?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
 'Modern comfort meets urban convenience. Steps away from shopping, dining and entertainment.',
 4.5, 199,
 'Business Center,Restaurant,Fitness Center,Parking,Room Service',
 'City Center'
);

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

