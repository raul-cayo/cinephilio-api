# Python libraries
from datetime import date
# Own libraries
from db import db


class AttributeModel(db.Model):
    __tablename__ = "attributes"

    attr_id = db.Column(db.String(16), primary_key=True)
    description = db.Column(db.String(128))

    def __init__(self, attr_id, description):
        self.attr_id = attr_id
        self.description = description

    def json(self):
        return {
            "attr_id": self.attr_id,
            "description": self.description
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _attr_id):
        return cls.query.filter_by(attr_id=_attr_id).first()

    @classmethod
    def find_all_json(cls):
        all_attributes = cls.query.all()
        return {"all_attributes": [attr.json() for attr in all_attributes]}


class UserProfileModel(db.Model):
    __tablename__ = "users_profile"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        primary_key=True
    )
    attr_id = db.Column(
        db.String(16),
        db.ForeignKey("attributes.attr_id"),
        primary_key=True
    )
    value = db.Column(db.Integer, default=50)

    created_at = db.Column(db.Date, default=date.today())
    updated_at = db.Column(
        db.Date,
        onupdate=date.today(),
        default=date.today()
    )

    def __init__(self, user_id, attr_id, value=50):
        self.user_id = user_id
        self.attr_id = attr_id
        self.value = value

    def get_id(self):
        return self.attr_id

    def get_value(self):
        return self.value

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_ids(cls, _user_id, _attr_id):
        return \
            cls.query.filter_by(user_id=_user_id, attr_id=_attr_id).first()

    @classmethod
    def user_profile_json(cls, _user_id):
        all_attr = cls.query.filter_by(user_id=_user_id).all()

        profile = {}
        profile["user_id"] = _user_id
        for attr in all_attr:
            profile[attr.get_id()] = attr.get_value()

        return profile
