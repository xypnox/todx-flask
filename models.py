from app import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), unique=True)
    password_hash = db.Column(db.String())
    todxdata = db.Column(JSON)

    def __init__(self, username, password_hash, todxdata):
        self.username = username
        self.password_hash = password_hash
        self.todxdata = todxdata

    def __repr__(self):
        return '<id {}>'.format(self.id)
