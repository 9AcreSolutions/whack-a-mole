import os, flask

from flask import Flask, render_template, redirect, url_for, request, session, flash
from functools import wraps
import sqlite3

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.SECRET_KEY = "my precious"
    app.database = "sample.db"

    # login required decorator
    def login_required(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if 'logged_in' in session:
                return f(*args, **kwargs)
            else:
                flash('You need to login first.')
                return redirect(url_for('login'))
        return wrap

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route('/hello')
    @login_required
    def hello():
        return render_template('home.html')

    @app.route('/')
    @login_required
    def home():
        return render_template('index-START.html')
    if __name__ == '__main__':
        app.run()

    # Route for handling the login page logic
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            if request.form['username'] != 'admin' or request.form['password'] != 'admin':
                error = 'Invalid Credentials. Please try again.'
            else:
                session['logged_in'] = True
                flash('You were just logged in!')
                return redirect(url_for('home'))
        return render_template('login.html', error=error)

    @app.route('/logout')
    @login_required
    def logout():
        session.pop('logged_in', None)
        flash('You were just logged out !')
        return redirect(url_for('hello'))

    def connect_db():
        return sqlite3.connect(app.database)

    return app

app = create_app()

#
# # # start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
