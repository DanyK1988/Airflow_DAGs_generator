-- schedule: @once

CREATE TABLE IF NOT EXISTS users_demo (
    id SERIAL PRIMARY KEY,
    username TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users_demo (username) VALUES
('john'),
('maria'),
('alex');

SELECT * FROM users_demo;