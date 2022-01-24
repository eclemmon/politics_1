from database import db
from flask_twilio_twitter_server import app


def reset_db(app, db):
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == "__main__":
    reset_db(app, db)

