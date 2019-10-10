# Python libraries
# Own libraries
from db import db


class FunFactModel(db.Model):
    __tablename__ = "fun_facts"

    fun_fact_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(45), nullable=False)

    def __init__(self, text):
        self.text = text

    def json(self):
        return {
            "fun_fact_id": self.fun_fact_id,
            "text": self.text,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, _fun_fact_id):
        return cls.query.filter_by(fun_fact_id=_fun_fact_id).first()

    @classmethod
    def total_fun_fatcs(cls):
        return len(cls.query().all())
