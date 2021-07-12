from webapp import db, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return f"{self.id, self.username}"


class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)


class Crypto(db.Model):
    __tablename__ = 'crypto'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    symbol = db.Column(db.String(10))
    price = db.Column(db.DECIMAL(20, 2))
    percent_change_24h = db.Column(db.DECIMAL(10, 3))
    market_cap = db.Column(db.DECIMAL(20))

    def __repr__(self):
        return f"{self.id, self.name}"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
