from database import db
from Models.user import User


class Message(db.Model):
    """
    Message model class for db storage.
    id: Message id -> Integer
    text: Stored message -> String
    date: Datatime object -> DateTime
    movement: The Movement number -> Integer
    scored: Whether the performance is scored or not (helper for identifying performances) -> boolean
    user_id: the user id who submitted the message for -> Integer & Foreign key
    """
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    date = db.Column(db.DateTime, unique=True, nullable=False)
    movement = db.Column(db.Integer, nullable=True)
    scored = db.Column(db.BOOLEAN, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        """
        Representation of a Message model
        :return: str
        """
        return '<id {}:: On {} in movement {}: User {} said: {}>'.format(self.id,
                                                                         self.date,
                                                                         self.movementself.user.username,
                                                                         self.text)
