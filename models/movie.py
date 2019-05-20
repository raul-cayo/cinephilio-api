# Python libraries
from datetime import date
# Own libraries
from db import db


class MovieModel(db.Model):
    __tablename__ = "movies"

    movie_id = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(128), nullable=False)
    release_date = db.Column(db.Date, nullable=False)
    poster_path = db.Column(db.String(128), default=None)

    is_categorized = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.Date, default=date.today())
    updated_at = db.Column(
        db.Date,
        onupdate=date.today(),
        default=date.today()
    )

    def __init__(
            self, movie_id, original_title, release_date, poster_path=None):
        self.movie_id = movie_id
        self.original_title = original_title
        self.release_date = date(
            int(release_date[0:4]),
            int(release_date[5:7]),
            int(release_date[8:10])
        )
        self.poster_path = poster_path

    def json(self):
        return {
            "movie_id": self.movie_id,
            "original_title": self.original_title,
            "release_date": self.release_date.strftime("%Y-%m-%d"),
            "poster_path": self.poster_path,
            "is_categorized": self.is_categorized,
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
    def find_by_id(cls, _movie_id):
        return cls.query.filter_by(movie_id=_movie_id).first()

    @classmethod
    def find_by_title(cls, title):
        return cls.query.filter_by(original_title=title).first()


class MovieSeenModel(db.Model):
    __tablename__ = "movies_seen"

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        primary_key=True
    )
    movie_id = db.Column(
        db.Integer,
        db.ForeignKey("movies.movie_id"),
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
