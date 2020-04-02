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
	ingredient TEXT,
	quantity DOUBLE,
	unit TEXT,
	delivery DATE,
	last_delivery_amount DOUBLE,
    
	PRIMARY KEY (ingredient)
	CONSTRAINT
		ingredient_check CHECK (quantity >= 0) ON CONFLICT ROLLBACK
);

CREATE TABLE recipes (
	ingredient TEXT,
	cookie TEXT,
	quantity_needed DOUBLE,
    
	PRIMARY KEY (ingredient, cookie),
	FOREIGN KEY (ingredient) REFERENCES ingredients(ingredient),
	FOREIGN KEY (cookie) REFERENCES cookies(cookie)
);

CREATE TABLE cookies (
	cookie TEXT,
    
	PRIMARY KEY (cookie)
);

CREATE TABLE pallets (
	pallet_id TEXT DEFAULT (lower(hex(randomblob(16)))),
	cookie TEXT,
	blocked BOOLEAN DEFAULT (0),
	produced DATE DEFAULT (CURRENT_DATE),
	delivered DATE DEFAULT (NULL),
	customer TEXT DEFAULT (NULL),
    
	PRIMARY KEY (pallet_id),
	FOREIGN KEY (cookie) REFERENCES cookies(cookie)
	FOREIGN KEY (customer) REFERENCES customers(customer)
);

CREATE TABLE orders (
	order_id TEXT DEFAULT (lower(hex(randomblob(16)))),
	order_status BOOLEAN,
	ordered DATE,
	customer TEXT,
    
	PRIMARY KEY (order_id),
	FOREIGN KEY (customer) REFERENCES customers(customer)
);

CREATE TABLE cookie_orders (
	cookie TEXT,
	order_id TEXT,
	nbr_pallets INT,

	PRIMARY KEY (cookie, order_id),
	FOREIGN KEY (cookie) REFERENCES cookies(cookie),
	FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE customers (
	customer TEXT,
	customer_address TEXT,
    
	PRIMARY KEY (customer)
);


-- And re-enable foreign key checks.

PRAGMA foreign_key = on;