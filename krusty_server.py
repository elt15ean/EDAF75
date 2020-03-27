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
        INTO   cookies(cookie)
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
        INTO   ingredients(ingredient, quantity, unit)
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
               ('Marzipan',100000, 'g'),
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
        INTO   recipes(cookie, ingredient, quantity_needed)
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
        INTO   customers(customer, customer_address)
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
        SELECT customer, customer_address
        FROM   customers
	ORDER BY customer_name
        """
    )
    s = [{"customer": name, "customer_address": address}
         for (name, address) in c]
    return json.dumps({"customers": s}, indent=4)

@get('/ingredients')
def ingredients():
    c = conn.cursor()
    c.execute(
        """
        SELECT ingredient, quantity, unit
        FROM   ingredients
	ORDER BY ingredient
        """
    )
    s = [{"ingredient": ingredient_name, "quantity": quantity, "unit": unit}
         for (ingredient, quantity, unit) in c]
    return json.dumps({"ingredients": s}, indent=4)

@get('/cookies')
def cookies():
    c = conn.cursor()
    c.execute(
        """
        SELECT cookie
        FROM   cookies
	ORDER BY cookie
        """
    )
    s = [{"name": cookie}
         for (cookie) in c]
    return json.dumps({"cookies": s}, indent=4)

@get('/recipes')
def recipes():
    c = conn.cursor()
    c.execute(
        """
        SELECT cookie, ingredient, quantity_needed, unit
        FROM   recipes
	JOIN ingredients
	USING (ingredient)
	ORDER BY cookie, ingredient
        """
    )
    s = [{"cookie": cookie, "ingredient": ingredient,"quantity": quantity_needed,"unit": unit}
         for (cookie, ingredient, quantity_needed, unit) in c]
    return json.dumps({"recipes": s}, indent=4)

@get('/pallets')
def get_pallets():
    response.content_type= 'application/json'
    query = """
    SELECT pallet_id, cookie, produced, customer, blocked
    FROM pallets
    WHERE 1 = 1
    """
    params = []
    if request.query.cookie_name:
        query += "AND cookie_name = ?"
        params.append(request.query.cookie)
    if request.query.blocked:
        query += "AND blocked = ?"
        params.append(request.query.blocked)
    if request.query.after:
        query += "AND produced > ?"
        params.append(request.query.after)
    if request.query.before:
        query += "AND produced < ?"
        params.append(request.query.before)
    c = conn.cursor()
    c.execute(
    query,
    params
    )
    s = [{"id":pallet_id, "cookie":cookie,"productionDate":produced,"customer":customer,"blocked":blocked}
        for(pallet_id, cookie, produced, customer, blocked) in c]
    response.status = 200
    return json.dumps({"pallets": s}, indent=4)

@post('/pallets')
def post_pallets():
    response.content_type= 'application/json'
    cookie = request.query.cookie
    c = conn.cursor()
    cookieList = c.execute(
    """
    SELECT cookie
    FROM cookies
    WHERE cookie = ?
    """
    ,
    [cookie]
    ).fetchall()
    print(type(cookieList))

    if len(cookieList) == 0:
        s = {"status": "no such cookie"}
        c.close()
        response.status = 400
        return json.dumps({"data": s}, indent=4)
    else:
        try:
            c.execute(
            """
            WITH ingredients_needed AS(
                SELECT ingredient
                FROM recipes
                WHERE cookie = ?
            )
            UPDATE ingredients
            SET quantity = quantity - (SELECT quantity_needed
            FROM recipes
            WHERE cookie = ?
                AND ingredients.ingredient = recipes.ingredient)
            WHERE ingredient IN ingredients_needed
            """
            ,
            [cookie, cookie]
            )
        except:
            s = {"status": "not enough ingredients"}
            c.close()
            response.status = 400
            return json.dumps({"data": s}, indent=4)
        c.execute(
        """
        INSERT
        INTO pallets (cookie)
        VALUES (?)
        """
        ,
        [cookie]
        )
        conn.commit()
        s = [{"status": "ok", "id":"123"}]
        c.close()
        response.status = 200
        return json.dumps({"data": s}, indent=4)

run(host=HOST, port=PORT, reloader=True, debug=True)