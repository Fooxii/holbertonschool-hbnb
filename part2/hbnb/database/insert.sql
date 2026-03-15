-- ADMIN USER
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
'36c9050e-ddd3-4c3b-9731-9f487208bbc1',
'Admin',
'HBnB',
'admin@hbnb.io',
'$2b$12$replace_this_with_real_hash',
TRUE
);

-- AMENITIES
INSERT INTO amenities (id, name) VALUES
('11111111-1111-1111-1111-111111111111', 'WiFi'),
('22222222-2222-2222-2222-222222222222', 'Swimming Pool'),
('33333333-3333-3333-3333-333333333333', 'Air Conditioning');