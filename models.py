from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


"""Models for Blogly."""

DEFAULT_IMAGE_URL = 'https://i.imgflip.com/6atbfs.jpg'

class User(db.Model):
    """Adds user to database."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(30), nullable = False)
    last_name = db.Column(db.String(30), nullable = False)
    image_url = db.Column(db.String, default = DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref = "user")



class Post(db.Model):
    """Add post to database and references users table."""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.String, nullable = False)
    created_at = db.Column(db.DateTime,
    nullable = False, default= db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

