-- create tables
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user', 'viewer') NOT NULL
);

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    stock_quantity INT NOT NULL
);

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_date DATETIME NOT NULL,
    status ENUM('pending', 'completed', 'cancelled') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS order_products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- create integrator role
CREATE ROLE IF NOT EXISTS role_integrator;

-- grant permissions to role_integrator
GRANT SELECT(id, email, role) ON users TO role_integrator;
GRANT SELECT ON products TO 'role_integrator';
GRANT UPDATE(description, stock_quantity) ON products TO 'role_integrator';

GRANT SELECT, INSERT, UPDATE ON orders TO role_integrator;
GRANT SELECT, INSERT, UPDATE ON order_products TO role_integrator;

-- create integrator user
CREATE USER IF NOT EXISTS 'integrator'@'%' IDENTIFIED BY 'verysecret';

-- assign integrator role to integrator user
GRANT role_integrator TO 'integrator'@'%';

FLUSH PRIVILEGES;

-- test data
INSERT INTO users (email, password, role) VALUES
('admin@example.com', 'password123', 'admin'),
('user@example.com', 'password123', 'user'),
('viewer@example.com', 'password123', 'viewer');

INSERT INTO products (name, description, price, stock_quantity) VALUES
('Laptop', 'A high-performance laptop suitable for all your computing needs.', 1200.00, 10),
('Smartphone', 'A latest model smartphone with high-resolution camera.', 800.00, 15),
('Headphones', 'Noise-cancelling headphones for a superior audio experience.', 150.00, 20),
('Tablet', 'A portable tablet for all your entertainment needs.', 500.00, 5),
('Smartwatch', 'A smartwatch that tracks your fitness and health.', 300.00, 10),
('Camera', 'A professional camera for capturing high-quality images.', 2000.00, 5),
('Printer', 'A wireless printer for all your printing needs.', 300.00, 10),
('Monitor', 'A high-resolution monitor for a superior viewing experience.', 400.00, 10);

INSERT INTO orders (user_id, order_date, status) VALUES
(2, NOW(), 'pending'),
(2, NOW(), 'completed'),
(2, NOW(), 'cancelled'),
(3, NOW(), 'pending'),
(3, NOW(), 'completed'),
(3, NOW(), 'pending');

INSERT INTO order_products (order_id, product_id, quantity) VALUES
(1, 1, 1),
(1, 3, 2),
(1, 2, 1),
(2, 4, 4),
(3, 5, 1),
(3, 6, 3),
(4, 2, 3),
(5, 3, 3),
(6, 4, 3);
