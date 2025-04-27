from flask_login import UserMixin
from extensions import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(100))
    position = db.Column(db.String(100))
    product = db.Column(db.String(100))
    utp = db.Column(db.String(255))
    lpr_position = db.Column(db.String(100))

class Objection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    objection = db.Column(db.String(255), nullable=False)
    response = db.Column(db.Text, nullable=False)