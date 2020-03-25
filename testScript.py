from bottle import route, run

@route('/hello')
def hello():
    return "Hello Edvin! \n I've been waiting for you."

run(host='localhost', port=8080, debug=True)