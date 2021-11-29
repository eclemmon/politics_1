from flask_twilio_twitter_server import db
from sqlalchemy.dialects.postgresql import JSON

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, text, user):
        self.text = text

    def __repr__(self):
        return '<id {}>'.format(self.id)