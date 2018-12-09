from app import db
from sqlalchemy.dialects.postgresql import JSON
from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    todxdata = db.Column(JSON)

    def __init__(self, username):
        self.username = username
        # self.password_hash = ''
        # self.todxdata = todxdata

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
