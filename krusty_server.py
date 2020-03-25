from bottle import get, post, run, request, response, delete, put
import sqlite3
import json

HOST = 'localhost'
PORT = 7007

conn = sqlite3.connect("movies.sqlite")

#-----------HELP FUNCTIONS----------------
def url(resource):
    return f"http://{HOST}:{PORT}{resource}"

def format_response(d):
    return json.dumps(d, indent=4) + "\n"

def hash(msg):
    import hashlib
    return hashlib.sha256(msg.encode('utf-8')).hexdigest()

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
    conn.commit()
    c.close()
    s = {'OK'}
    response.status = 200
    return s