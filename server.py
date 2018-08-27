"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db

from sqlalchemy.sql import func


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


@app.route('/movie-list')
def movie_list():
    """show list of movies."""

    movies = Movie.query.order_by(Movie.title).all()
    return render_template("movie_list.html", movies=movies)


@app.route('/registration')
def registration_form():
    """ register new users """
    return render_template("register.html")

@app.route('/add-user', methods=["POST"])
def add_new_user():
    """ add new users """

    email = request.form.get('email')
    password = request.form.get('password')

    registered_email = User.query.filter(User.email == email).first()
    print(registered_email)

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

@app.route('/verifylogin')
def verifylogin():
    email = request.args.get('email')
    password = request.args.get('password')

    User_object = User.query.filter(User.email == email).first()

    if User_object:
        if User_object.password == password:
            session['userid'] = email
            flash("login successful")
            return redirect('/')

        else:
            flash("Password is incorrect. Please try again")
            return redirect('/login')

    else:
        flash("Login does not exist. Please create account")
        return redirect('/registration')

@app.route('/logout')
def logout():
    if session.get('userid'):
        session['userid'] = ""
        return redirect('/')

# /user_page/923

@app.route('/user_page')
def user_page():
    """user page"""

    personid = request.args.get('person')
    person = User.query.get(personid)

    return render_template('user_page.html', person=person)

@app.route('/movie_page')
def movie_page():
    """movie page"""

    movieid = request.args.get('movie')
    movieinfo = Movie.query.get(movieid)
    avgrating = round(db.session.query(func.avg(Rating.score)).filter(Rating.movie_id==movieid).first()[0],1)

    return render_template('movie_page.html', movieinfo=movieinfo, avgrating=avgrating)

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
