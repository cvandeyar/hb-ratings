"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/registration')
def registration_form():
    """ register new users """
    return render_template("register.html")

@app.route('/add-user', methods=["POST"])
def add_new_user():
    """ add new users """

    email = request.form.get('email')
    password = request.form.get('password')

    registered_email = User.query.filter(User.email == email)

    if registered_email:
        flash("Email already taken. Please try logging in")
        return redirect('/registration')

    else:
        new_user = User(email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        flash("You have been added. Welcome")
        return redirect('/registration')

@app.route('/login')
def login():
    """ login """

    return render_template("login.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
