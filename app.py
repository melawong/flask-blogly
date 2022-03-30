"""Blogly application."""

from flask import Flask, redirect, render_template, request
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True



connect_db(app)
db.create_all()

# GET /
# Redirect to list of users. (We’ll fix this in a later step).

@app.get("/")
def get_home_page():
    """Return homepage"""
    return redirect ("/users")

## GET /users
## Show all users.

# Make these links to view the detail page for the user.
## Have a link here to the add-user form.

@app.get("/users")
def get_users():
    """Retrieves all users in the db and renders template wth user list"""
    userlist = User.query.all()

    return render_template("home.html", users = userlist)

# GET /users/new
# Show an add form for users

@app.get("/users/new")
def add_user():
    """Returns a template with add user form"""
    #in models create something that we can iterate for details about user
    return render_template("users/new.html")

# POST /users/new
# Process the add form, adding a new user and going back to /users

@app.post('/users/new')
def process_form():
    form_data = request.form
    f_name = form_data['first_name']
    l_name = form_data['last_name']
    img = form_data['image_link']

    new_user = User(f_name, l_name, img)
    db.session.add(new_user)
    return redirect("/users")


# GET /users/[user-id]
# Show information about the given user.

# Have a button to get to their edit page, and to delete the user.

# GET /users/[user-id]/edit
# Show the edit page for a user.

# Have a cancel button that returns to the detail page for a user, and a save button that updates the user.

# POST /users/[user-id]/edit
# Process the edit form, returning the user to the /users page.
# POST /users/[user-id]/delete
# Delete the user.