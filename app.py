"""Blogly application."""

from flask import Flask,request,redirect,render_template,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretsecret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
toolbar = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    db.create_all()


@app.route("/")
def main():
    """home routes to the users list"""
    return redirect('/users')


@app.route("/users")
def show_users():
    """show the user list"""
    users=User.query.order_by(User.first_name,User.last_name).all()
    return render_template('userlist.html',users=users)


@app.route("/users/new",methods=["GET"])    #get and post methods here
def show_new_user_form():
    """show add new user form"""
    return render_template("new-user-form.html")


@app.route("/users/new",methods=["POST"])
def process_new_user_form():
    """process form data and redirect to the userslist"""
    new_user=User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'])#or None)
    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")

@app.route("/users/<int:user_id>")
def show_user_details(user_id):
    user=User.query.get_or_404(user_id)

    return render_template("user-details.html",user=user)


@app.route("/users/<int:user_id>/edit")
def show_edit_form(user_id):
    user=User.query.get_or_404(user_id)
    return render_template("edit-user-form.html",user=user)

@app.route("/users/<int:user_id>/edit",methods=["POST"])
def handle_edits(user_id):
    """handle user information edits"""
    user=User.query.get_or_404(user_id)
    user.first_name=request.form['first_name'],
    user.last_name=request.form['last_name'],
    user.image_url=request.form['image_url']#or None

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")

# this is starting part two of the project

@app.route("/users/<int:user_id>/posts/new", methods=["GET"])
def show_new_post_form(user_id):
    """show the form for new posts for specific user"""
    user=User.query.get_or_404(user_id)
    return render_template("new_post_form.html",user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["GET","POST"])
def process_new_post_Form(user_id):

    user=User.query.get_or_404(user_id)
    new_post=Post(title=request.form['title'],content=request.form['content'],user=user)
       
    db.session.add(new_post)
    db.session.commit()
 

    return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_post_details(post_id):
    """Show a page with info on a specific post"""

    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit',methods=["GET"])
def show_posts_edit_form(post_id):
    """show edit post form """
    post=Post.query.get_or_404(post_id)
    return render_template("edit_post.html",post=post)

@app.route('/posts/<int:post_id>/edit',methods=["POST"])
def handle_post_edits(post_id):
    """handle post  edits"""
    post=Post.query.get_or_404(post_id)
    post.title=request.form['title'],
    post.content=request.form['content']

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete',methods=["POST"])
def delete_post(post_id):
    """handle deleting of specific post"""
    post=Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")
