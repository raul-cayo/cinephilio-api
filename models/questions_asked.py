# Python libraries
from datetime import date
# Own libraries
from db import db


class QuestionAskedModel(db.Model):
    __tablename__ = "questions_asked"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        primary_key=True
    )
    question_id = db.Column(db.Integer, primary_key=True)
    times_asked = db.Column(db.Integer, default=1)

    created_at = db.Column(
        db.Date,
        default=date.today()
    )
    updated_at = db.Column(
        db.Date,
        onupdate=date.today(),
        default=date.today()
    )

    def __init__(self, user_id, question_id, times_asked=1):
        self.user_id = user_id
        self.question_id = question_id
        self.times_asked = times_asked

    def json(self):
        return {
            "question_id": self.question_id,
            "times_asked": self.times_asked
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_ids(cls, _user_id, _question_id):
        return cls.query.filter_by(user_id=_user_id,
                                   question_id=_question_id).first()

    @classmethod
    def all_by_user_json(cls, _user_id):
        all_questions = cls.query.filter_by(
            user_id=_user_id
        ).all()
        return {
          "questions_asked": [question.json() for question in all_questions]
        }
