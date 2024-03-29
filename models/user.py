# Python libraries
from datetime import date
# Own libraries
from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    profile_weight = db.Column(db.Integer, nullable=False)
    auth = db.Column(db.Boolean, nullable=False)

    created_at = db.Column(db.Date, default=date.today())
    updated_at = db.Column(
        db.Date,
        onupdate=date.today(),
        default=date.today()
    )

    def __init__(self, username, email, password, birthdate, auth):
        self.username = username
        self.email = email
        self.password = password
        self.birthdate = date(
            int(birthdate[0:4]),
            int(birthdate[5:7]),
            int(birthdate[8:10])
        )
        self.auth = auth
        self.profile_weight = 0

    def json(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "birthdate": self.birthdate.strftime("%Y-%m-%d"),
            "authentication": self.auth,
            "created_at": self.created_at.strftime("%Y-%m-%d"),
            "updated_at": self.updated_at.strftime("%Y-%m-%d")
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _user_id):
        return cls.query.filter_by(user_id=_user_id).first()

    @classmethod
    def find_by_email(cls, _email):
        return cls.query.filter_by(email=_email).first()
