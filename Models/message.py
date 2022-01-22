from database import db
from Models.user import User


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    # def __init__(self, text, date, user_id):
    #     self.text = text
    #     self.date = date
    #     self.user = User.query.get(user_id)

    def __repr__(self):
        return '<id {}:: On {} User {} said: {}>'.format(self.id, self.date, self.user.username, self.text)
