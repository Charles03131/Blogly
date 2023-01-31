"""Blogly application."""

from flask import Flask,request,redirect,render_template,flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post,Tag, PostTag
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


@app.route("/users/new")    #get and post methods here
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
    tags=Tag.query.all()
    return render_template("new_post_form.html",user=user,tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=["GET","POST"])
def process_new_post_Form(user_id):

    user=User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags=Tag.query.filter(Tag.id.in_(tag_ids)).all()
    new_post=Post(title=request.form['title'],content=request.form['content'],user=user,tags=tags)
       
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
    tags=Tag.query.all()
  
    return render_template("edit_post.html",post=post,tags=tags)

@app.route('/posts/<int:post_id>/edit',methods=["POST"])
def handle_post_edits(post_id):
    """process post  edits"""
    post=Post.query.get_or_404(post_id)
    post.title=request.form['title'],
    post.content=request.form['content']
    
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

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

#this is the begining of part 3 of project



@app.route('/tags')
def show_tags_list():
    tags=Tag.query.all()
    return render_template("tagslist.html",tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag_detail(tag_id):
    """Show a page with info on a specific tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)



@app.route('/tags/new',methods=['GET'])
def show_tag_form():
    posts=Post.query.all()
    return render_template("tag_form.html",posts=posts)



@app.route("/tags/new",methods=["POST"])
def process_tag_form():
    """process form data and redirect to the tagslist"""
    new_tag=Tag(
          name=request.form['name'])
        
    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')




@app.route("/tags/<int:tag_id>/edit",methods=["GET"])
def show_edit_tag_form(tag_id):
    tag=Tag.query.get_or_404(tag_id)

    return render_template("edit_tag_form.html",tag=tag)




@app.route("/tags/<int:tag_id>/edit",methods=["POST"])
def handle_tag_edits(tag_id):
    """handle user information edits"""
    tag=Tag.query.get_or_404(tag_id)
    tag.name=request.form['name']

    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')



@app.route("/tags/<int:tag_id>/delete",methods=["POST"])
def delete_tag(tag_id):
    tag=Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect('/tags')