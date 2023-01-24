"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy


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




