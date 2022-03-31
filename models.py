from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""

DEFAULT_IMAGE_URL = 'https://i.imgflip.com/6atbfs.jpg'

class User(db.Model):
    '''Creates users.'''

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    image_url = db.Column(db.String, default = DEFAULT_IMAGE_URL)


