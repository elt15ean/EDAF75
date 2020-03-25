-- Delete the tables if they exist.
-- Disable foreign key checks, so the tables can
-- be dropped in arbitrary order.
PRAGMA foreign_keys=OFF;

DROP TABLE IF EXISTS theaters;
DROP TABLE IF EXISTS movies;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS screenings;
DROP TABLE IF EXISTS ticets;

PRAGMA foreign_keys=ON;

-- Create the tables.
CREATE TABLE theaters (
    th_name TEXT,
    capacity INT,
    
    PRIMARY KEY (th_name)
);

CREATE TABLE movies (
    imdb_key TEXT DEFAULT (lower(hex(randomblob(16)))),
    title TEXT,
    year INT,
    running_time TEXT,
    
    PRIMARY KEY (imdb_key)
);

CREATE TABLE customers (
    user_name TEXT,
    full_name TEXT,
    password TEXT,
    
    PRIMARY KEY (user_name)
);

CREATE TABLE screenings (
    th_name TEXT,
    start_time TIME,
    start_date DATE,
	title TEXT,
    imdb_key TEXT,

	FOREIGN KEY (imdb_key) REFERENCES movies(imdb_key),
    FOREIGN KEY (th_name) REFERENCES theaters(th_name)
);

CREATE TABLE ticets (
    t_id TEXT DEFAULT (lower(hex(randomblob(16)))),
    th_name TEXT,
    imdb_key TEXT,
    start_time TIME,
    start_date DATE,
    user_name TEXT,
    
    PRIMARY KEY (t_id),
    
    FOREIGN KEY (th_name) REFERENCES theaters(th_name),
    FOREIGN KEY (imdb_key) REFERENCES movies(imdb_key),
    FOREIGN KEY (user_name) REFERENCES customers(user_name)
);

-- Insert data into the tables.
INSERT
INTO    theaters(th_name, capacity)
VALUES  ('Royal Malmö', 300),
        ('Lund', 150),
        ('Eslöv', 50),
        ('Helsingborg', 200),
        ('Landskrona', 100);

INSERT
INTO    movies(title, year, running_time)
VALUES  ('1917', 2020, '1h58min'),
        ('and then we danced', 2019, '1h52min'),
        ('bombshell - när tystnaden bryts', 2019, '1h49min'),
        ('cats', 2010, '1h50min'),
        ('bad boys for life', 2019, '2h4min');

INSERT
INTO    customers(user_name, full_name, password)
VALUES  ('Simon_kid', 'Simon Andersson','blabla123'),
        ('Jenny_swag', 'Jenny Karlsson','bopbop123'),
        ('Big_Anders', 'Anders Jansson','tratra123'),
        ('lilla_Peter', 'Peter Jönsson', 'ditdit123'),
        ('stora_Jasmin', 'Jasmin Osmanov', 'tritri123');

INSERT
INTO    screenings(title, th_name, start_date, start_time)
VALUES  ('1917', 'Royal Malmö', '2020–02-11', '19:30'),
        ('and then we danced', 'Royal Malmö', '2020–02-21', '20:30'),
        ('1917', 'Royal Malmö', '2020–02-11', '22:30'),
        ('bombshell - när tystnaden bryts', 'Eslöv', '2020–02-13', '19:30'),
        ('bad boys for life', 'Helsingborg', '2020–02-11', '19:30'),
        ('bad boys for life', 'Lund', '2020–02-14', '17:30'),
        ('cats', 'Landskrona', '2020–02-21', '19:30');