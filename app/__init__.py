import os
from flask import Flask, render_template, jsonify, request
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from app.db import get_db

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(os.getcwd(),'flask.sqlite')
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html', title="Portfolio", url=os.getenv("URL"))

@app.route('/athena')
def athena():
    return render_template('athena.html', name="Athena")

@app.route('/patrick')
def patrick():
    return render_template('patrick.html', name ="Patrick")

@app.route('/juancarlos')
def juancarlos():
    return render_template('juancarlos.html', name="Juan Carlos")

@app.route('/health', methods=[ 'GET' ])
def health():
    return jsonify(status=200)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = f"User {username} is already registered."

        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return f"User {username} created successfully\n"
        else:
            return error, 418

    ## TODO: Return a restister page
    return "Register Page not yet implemented", 501

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            return "Login Successful\n", 200 
        else:
            return error, 418
    
    ## TODO: Return a login page
    return "Login Page not yet implemented", 501
