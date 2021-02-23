"""Models for Blogly."""

from flask.helpers import get_template_attribute
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEF_IMG_URL = "https://www.freeiconspng.com/uploads/user-group-flat-icon-png-24.png" 

class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=True, default=DEF_IMG_URL)

    posts = db.relationship("Post", backref="user", cascade="all")

    @property
    def full_name(self):
        """retrieve user full name"""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):

    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %#d  %Y, %#I:%M %p")
        ###copied this part, unsure about how the datetime attributes work


def connect_db(app):
    """connect to flask"""
    db.app = app
    db.init_app(app)