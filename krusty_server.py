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
