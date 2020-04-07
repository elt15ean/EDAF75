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
	name TEXT,
	quantity_in_stock DOUBLE,
	unit TEXT,
	delivery DATE,
	last_delivery_amount DOUBLE,
    
	PRIMARY KEY (name),
	CONSTRAINT
		ingredient_check CHECK (quantity_in_stock >= 0) ON CONFLICT ROLLBACK
);

CREATE TABLE recipes (
	ingredient TEXT,
	cookie TEXT,
	quantity DOUBLE,
    
	PRIMARY KEY (ingredient, cookie),
	FOREIGN KEY (ingredient) REFERENCES ingredients(name),
	FOREIGN KEY (cookie) REFERENCES cookies(name)
);

CREATE TABLE cookies (
	name TEXT,
    
	PRIMARY KEY (name)
);

CREATE TABLE pallets (
	pallet_id TEXT DEFAULT (lower(hex(randomblob(16)))),
	cookie TEXT,
	blocked BOOLEAN DEFAULT (0),
	produced DATE DEFAULT (CURRENT_DATE),
	delivered DATE DEFAULT (NULL),
	order_id TEXT DEFAULT (NULL),
    
	PRIMARY KEY (pallet_id),
	FOREIGN KEY (cookie) REFERENCES cookies(name),
	FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE orders (
	order_id TEXT DEFAULT (lower(hex(randomblob(16)))),
	order_status BOOLEAN,
	ordered DATE,
	name TEXT,
    
	PRIMARY KEY (order_id),
	FOREIGN KEY (name) REFERENCES customers(name)
);

CREATE TABLE cookie_orders (
	cookie TEXT,
	order_id TEXT,
	nbr_pallets INT,

	PRIMARY KEY (cookie, order_id),
	FOREIGN KEY (cookie) REFERENCES cookies(name),
	FOREIGN KEY (order_id) REFERENCES orders(order_id)
);

CREATE TABLE customers (
	name TEXT,
	address TEXT,
    
	PRIMARY KEY (name)
);


-- And re-enable foreign key checks.

PRAGMA foreign_key = on;