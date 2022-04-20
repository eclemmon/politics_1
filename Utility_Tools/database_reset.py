from database import db
from flask_twilio_twitter_server import app


def reset_db(app, db):
    """
    Resets the app's database. WARNING! WILL DELETE ALL THE TEXTS YOU GOT! :,(
    :param app: Flask app
    :param db: Database
    :return: None
    """
    with app.app_context():
        db.drop_all()
        db.create_all()


if __name__ == "__main__":
    reset_db(app, db)

