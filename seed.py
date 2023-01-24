"""seed file to make user data"""


from models import User,db,connect_db
from app import app

with app.app_context():
    db.drop_all()
    db.create_all()


    User.query.delete()


Spongebob=User(first_name="Sponge",last_name="Bob",image_url="https://i.pinimg.com/originals/44/c9/9c/44c99c3c1ada52473c392b397594ff1c.jpg")
Burt=User(first_name="Burt",last_name="Cobb",image_url="https://i.pinimg.com/originals/d4/73/2a/d4732a112320f72ccff48bccca1d5bcf.jpg")
Reginald=User(first_name="Reginald",last_name="Calvin",image_url="https://as2.ftcdn.net/v2/jpg/02/08/43/55/1000_F_208435521_EI6t7FKQfzOu4dwoKOZ0nnDliY2yX2kb.jpg")


with app.app_context():
    db.session.add(Spongebob)
    db.session.add(Burt)
    db.session.add(Reginald)
    db.session.commit()