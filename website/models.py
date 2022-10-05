from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask_admin import Admin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    admin = db.Column(db.Boolean, default=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    market_id = db.Column(db.Integer, nullable=False)
    img_url = db.Column(db.String(150), nullable=False)

class Market(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False, unique=True)
    address = db.Column(db.String(150), nullable=False)
    img_url = db.Column(db.String(150), nullable=False)