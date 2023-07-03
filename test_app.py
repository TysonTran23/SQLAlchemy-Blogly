from unittest import TestCase

from app import app
from models import User, db, Post

# Use test database and don't clutter tests with SQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly_test"
app.config["SQLALCHEMY_ECHO"] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config["TESTING"] = True


# This is a bit of hack, but don't use Flask DebugToolbar
app.config["DEBUG_TB_HOSTS"] = ["dont-show-debug-toolbar"]

db.drop_all()
db.create_all()


class UserTestCase(TestCase):
    def setUp(self):
        User.query.delete()
        default_url = "https://i.natgeofe.com/k/d2701667-c426-4a1b-8d75-d01bdc387fdc/vietnam-ha-long-bay.jpg?w=1084.125&h=609"

        user = User(first_name="tyson", last_name="tran", image_url=default_url)
        db.session.add(user)
        db.session.commit()

        post = Post(title='Canada wins olympics', content='We won gold!', user_id=1)

        self.user = user
        self.user.id = user.id
        
        self.post = post
        self.post.id = post.id
        

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_home_page(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)

    def test_adding_user(self):
        with app.test_client() as client:
            user = {
                "first": "tyson",
                "last": "tran",
                "image": "https://i.natgeofe.com/k/d2701667-c426-4a1b-8d75-d01bdc387fdc/vietnam-ha-long-bay.jpg?w=1084.125&h=609",
            }
            resp = client.post("/users/new", data=user, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<a href="/users/1">tyson tran</a>', html)
    
    def test_show_user_detail(self):
        with app.test_client() as client:

            resp = client.get(f'/users/{self.user.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>tyson tran</h1>', html)

    def test_show_post_detail(self):
        with app.test_client() as client:

            resp = client.get(f'/posts/{self.post.id}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Canada wins olympics</h1>', html)

