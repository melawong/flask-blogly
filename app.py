"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import db, connect_db, User, DEFAULT_IMAGE_URL, Post
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
    """Redirect to users page"""
    return redirect ("/users")

## GET /users
## Show all users.

# Make these links to view the detail page for the user.
## Have a link here to the add-user form.

@app.get("/users")
def get_users():
    """Retrieves all users in the db and renders template wth user list"""
    users = User.query.all()

    return render_template("home.html", users = users)

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
    image_url = form_data.get('image_url') or None

    new_user = User(first_name = first_name, last_name = last_name,
    image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    flash('User Successfully Added!')

    return redirect("/users")

# GET /users/[user-id]
# Show information about the given user.
# Have a button to get to their edit page, and to delete the user.
@app.get('/users/<int:id>')
def show_user_details(id):
    """Accepts user detail request and user id, renders template corresponding to the id"""
    user = User.query.get(id)
    posts = Post.query.filter(Post.user_id == id)

    return render_template("user-details.html", user = user, posts = posts)



# GET /users/[user-id]/edit
# Show the edit page for a user.
@app.get('/users/<int:id>/edit')
def get_edit_page(id):
    """Renders template to the edit-user.html with the correct id"""
    user = User.query.get(id)

    return render_template("edit-user.html", user = user)

# POST /users/[user-id]/edit
# Process the edit form, returning the user to the /users page.

@app.post('/users/<int:id>/edit')
def process_update(id):
    """Accepts form data and adds new user to db"""
    user = User.query.get(id)
    form_data = request.form
    user.first_name = form_data['first_name']
    user.last_name = form_data['last_name']
    user.image_url = form_data.get('image_url') or DEFAULT_IMAGE_URL

    db.session.commit()
    flash('User Successfully Updated!')

    return redirect(f"/users/{id}")

# POST /users/[user-id]/delete
# Delete the user.

@app.post('/users/<int:id>/delete')
def delete_user(id):
    '''Deletes user from database'''
    User.query.filter_by(id = id).delete()
    db.session.commit()
    flash('User Successfully Deleted!')

    return redirect('/users')


# GET /users/[user-id]/posts/new
# Show form to add a post for that user.
@app.get('/users/<int:id>/posts/new')
def get_new_post_form(id):
    user = User.query.get(id)

    return render_template("new-post.html", user = user)


# POST /users/[user-id]/posts/new
# Handle add form; add post and redirect to the user detail page.

@app.post('/users/<int:id>/posts/new')
def add_new_post(id):
    """Takes in form data and creates/adds new post to database. Returns
    redirect to user's detail page."""
    form = request.form
    title = form['title']
    content = form['content']

    new_post = Post(title = title, content = content, user_id = id)
    db.session.add(new_post)
    db.session.commit()
    flash('Post Successfully Added!')

    return redirect(f"/users/{id}")

# GET /posts/[post-id]
# Show a post.

@app.get("/posts/<int:id>")
def show_post(id):
    """Retrieves and renders template wth post"""
    post = Post.query.get(id)

    return render_template("post.html", post = post)

# Show buttons to edit and delete the post.

# GET /posts/[post-id]/edit
# Show form to edit a post, and to cancel (back to user page).

@app.get("/posts/<int:id>/edit")
def render_edit_post_page(id):
    post = Post.query.get(id)

    return render_template("edit-post.html", post = post)

# POST /posts/[post-id]/edit
# Handle editing of a post. Redirect back to the post view.
# POST /posts/[post-id]/delete
# Delete the post.