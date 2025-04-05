from extensions import db, login_manager  # Теперь из extensions.py
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    name = db.Column(db.String(50))
    position = db.Column(db.String(50))
    product = db.Column(db.String(100))
    utp = db.Column(db.String(100))
    lpr_position = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.email}>'

class Objection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    objection = db.Column(db.String(100))
    response = db.Column(db.String(200))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))