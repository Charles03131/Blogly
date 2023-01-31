"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
import datetime


db=SQLAlchemy()
    
def connect_db(app):
    with app.app_context():
        db.app = app
        db.init_app(app)



class User(db.Model):
    """site User"""
    __tablename__="users"

    id=db.Column(db.Integer, primary_key=True)
    first_name=db.Column(db.Text, nullable=False)
    last_name=db.Column(db.Text, nullable=False)
    image_url=db.Column(db.Text, nullable=False)


    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


class Post(db.Model):
    """blog post"""
    __tablename__="posts"

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.Text,nullable=False)
    content=db.Column(db.Text,nullable=False)
    created_at=db.Column(db.DateTime,nullable=False, default=datetime.datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



class PostTag(db.Model):
    """shows the tags on a post"""
    __tablename__="post_tags"
    post_id=db.Column(db.Integer, db.ForeignKey('posts.id'),primary_key=True)
    tag_id=db.Column(db.Integer, db.ForeignKey('tags.id'),primary_key=True)


class Tag(db.Model):
    """ tags that can be added to posts"""
    __tablename__="tags"
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.Text,nullable=False,unique=True)
    posts = db.relationship(
            'Post',
            secondary="post_tags",
            cascade="all,delete",
            backref="tags",
        )