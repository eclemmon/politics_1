from database import db
from Models.user import User


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, unique=True, nullable=False)
    movement = db.Column(db.Integer, nullable=True)
    scored = db.Column(db.BOOLEAN, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return '<id {}:: On {} in movement {}: User {} said: {}>'.format(self.id,
                                                                         self.date,
                                                                         self.movementself.user.username,
                                                                         self.text)
