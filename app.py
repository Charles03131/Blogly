"""Blogly application."""

from flask import Flask,request,redirect,render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretsecret'

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


@app.route("/users/<int:user_id>/delete", methods={"POST"})
def delete_user(user_id):
    user=User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")