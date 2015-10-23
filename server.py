"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route("/movies")
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by("title").all()

    return render_template("movie_list.html", movies=movies)


@app.route("/movies/<int:movie_id>", methods=['GET'])
def movie_rating(movie_id):
    """Show list of ratings by movie."""
    movie = Movie.query.get(movie_id)


    #####TODO need a page that shows movie info and ratings. 
    #####Route is not taking us to template
    ratings = Rating.query.get(movie_id)

    return render_template("ratings_list.html", movie=movie)


@app.route("/users/<int:user_id>")
def user_ratings(user_id):
    """Show list of movies a user has rated."""

    user = User.query.get(user_id)

    return render_template("user_page.html", user=user,)


@app.route("/login")
def log_in():
    """Show user login."""


    return render_template("login.html")


@app.route("/submit", methods=["POST"])
def submit():
    """Show user login."""
    email = request.form["email"]
    password = request.form["password"]

    user = User.query.filter(User.email==email).first()

    if user:
        #if the password is correct
        if user.password == password:
            flash('You were successfully logged in')

            session["userid"] = user.user_id
            return redirect("/users/%s" % user.user_id)
        else:
            flash('Your password is incorrect')
            return redirect("/login")
            #show user a message that their password is incorrect
    # email not in db, add email and password to db
    else:
        user = User(email=email, password=password)
        flash('Your account was created!')
        db.session.add(user)
        db.session.commit()
        return redirect("/")


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('userid', None)
    flash('You were successfully logged out!')
    return redirect('/')


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

