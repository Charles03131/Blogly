from unittest import TestCase

from app import app
from flask import session
from models import db, User


app.config['SQLALCHEMY_DATABASE_URI']='postgresql:///testuser'
app.config['SQLALCHEMY_ECHO']=False

app.config['TESTING']=True

app.config['DEBUG_TB_HOSTS']=['dont-show-debug-toolbar']

with app.app_context():
    db.drop_all()
    db.create_all()


class TestUserViews(TestCase):
    """tests for views for Users"""


    def setUp(self):
        #User.query.delete()
        user=User(first_name="TESTRicky",last_name="Bobby",image_url="https://www.dictionary.com/e/wp-content/uploads/2018/03/Ricky-Bobby.jpg")
        with app.app_context(): 
            db.session.add(user)
            db.session.commit()



            self.user_id=user.id

    def tearDown(self):
        """remove any fouled tests"""
        with app.app_context():
            db.session.rollback()


    def test_show_users(self):
        with app.test_client() as client:
            resp=client.get("/users")
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>USERS</h1>',html)


    def test_show_new_user_form(self):
        with app.test_client() as client:
            resp=client.get("users/new")
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn('<h1>Create New User</h1>',html)


    def test_process_new_user_form(self):
        with app.test_client() as client:
            testuser={"first_name":"TESTUSER", "last_name":"TESTUSERLAST",
            "image_url":"https://static.wikia.nocookie.net/stitchipediaalilostitch/images/d/d2/Stitch_%28Lilo_%26_Stitch%29.svg/revision/latest?cb=20210422125647"}

            resp=client.post("users/new",data=testuser,follow_redirects=True)
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn("TESTUSER TESTUSERLAST",html)


    def test_show_user_details(self):
        with app.test_client() as client:
            resp=client.get(f"/users/{self.user_id}")
            html=resp.get_data(as_text=True)

            self.assertEqual(resp.status_code,200)
            self.assertIn("TESTRicky Bobby",html)