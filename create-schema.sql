-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.

PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS cookies;
DROP TABLE IF EXISTS pallets;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS cookie_orders;
DROP TABLE IF EXISTS customers;


-- Creating the tables


CREATE TABLE ingredients (
	ingredient_name TEXT,
	quantity DOUBLE,
	unit TEXT,
	delivery DATE,
	last_delivery_amount DOUBLE,
    
	PRIMARY KEY (ingredient_name)
);

CREATE TABLE recipes (
	ingredient_name TEXT,
	cookie_name TEXT,
	quantity_needed DOUBLE,
    
	PRIMARY KEY (ingredient_name, cookie_name),
	FOREIGN KEY (ingredient_name) REFERENCES ingredients(ingredient_name),
	FOREIGN KEY (cookie_name) REFERENCES cookies(cookie_name)
);

CREATE TABLE cookies (
	cookie_name TEXT,
    
	PRIMARY KEY (cookie_name)
);

CREATE TABLE pallets (
	pallet_id TEXT DEFAULT (lower(hex(randomblob(16)))),
	cookie_name TEXT,
	blocked BOOLEAN DEFAULT (0),
	produced DATE DEFAULT (CURRENT_DATE),
	delivered DATE DEFAULT (NULL),
	customer_name TEXT DEFAULT (NULL),
    
	PRIMARY KEY (pallet_id),
	FOREIGN KEY (cookie_name) REFERENCES cookies(cookie_name)
	FOREIGN KEY (customer_name) REFERENCES customers(customer_name)
);

CREATE TABLE orders (
	order_id TEXT DEFAULT (lower(hex(randomblob(16)))),
	no_pallets INT,
	order_status BOOLEAN,
	ordered DATE,
	cookie_name TEXT,
	customer_name TEXT,
    
	PRIMARY KEY (order_id),
	FOREIGN KEY (cookie_name) REFERENCES cookies(cookie_name),
	FOREIGN KEY (customer_name) REFERENCES customers(customer_name)
);

CREATE TABLE cookie_orders (
	cookie_name TEXT,
    	order_id TEXT,

	PRIMARY KEY (cookie_name, order_id),
	FOREIGN KEY (cookie_name) REFERENCES cookies(cookie_name),
	FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE customers (
	customer_name TEXT,
	customer_address TEXT,
    
	PRIMARY KEY (customer_name)
);


-- And re-enable foreign key checks.

PRAGMA foreign_key = on;