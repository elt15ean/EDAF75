from bottle import get, post, run, request, response, delete, put
import sqlite3
import json

HOST = 'localhost'
PORT = 8888

conn = sqlite3.connect("krustyDB.sqlite")

#---------------SOLVING THE ASSINGMENTS-----------------------------

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
        INTO   cookies(name)
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
        INTO   ingredients(name, quantity_in_stock, unit)
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
        INTO   recipes(cookie, ingredient, quantity)
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
        INTO   customers(name, address)
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
    response.status = 200
    return json.dumps({"status": "ok"}, indent=4)

@get('/customers')
def customers():
    c = conn.cursor()
    c.execute(
        """
        SELECT name, address
        FROM   customers
	ORDER BY name
        """
    )
    s = [{"name": name, "address": address}
         for (name, address,) in c]
    return json.dumps({"customers": s}, indent=4)

@get('/ingredients')
def ingredients():
    c = conn.cursor()
    c.execute(
        """
        SELECT name, quantity_in_stock, unit
        FROM   ingredients
	ORDER BY name
        """
    )
    s = [{"name": name, "quantity": quantity_in_stock, "unit": unit}
         for (name, quantity_in_stock, unit,) in c]
    return json.dumps({"ingredients": s}, indent=4)

@get('/cookies')
def cookies():
    c = conn.cursor()
    lista = c.execute(
        """
        SELECT name
        FROM   cookies
	ORDER BY name
        """
    )

    s = [{"name": name}
         for (name,) in c]
    return json.dumps({"cookies": s}, indent=4)

@get('/recipes')
def recipes():
    c = conn.cursor()
    c.execute(
        """
        SELECT cookie, recipes.ingredient, quantity, unit
        FROM   recipes
	JOIN ingredients
	ON ingredients.name = recipes.ingredient
	ORDER BY cookie, recipes.ingredient
        """
    )
    s = [{"cookie": cookie, "ingredient": recipes.ingredient,"quantity": quantity,"unit": unit}
         for (cookie, recipes.ingredient, quantity, unit,) in c]
    return json.dumps({"recipes": s}, indent=4)

@get('/pallets')
def get_pallets():
    response.content_type= 'application/json'
    query = """
    SELECT pallet_id, cookie, produced, name, blocked
    FROM pallets
    LEFT JOIN orders
    USING (order_id)
    WHERE 1 = 1
    """
    params = []
    if request.query.cookie:
        query += "AND cookie = ?"
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
    s = [{"id":pallet_id, "cookie":cookie,"productionDate":produced,"customer":name,"blocked":blocked}
        for(pallet_id, cookie, produced, name, blocked,) in c]
    response.status = 200
    return json.dumps({"pallets": s}, indent=4)

@post('/pallets')
def post_pallets():
    response.content_type= 'application/json'
    cookie = request.query.cookie
    c = conn.cursor()
    cookieList = c.execute(
    """
    SELECT name
    FROM cookies
    WHERE name = ?
    """
    ,
    [cookie]
    ).fetchall()

    if len(cookieList) == 0:
        s = {"status": "no such cookie"}
        c.close()
        response.status = 400
        return json.dumps(s, indent=4)
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
            SET quantity_in_stock = quantity_in_stock - 54*(SELECT quantity
                FROM recipes
                WHERE cookie = ?
                AND ingredients.name = recipes.ingredient)
            WHERE name IN ingredients_needed
            """
            ,
            [cookie, cookie]
            )
        except:
            s = {"status": "not enough ingredients"}
            c.close()
            response.status = 400
            return json.dumps(s, indent=4)
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
        c.execute(
        """
        SELECT pallet_id
        FROM pallets
        WHERE rowid = last_insert_rowid()
        """
        )
        id = c.fetchone()[0]
        s = {"status": "ok", "id": id}
        c.close()
        response.status = 200
        return json.dumps(s, indent=4)


@post('/block/<cookie>/<from_date>/<to_date>')
def block(cookie, from_date, to_date):
	c = conn.cursor()
	c.execute(
	"""
	UPDATE pallets
	SET blocked = 1
	WHERE cookie = ?
		AND produced >= ?
			AND produced <= ?
	"""
	,
	[cookie, from_date, to_date]
	)
	s = [{"status": "ok"}]
	c.close()
	response.status = 200
	return json.dumps({"status": "ok"}, indent=4)


@post('/unblock/<cookie>/<from_date>/<to_date>')
def unblock(cookie, from_date, to_date):
	c = conn.cursor()
	c.execute(
	"""
	UPDATE pallets
	SET blocked = 0
	WHERE cookie = ?
		AND produced >= ?
			AND produced <= ?
	"""
	,
	[cookie, from_date, to_date]
	)
	s = [{"status": "ok"}]
	c.close()
	response.status = 200
	return json.dumps({"status": "ok"}, indent=4)

run(host=HOST, port=PORT, reloader=True, debug=True)