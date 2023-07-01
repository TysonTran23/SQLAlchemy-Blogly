"""Blogly application."""
from flask import Flask, flash, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension

from models import Post, User, connect_db, db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "chickenzarecool21837"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def users():
    return redirect("/users")


@app.route("/users")
def all_users():
    users = User.query.all()
    return render_template("home.html", users=users)


@app.route("/users/new")
def add_user_page():
    return render_template("newuser.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    first_name = request.form["first"]
    last_name = request.form["last"]
    img = request.form["image"]

    new_user = User(first_name=first_name, last_name=last_name, image_url=img)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edituser.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def save_user(user_id):
    user = User.query.get_or_404(user_id)

    first_name = request.form["first"]
    last_name = request.form["last"]
    img = request.form["image"]

    user.first_name = first_name
    user.last_name = last_name
    user.image_url = img

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def post_form(user_id):
    users = User.query.get_or_404(user_id)

    return render_template("newpost.html", users=users)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    title = request.form["title"]
    content = request.form["content"]

    post = Post(title=title, content=content)
    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")
