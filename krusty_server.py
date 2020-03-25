from bottle import get, post, run, request, response, delete, put
import sqlite3
import json

HOST = 'localhost'
PORT = 7007

conn = sqlite3.connect("movies.sqlite")

#-----------HELP FUNCTIONS----------------
def url(resource):
	return "http://{HOST}:{PORT}{resource}"

def format_response(d):
	return json.dumps(d, indent=4) + "\n"

def hash(msg):
    import hashlib
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

#---------------SOLVING THE ASSINGMENTS-----------------------------

@get('/ping')
def get_ping():

    s = {"pong"}
    response.status = 200
    return s

@post('/reset')
def reset():

    c = conn.cursor()
    c.execute(
        """
        DELETE FROM cookies
        """
    )
    c.execute(
        """
        DELETE FROM ingredients
        """
    )
    c.execute(
        """
        DELETE FROM recipes
        """
    )
    c.execute(
        """
        DELETE FROM pallets
        """
    )
    c.execute(
        """
        DELETE FROM orders
        """
    )
    c.execute(
        """
        DELETE FROM cookie_orders
        """
    )
    c.execute(
        """
        DELETE FROM customers
        """
    )
    c.execute(
        """
        INSERT
        INTO   cookies(cookie_name)
        VALUES ('Nut ring'),
               ('Nut cookie'),
               ('Amneris'),
               ('Tango'),
               ('Almond delight'),
               ('Berliner')
        """
    )
    c.execute(
        """
        INSERT
        INTO   ingredients(ingredient_name, quantity, unit)
        VALUES ('Flour', 100 000, g),
               ('Butter', 100 000, g),
               ('Icing sugar', 100 000, g),
               ('Roasted', chopped nuts, 100 000, g),
               ('Fine-ground nuts', 100 000, g),
               ('Ground, roasted nuts', 100 000, g),
               ('Bread crumbs', 100 000, g),
               ('Sugar', 100 000, g),
               ('Egg whites', 100 000, ml),
               ('Chocolate', 100 000, g),
               ('Marzipan', 100 000, g),
               ('Eggs', 100 000, g),
               ('Potato starch', 100 000, g),
               ('Wheat flour', 100 000, g),
               ('Sodium bicarbonate', 100 000, g),
               ('Vanilla', 100 000, g),
               ('Chopped almonds', 100 000, g),
               ('Cinnamon', 100 000, g),
               ('Vanilla sugar', 100 000, g)
        """
    )
    c.execute(
        """
        INSERT
        INTO   recipes(cookie_name, ingredient_name, quantity_needed)
        VALUES ('Nut ring','Flour',450),
               ('Nut ring','Butter',450),
               ('Nut ring','Icing sugar',190),
               ('Nut ring','Roasted',225),
               ('Nut cookie','Fine-ground nuts',750),
               ('Nut cookie','Ground, roasted nuts',625),
               ('Nut cookie','Bread crumbs',125),
               ('Nut cookie','Sugar',375),
               ('Nut cookie','Egg whites',350),
               ('Nut cookie','Chocolate',50),
               ('Amneris','Marzipan',750),
               ('Amneris','Butter',250),
               ('Amneris','Eggs',250),
               ('Amneris','Potato starch',25),
               ('Amneris','Wheat flour',25),
               ('Tango','',),
               ('Tango','Butter',200),
               ('Tango','Sugar',250),
               ('Tango','Flour',300),
               ('Tango','Sodium bicarbonate',4),
               ('Tango','Vanilla',2),
               ('Almond delight','Butter',400),
               ('Almond delight','Sugar',270),
               ('Almond delight','Chopped almonds',279),
               ('Almond delight','Flour',400),
               ('Almond delight','Cinnamon',10),
               ('Berliner','Flour',350),
               ('Berliner','Butter',250),
               ('Berliner','Icing sugar',100),
               ('Berliner','Eggs',50),
               ('Berliner','Vanilla sugar',5),
               ('Berliner','Chocolate',50)
        """
    )
    c.execute(
        """
        INSERT
        INTO   customers(customer_name, customer_address)
        VALUES ('Nut ring'),
               ('Nut cookie'),
               ('Amneris'),
               ('Almond delight'),
               ('Berliner')
        """
    )
    conn.commit()
    c.close()
    s = {'OK'}
    response.status = 200
    return s

@get('/customers')
def customers():
    c = conn.cursor()
    c.execute(
        """
        SELECT name, address
        FROM   customers
        """
    )
    s = [{"name": name, "address": address}
         for (name, address) in c]
    return json.dumps({"data": s}, indent=4)

@get('/ingredients')
def ingredients():
    c = conn.cursor()
    c.execute(
        """
        SELECT ingredient_name, quantity, unit
        FROM   ingredients
        """
    )
    s = [{"name": ingredient_name, "quantity": quantity, "unit": unit}
         for (name, address) in c]
    return json.dumps({"data": s}, indent=4)


run(host=HOST, port=PORT, reloader=True, debug=True)
