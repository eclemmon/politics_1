from database import db
from sqlalchemy.dialects.postgresql import JSON

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    messages = db.relationship('Message', backref='users', lazy=True)

    # def __init__(self, username, messages):
    #     self.username = username
    #     self.messages = messages

    def __repr__(self):
        return '<id {}>'.format(self.id)
