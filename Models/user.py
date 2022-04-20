from database import db
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model):
    """
    User model class for db storage.
    id: user id -> Integer
    username: User name -> String
    messages: message ids -> relationship
    """
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    messages = db.relationship('Message', backref='users', lazy=True)

    def __repr__(self):
        """
        Representation of the User model.
        :return: str
        """
        return '<id {}:: username: {}>'.format(self.id, self.username)
