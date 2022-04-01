from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        Post.query.delete()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(first_name="test_first",
                                    last_name="test_last",
                                    image_url=None)

        second_user = User(first_name="test_first_two", last_name="test_last_two",
                           image_url=None)

        db.session.add_all([test_user, second_user])
        db.session.commit()

        test_post = Post(title="test_title",
                                content="test_content", created_at=None,
                                user_id=test_user.id)

        second_post = Post(title="test_title_two",
                                content="test_content_two", created_at=None,
                                user_id=second_user.id)

        db.session.add_all([test_post, second_post])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_home_redirect(self):
        """Tests redirect and content on redirect page"""
        with self.client as client:
            response = client.get("/users", follow_redirects=True)
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('Testing for rendering user-list', html)

    def test_add_user(self):
        """Tests that when add button is clicked, it renders the add user html"""
        with self.client as client:
            response = client.get("/users/new", follow_redirects=True)
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Testing for rendering add-user', html)

    def test_process_new_user_form(self):
        """Tests that new user form processes input data correctly and shows up on redirect page"""
        #bugs encounters: post request tests: route, params={}, follow_redirects because on the app.py, it does not render_template but it does redirect instead.
        with self.client as client:
            response = client.post('/users/new', data={'first_name': 'Test', 'last_name': "Case",'image_url': DEFAULT_IMAGE_URL}, follow_redirects=True)

            html = response.get_data(as_text=True)
            self.assertIn('Test', html)
            self.assertIn("Case", html)

    def test_show_user_detail(self):
        """Tests that user details show up on the user-detail page after committed to database"""
        with self.client as client:
            response = client.get(f'/users/{self.user_id}')

            html = response.get_data(as_text=True)
            self.assertIn('test_first', html)
            self.assertIn("test_last", html)


    def test_get_new_post_form(self):
        """Tests that new post form shows up properly"""
        with self.client as client:
            response = client.get(f'/users/{self.user_id}/posts/new')
            html = response.get_data(as_text=True)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Testing for new post form', html)

    def test_add_post_successful(self):
        """Tests that post data is processed correctly and added to user page"""
        with self.client as client:
            response = client.post(f'/users/{self.user_id}/posts/new', data={'title': 'Test_Title', 'content': "Test_Content"},follow_redirects=True)

            html = response.get_data(as_text=True)
            self.assertIn('Test_Title', html)
