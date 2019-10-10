# Python libraries
from datetime import date
# Own libraries
from db import db


class MovieSeenModel(db.Model):
    __tablename__ = "movies_seen"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        primary_key=True
    )
    movie_id = db.Column(
        db.Integer,
        primary_key=True
    )
    score = db.Column(db.Integer, default=0)

    created_at = db.Column(db.Date, default=date.today())
    updated_at = db.Column(
        db.Date,
        onupdate=date.today(),
        default=date.today()
    )

    def __init__(self, user_id, movie_id, score=0):
        self.user_id = user_id
        self.movie_id = movie_id
        self.score = score

    def json(self):
        return {
            "user_id": self.user_id,
            "movie_id": self.movie_id,
            "score": self.score
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_ids(cls, _user_id, _movie_id):
        return \
            cls.query.filter_by(user_id=_user_id, movie_id=_movie_id).first()

    @classmethod
    def all_by_user_json(cls, _user_id):
        all_movies = cls.query.filter_by(user_id=_user_id).all()
        return {"movies_seenn": [movie.json() for movie in all_movies]}
