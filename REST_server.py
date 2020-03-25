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
        DELETE FROM movies
        """
    )
    c.execute(
        """
        DELETE FROM theaters
        """
    )
    c.execute(
        """
        DELETE FROM customers
        """
    )
    c.execute(
        """
        DELETE FROM screenings
        """
    )
    c.execute(
        """
        DELETE FROM ticets
        """
    )    
    c.execute(
        """
        INSERT
        INTO   movies(title, year, imdb_key)
        VALUES ('The Shape of Water', 2017, 'tt5580390'),
               ('Moonlight', 2016, 'tt4975722'),
               ('Spotlight', 2015, 'tt1895587'),
               ('Birdman', 2014, 'tt2562232')
        """
    )
    c.execute(
        """
        INSERT
        INTO   theaters(th_name, capacity)
        VALUES ('Sodran', 16),
               ('Kino', 10),
               ('Skandia', 100)
        """
    )
    password1 = hash('dobido')
    password2 = hash('whatsinaname')
    c.execute(
        """
        INSERT
        INTO   customers(user_name, full_name, password)
        VALUES ('alice', 'Alice', ?),
               ('bob', 'Bob', ?)
        """
        ,
        [password1, password2]
    )
    conn.commit()
    c.close()
    s = {'OK'}
    response.status = 200
    return s


@get('/movies')
def get_movies():
    c = conn.cursor()
    c.execute(
        """
        SELECT imdb_key, title, year
        FROM   movies
        """
    )
    s = [{"imdb_key": imdb_key, "title": title, "year": year}
         for (imdb_key, title, year) in c]
    return json.dumps({"data": s}, indent=4)


@get('/movies/<title>/<year>')
def get_movies(title,year):

    c = conn.cursor()
    c.execute(
        """
        SELECT imdb_key, title, year
        FROM   movies
        WHERE   title = ? AND year = ?
        """
        ,
        [title,year]
    )
    s = [{"imdb_key": imdb_key, "title": title, "year": year}
         for (imdb_key, title, year) in c]
    c.close()
    return json.dumps({"data": s}, indent=4)

    
@get('/movies/<imdb_key>')
def get_movies(imdb_key):

    c = conn.cursor()
    c.execute(
        """
        SELECT imdb_key, title, year
        FROM   movies
        WHERE   imdb_key = ?
        """
        ,
        [imdb_key]
    )
    s = [{"imdb_key": imdb_key, "title": title, "year": year}
         for (imdb_key, title, year) in c]
    c.close()
    return json.dumps({"data": s}, indent=4)


@post('/performances/<imdb_key>/<th_name>/<start_date>/<start_time>')
def post_screenings(imdb_key,th_name,start_date,start_time):
    c = conn.cursor()
    
    movies = c.execute(
        """
        SELECT imdb_key
        FROM   movies
        """
    ).fetchall()
    print(type (movies))
    count = 0;
    
    for i in range(0,len(movies)):
        
        comp = ' '.join(movies[i]);
        
        if(imdb_key == comp):
        
            count = count + 1;
    
    
    theaters = c.execute(
        """
        SELECT th_name
        FROM   theaters
        """
    ).fetchall()
    
    for i in range(0,len(theaters)):
    
        comp = ' '.join(theaters[i]);
        
        if(th_name == comp):
        
            count = count + 1;
    
    
    if(count == 2):
        c.execute(
            """
            INSERT
            INTO   screenings(imdb_key,th_name,start_date,start_time)
            VALUES (?, ?, ?, ?)
            """
            ,
            [imdb_key,th_name,start_date,start_time]
        )
        conn.commit()
        c.execute(
            """
            SELECT  scr_id
            FROM    screenings
            WHERE   rowid = last_insert_rowid()
            """
        )
        id = c.fetchone()[0]
        c.close()
        s = format_response({"scr_id": id, "url": url(f"/screenings/{id}")})
        response.status = 200
    else:
        c.close()
        s = {"No such movie or theater"}
    return s


@get('/performances')
def get_performances():
    c = conn.cursor()
    c.execute(
        """
        WITH temp_screenings as
            (SELECT scr_id, start_date, start_time, title, year, th_name, capacity
            FROM screenings
            JOIN    movies
            USING (imdb_key)
            JOIN theaters
            USING (th_name)
            )
        SELECT scr_id, start_date, start_time, title, year, th_name, capacity - count(t_id) AS re
        FROM  temp_screenings
        LEFT JOIN ticets
        USING (scr_id)
        GROUP BY (scr_id)
        """
    )
    
    s = [{"screening_id": scr_id, "start_date": start_date, "start_time": start_time, "title": title, "year": year, "theater": th_name, "Remaining seats": re}
         for (scr_id, start_date, start_time, title, year, th_name, re) in c]
    
    return json.dumps({"data": s}, indent=4)


@post('/ticets/<user_name>/<scr_id>/<password>')
def post_ticets(user_name,scr_id,password):
    c = conn.cursor()
    
    password_attempt = hash(password)
    try:
        trying_password = c.execute(
            """
            SELECT user_name
            FROM  customers
            WHERE password = ?
            """
            ,
            [password_attempt]
        ).fetchone()[0]
    except:
        s = {"Error"}
        return s
    
    try:
        nbr_seats = c.execute(
            """
            WITH temp_screenings as
                (SELECT scr_id, start_date, start_time, title, year, th_name, capacity
                FROM screenings
                JOIN    movies
                USING (imdb_key)
                JOIN theaters
                USING (th_name)
                )
            SELECT capacity - count(t_id) AS nbr_seats
            FROM  temp_screenings
            LEFT JOIN ticets
            USING (scr_id)
            GROUP BY (scr_id)
            HAVING scr_id = ?
            """
            ,
            [scr_id]
        ).fetchone()[0]
    except:
        s = {"Error"}
        return s
    
    try:
        trying_name = c.execute(
            """
            SELECT user_name
            FROM  customers
            WHERE user_name = ?
            """
            ,
            [user_name]
        ).fetchone()[0]
    except:
        s = {"Error"}
        return s
    
    
    if(nbr_seats > 0):
        c.execute(
            """
            INSERT
            INTO   ticets(user_name, scr_id)
            VALUES (?, ?)
            """
            ,
            [user_name, scr_id]
        )
        conn.commit()
        c.execute(
            """
            SELECT  t_id
            FROM    ticets
            WHERE   rowid = last_insert_rowid()
            """
        )
        id = c.fetchone()[0]
        c.close()
        s = format_response({"t_id": id, "url": url(f"/screenings/{id}")})
        response.status = 200
    elif(nbr_seats <= 0):
        c.close()
        s = {"No ticets left"}
    else:
        c.close()
        s = {"Error"}
    return s


@get('/customers/<user_name>/ticets')
def get_customer_ticets(user_name):
    c = conn.cursor()
    try:
        c.execute(
            """
            SELECT start_date, start_time, th_name, title, year, count(t_id) AS nbr_of_ticets
            FROM ticets
            JOIN screenings
            USING (scr_id)
            JOIN movies
            USING (imdb_key)
            JOIN theaters
            USING (th_name)
            GROUP BY (scr_id)
            HAVING user_name = ?
            """
            ,
            [user_name]
        )
        s = [{"start_date": start_date, "start_time": start_time, "theater": th_name, "title": title, "year": year, "nbr_of_ticets": nbr_of_ticets}
            for (start_date, start_time, th_name, title, year, nbr_of_ticets) in c]        
        response.status = 200
        return json.dumps({"data": s}, indent=4)
    except:
        c.close()
        s = {"Error"}
        return s

  


#---------LOOKING UP TABLES-----------------
@get('/theaters')
def get_theaters():
    c = conn.cursor()
    c.execute(
        """
        SELECT th_name, capacity
        FROM   theaters
        """
    )
    s = [{"th_name": th_name, "capacity": capacity}
         for (th_name, capacity) in c]
    return json.dumps({"data": s}, indent=4)

@get('/customers')
def get_customers():
    c = conn.cursor()
    c.execute(
        """
        SELECT *
        FROM   customers
        """
    )
    s = [{"user_name": user_name, "full_name": full_name, "password": password}
         for (user_name, full_name, password) in c]
    return json.dumps({"data": s}, indent=4)

@get('/screenings')
def get_screenings():
    c = conn.cursor()
    c.execute(
        """
        SELECT scr_id, start_date, start_time, title, year, th_name, capacity
        FROM screenings
        JOIN    movies
        USING (imdb_key)
        JOIN theaters
        USING (th_name)
        """
    )
    
    s = [{"screening_id": scr_id, "start_date": start_date, "start_time": start_time, "title": title, "year": year, "theater": th_name}
         for (scr_id, start_date, start_time, title, year, th_name, capacity) in c]
    
    return json.dumps({"data": s}, indent=4)


@get('/ticets')
def get_ticets():
    c = conn.cursor()
    c.execute(
        """
        SELECT t_id, scr_id, user_name
        FROM   ticets
        """
    )
    s = [{"t_id": t_id, "scr_id": scr_id, "user_name": user_name}
         for (t_id, scr_id, user_name) in c]
    
    return json.dumps({"data": s}, indent=4)




#----------------RUNNING SERVER--------------------
run(host=HOST, port=PORT, reloader=True, debug=True)