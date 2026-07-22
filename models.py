from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    village = db.Column(db.String(100))
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"<User {self.fullname}>"

class FarmDiary(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    farmer = db.Column(db.String(100))

    activity = db.Column(db.String(300))

    expense = db.Column(db.Float)

    date = db.Column(db.String(30))