"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, User, DEFAULT_IMAGE_URL
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'shhhh'
debug = DebugToolbarExtension(app)


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
    return render_template("add-user.html")

# POST /users/new
# Process the add form, adding a new user and going back to /users

@app.post('/users/new')
def process_new_user_form():
    """Accepts form data and adds new user to db"""
    form_data = request.form
    first_name = form_data['first_name']
    last_name = form_data['last_name']
    img = form_data['image_url']

    if img == '':
        img = DEFAULT_IMAGE_URL

    new_user = User(first_name = first_name, last_name = last_name, image_url = img)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")

# GET /users/[user-id]
# Show information about the given user.
# Have a button to get to their edit page, and to delete the user.
@app.get('/users/<int:id>')
def show_user_details(id):
    """Accepts user detail request and user id, renders template corresponding to the id"""
    user_data = User.query.get(id)

    return render_template("user-details.html", user_data = user_data)



# GET /users/[user-id]/edit
# Show the edit page for a user.
@app.get('/users/<int:id>/edit')
def get_edit_page(id):
    """Renders template to the edit-user.html with the correct id"""
    user_data = User.query.get(id)

    return render_template("edit-user.html", user_data = user_data)

# POST /users/[user-id]/edit
# Process the edit form, returning the user to the /users page.

@app.post('/users/<int:id>/edit')
def process_update(id):
    """Accepts form data and adds new user to db"""
    user_data = User.query.get(id)
    form_data = request.form
    edit_first_name = form_data['first_name']
    edit_last_name = form_data['last_name']
    edit_img = form_data['image_url']
    user_data.first_name = edit_first_name
    user_data.last_name = edit_last_name

    if edit_img == '':
        user_data.image_url = DEFAULT_IMAGE_URL
    else:
        user_data.image_url = edit_img


    db.session.commit()
    return redirect(f"/users/{id}")


# Have a cancel button that returns to the detail page for a user, and a save button that updates the user.
# - WE ARE ALREADY DOING IT HAHA



# POST /users/[user-id]/delete
# Delete the user.

@app.post('/users/<int:id>/delete')
def delete_user(id):
    '''Deletes user from database'''
    User.query.filter_by(id = id).delete()
    db.session.commit()
    flash('User Successfully Deleted!')
    return redirect('/users')
