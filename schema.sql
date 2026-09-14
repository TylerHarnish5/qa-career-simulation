PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    full_name TEXT NOT NULL
);

CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    category TEXT NOT NULL,
    price_cents INTEGER NOT NULL,
    stock INTEGER NOT NULL,
    image_label TEXT NOT NULL
);

CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    customer_name TEXT NOT NULL,
    email TEXT NOT NULL,
    address TEXT NOT NULL,
    city TEXT NOT NULL,
    postal_code TEXT NOT NULL,
    shipping_method TEXT NOT NULL,
    shipping_cents INTEGER NOT NULL,
    subtotal_cents INTEGER NOT NULL,
    total_cents INTEGER NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    product_name TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price_cents INTEGER NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO users (username, password, full_name) VALUES
    ('alex.morgan', 'Welcome123!', 'Alex Morgan'),
    ('sam.lee', 'Testing2026!', 'Sam Lee');

INSERT INTO products (name, description, category, price_cents, stock, image_label) VALUES
    ('Trailhead Daypack', 'A lightweight 18L daypack with padded straps and a weather-resistant finish.', 'Bags', 6800, 14, 'TP'),
    ('Ridge Merino Beanie', 'Soft merino-blend knit beanie for brisk mornings and campfire evenings.', 'Apparel', 2400, 32, 'RB'),
    ('Cedar Camp Mug', 'Enamel-style 12 oz mug with a rolled rim and speckled evergreen glaze.', 'Camp Kitchen', 1800, 25, 'CM'),
    ('Northstar Headlamp', 'Rechargeable 350-lumen headlamp with two brightness levels and red-light mode.', 'Gear', 4200, 9, 'NH'),
    ('Alpine Field Journal', 'Water-resistant pocket notebook with dot-grid pages and a durable canvas cover.', 'Accessories', 1600, 40, 'AJ'),
    ('Maplewood Bottle', 'Insulated 20 oz stainless steel bottle that keeps drinks cold on the trail.', 'Camp Kitchen', 3200, 18, 'MB'),
    ('Waypoint Compass', 'Baseplate compass with luminous markings and an easy-to-read rotating bezel.', 'Gear', 2900, 12, 'WC'),
    ('Harbor Canvas Tote', 'Structured everyday tote in waxed canvas with an interior zip pocket.', 'Bags', 5400, 7, 'HT'),
    ('Summit Crew Socks', 'Cushioned wool-blend crew socks built for day hikes and daily wear.', 'Apparel', 2100, 28, 'SS'),
    ('Pinecone Key Clip', 'Compact anodized key clip with a spring gate and split ring.', 'Accessories', 1200, 50, 'PK');
