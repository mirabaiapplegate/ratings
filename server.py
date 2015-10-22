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

@app.route("/login")
def log_in():
    """Show user login."""


    return render_template("login.html")


@app.route("/submit", methods=["POST"])
def submit():
    """Show user login."""
    email = request.form["email"]
    password = request.form["password"]

    # We need to check db to see if email and password exist, otherwise add it to db

    user = User.query.filter(User.email==email).first()
    #if the email is in the db
    if user.email == email:
        #if the password is correct
        if user.password == password:
            flash('You were successfully logged in')
            # XXX PUT USEER ID IN SESSION    session["userid"]
            return redirect("/")
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

@app.route("/logout")
def log_out():
    """Show user logout."""

    # user = User.query(User.email==email).first()
    # db.session.delete(user)
    flash('You were successfully logged out!')
    return redirect("/")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()