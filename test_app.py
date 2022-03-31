from unittest import TestCase
from app import app, db
from models import User

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BloglyTestCase(TestCase):
    """Test flask app of Blogly."""

    def setUp(self):
        """Stuff to do before every test."""
        self.client = app.test_client()


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
            response = client.post('/users/new', data={'first_name': 'Test', 'last_name': "Case",'image_url': ""}, follow_redirects=True)

            html = response.get_data(as_text=True)
            self.assertIn('Test', html)
            self.assertIn("Case", html)

    def test_show_user_detail(self):
        """Tests that user details show up on the user-detail page after committed to database"""
        #bugs encountered: forgot to add and commit dummy data into database
        with self.client as client:
            user1 = User(first_name = "Test", last_name = "Case", image_url = "")
            db.session.add(user1)
            db.session.commit()
            response = client.get(f'/users/{user1.id}')
            #
            html = response.get_data(as_text=True)
            self.assertIn('Test', html)
            self.assertIn("Case", html)
