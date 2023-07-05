"""Blogly application."""
from flask import Flask, flash, redirect, render_template, request, session
from flask_debugtoolbar import DebugToolbarExtension

from models import Post, User, connect_db, db, PostTag, Tag

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
    tags = Tag.query.all()

    return render_template("newpost.html", users=users, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_new_post(user_id):
    title = request.form["title"]
    content = request.form["content"]
    tags = request.form.getlist('tags')

    post = Post(title=title, content=content, user_id=user_id)

    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag:
            post.tags.append(tag)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)

    return render_template("post.html", post=post)

@app.route("/posts/<int:post_id>/edit")
def edit_form(post_id):
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
 
    post = Post.query.get_or_404(post_id)
    title = request.form['title']
    content = request.form['content']
    tags = request.form.getlist('tags')

    post.title = title
    post.content = content
    post.tags = []

    for tag_name in tags:
        tag = Tag.query.filter_by(name=tag_name).first()
        if tag:
            post.tags.append(tag)

    db.session.add(post)
    db.session.commit()


    return redirect(f"/posts/{post.id}")
    
@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users")

@app.route("/tags")
def list_tags():
    
    all_tags = Tag.query.all()

    return render_template('tags.html', tags=all_tags)

@app.route("/tags/<int:tag_id>")
def show_detail_of_tag(tag_id):
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag_details.html', tag=tag)

@app.route("/tags/new")
def new_tag_form():
    posts = Post.query.all()
    return render_template("newtag.html", posts=posts)

@app.route("/tags/new", methods=["POST"])
def new_tag():
    tag_name = request.form['name']
    post_ids = request.form.getlist('posts')


    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()


    for post_id in post_ids:
        post = Post.query.get(post_id)
        if post:
            new_tag.posts.append(post)

    db.session.commit()    

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    tag = Tag.query.get(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    tag = Tag.query.get(tag_id)
    tag_name = request.form['name']

    tag.name = tag_name

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def delete_tag(tag_id):
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')





