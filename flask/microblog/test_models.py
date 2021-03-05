from datetime import datetime, timedelta
import unittest

from app import app, db
from app.models import User, Post


class TestUser(unittest.TestCase):
    def setUp(self):
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_password_hashing(self):
        u = User(username="alpha")
        u.set_password("strong_password!")
        self.assertFalse(u.check_password("weak_password.."))
        self.assertTrue(u.check_password("strong_password!"))

    def test_avatar(self):
        u = User(username="beta", email="beta@example.com")
        self.assertEqual(
            u.avatar(128),
            (
                "https://www.gravatar.com/avatar/"
                "23f2c5086aa82e3f218c238632569d64"
                "?d=identicon&s=128"
            ),
        )

    def test_follow(self):
        u1 = User(username="gamma", email="gamma@example.com")
        u2 = User(username="delta", email="delta@example.com")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()

        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, "delta")
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, "gamma")

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # Create four users
        u1 = User(username="epsilon", email="epsilon@example.com")
        u2 = User(username="zeta", email="zeta@example.com")
        u3 = User(username="eta", email="eta@example.com")
        u4 = User(username="theta", email="theta@example.com")
        db.session.add_all([u1, u2, u3, u4])

        # Create four posts
        now = datetime.utcnow()
        p1 = Post(
            body="post from epsilon", author=u1, timestamp=now + timedelta(seconds=1)
        )
        p2 = Post(
            body="post from zeta", author=u2, timestamp=now + timedelta(seconds=4)
        )
        p3 = Post(body="post from eta", author=u3, timestamp=now + timedelta(seconds=3))
        p4 = Post(
            body="post from theta", author=u4, timestamp=now + timedelta(seconds=2)
        )
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # Setup the followers
        u1.follow(u2)
        u1.follow(u4)
        u2.follow(u3)
        u3.follow(u4)
        db.session.commit()

        # Check the followed posts of each other
        f1 = u1.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])

        f2 = u2.followed_posts().all()
        self.assertEqual(f2, [p2, p3])

        f3 = u3.followed_posts().all()
        self.assertEqual(f3, [p3, p4])

        f4 = u4.followed_posts().all()
        self.assertEqual(f4, [p4])


if __name__ == "__main__":
    unittest.main(verbosity=2)
