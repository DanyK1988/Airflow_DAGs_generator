-- schedule: @once

CREATE TABLE IF NOT EXISTS dag_test (
    id SERIAL PRIMARY KEY,
    name TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO dag_test (name) VALUES
('Alice'),
('Bob'),
('Charlie');

SELECT * FROM dag_test;