from bottle import get, post, run, request, response, delete, put
import sqlite3
import json

HOST = 'localhost'
PORT = 8888

conn = sqlite3.connect("krustyDB.sqlite")

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
        VALUES ('Flour', 100000, 'g'),
               ('Butter', 100000, 'g'),
               ('Icing sugar', 100000, 'g'),
               ('Roasted, chopped nuts', 100000, 'g'),
               ('Fine-ground nuts', 100000, 'g'),
               ('Ground, roasted nuts', 100000, 'g'),
               ('Bread crumbs', 100000, 'g'),
               ('Sugar', 100000, 'g'),
               ('Egg whites', 100000, 'ml'),
               ('Chocolate', 100000, 'g'),
               ('Marzipan', 100000, 'g'),
               ('Eggs', 100000, 'g'),
               ('Potato starch', 100000, 'g'),
               ('Wheat flour', 100000, 'g'),
               ('Sodium bicarbonate', 100000, 'g'),
               ('Vanilla', 100000, 'g'),
               ('Chopped almonds', 100000, 'g'),
               ('Cinnamon', 100000, 'g'),
               ('Vanilla sugar', 100000, 'g')
        """
    )
    c.execute(
        """
        INSERT
        INTO   recipes(cookie_name, ingredient_name, quantity_needed)
        VALUES ('Nut ring','Flour',450),
               ('Nut ring','Butter',450),
               ('Nut ring','Icing sugar',190),
               ('Nut ring','Roasted, chopped nuts',225),
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
        VALUES ('Finkakor AB', 'Helsingborg'),
               ('Smabrod AB', 'Malmo'),
               ('Kaffebrod AB', 'Landskrona'),
               ('Bjudkakor AB', 'Ystad'),
               ('Kalaskakor AB', 'Trelleborg'),
               ('Partykakor AB', 'Kristianstad'),
               ('Gastkakor AB', 'Hassleholm'),
               ('Skanekakor AB', 'Perstorp')
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
        SELECT customer_name, customer_address
        FROM   customers
	ORDER BY customer_name
        """
    )
    s = [{"customer_name": name, "customer_address": address}
         for (name, address) in c]
    return json.dumps({"customers": s}, indent=4)

@get('/ingredients')
def ingredients():
    c = conn.cursor()
    c.execute(
        """
        SELECT ingredient_name, quantity, unit
        FROM   ingredients
	ORDER BY ingredient_name
        """
    )
    s = [{"ingredient_name": ingredient_name, "quantity": quantity, "unit": unit}
         for (ingredient_name, quantity, unit) in c]
    return json.dumps({"ingredients": s}, indent=4)

@get('/cookies')
def cookies():
    c = conn.cursor()
    c.execute(
        """
        SELECT cookie_name
        FROM   cookies
	ORDER BY cookie_name
        """
    )
    s = [{"name": cookie_name}
         for (cookie_name) in c]
    return json.dumps({"cookies": s}, indent=4)

@get('/recipes')
def recipes():
    c = conn.cursor()
    c.execute(
        """
        SELECT cookie_name, ingredient_name, quantity_needed, unit
        FROM   recipes
	JOIN ingredients
	USING (ingredient_name)
	ORDER BY cookie_name, ingredient_name
        """
    )
    s = [{"cookie": cookie_name, "ingredient": ingredient_name,"quantity": quantity_needed,"unit": unit}
         for (cookie_name, ingredient_name, quantity_needed, unit) in c]
    return json.dumps({"recipes": s}, indent=4)

@get('/pallets')
def get_pallets():
    c = conn.cursor()
    c.execute(
        """
        SELECT pallet_id, cookie_name, produced, customer_name, blocked
        FROM   pallets
        """
    )
    s = [{"id":pallet_id, "cookie":cookie_name,"productionDate":produced,"customer":customer_name,"blocked":blocked}
        for(pallet_id, cookie_name, produced, customer_name, blocked) in c]
    return json.dumps({"pallets": s}, indent=4)

@post('/pallets/<current_cookie>')
def post_pallets(current_cookie):
    c = conn.cursor()


    cookieList = c.execute(
    """
    SELECT cookie_name
    FROM cookies
    WHERE cookie_name = ?
    """
    ,
    [current_cookie]
    ).fetchall()
    print(type(cookieList))

    if len(cookieList) == 0:
        s = {"status": "no such cookie"}
        c.close()
        response.status = 200
        return json.dumps({"data": s}, indent=4)
    else:
        c.execute(
        """
        INSERT
        INTO pallets (cookie_name)
        VALUES (?)
        """
        ,
        [current_cookie]
        )
        conn.commit()
        s = [{"status": "ok", "id":"123"}]
        c.close()
        response.status = 200
        return json.dumps({"data": s}, indent=4)

run(host=HOST, port=PORT, reloader=True, debug=True)