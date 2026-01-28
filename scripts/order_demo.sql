-- schedule: */5 * * * *

CREATE TABLE IF NOT EXISTS orders_demo (
    id SERIAL PRIMARY KEY,
    user_name TEXT,
    amount INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO orders_demo (user_name, amount) VALUES
('john', 100),
('maria', 250),
('alex', 180);

SELECT user_name, SUM(amount) AS total
FROM orders_demo
GROUP BY user_name;