"""I would love a rundown about testing my post requests, as I am still unsure how to test the other pages; maybe I am overthinking it. I relied heavily on the lesson videos for figuring out the testing."""

            

from unittest import TestCase

from app import app
from models import db, User


app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:///blogly"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['TESTING'] = True


app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
    "Tests for views of Users."

    def setUp(self):
        
        User.query.delete()

        user = User(first_name="New", last_name="User", image_url=None)
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New', html)

    def test_list_users_new(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('New', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>New</h1>', html)
            self.assertIn(self.user.first_name, html)
    
