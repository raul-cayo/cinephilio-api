# Python libraries
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
# Own libraries
from models.movie import MovieModel, MovieSeenModel


class MovieAdd(Resource):
    @classmethod
    def post(cls):
        movie_parser = reqparse.RequestParser()
        movie_parser.add_argument(
            "movie_id",
            type=int,
            required=True,
            help="Movie ID required"
        )
        movie_parser.add_argument(
            "original_title",
            type=str,
            required=True,
            help="Original title required"
        )
        movie_parser.add_argument(
            "release_date",
            type=str,
            required=True,
            help="Release date required"
        )
        movie_parser.add_argument(
            "poster_path",
            type=str,
            required=False
        )

        data = movie_parser.parse_args()

        if MovieModel.find_by_id(data["movie_id"]):
            return {"message": "A movie with that ID already exists"}, 400

        if MovieModel.find_by_title(data["original_title"]):
            return {"message": "A movie with that title already exists"}, 400

        movie = MovieModel(**data)
        movie.save_to_db()

        return {"message": "Movie added succesfully"}, 201


class Movie(Resource):
    @classmethod
    def get(cls, movie_id):
        movie = MovieModel.find_by_id(movie_id)
        if not movie:
            return {"message": "Movie not found"}, 404
        return movie.json(), 200


class MovieSeen(Resource):
    @classmethod
    @jwt_required
    def post(cls, movie_id):
        score_parser = reqparse.RequestParser()
        score_parser.add_argument(
            "score",
            type=int,
            required=False
        )

        data = score_parser.parse_args()
        if data["score"]:
            score = data["score"]
        else:
            score = 0

        user_id = get_jwt_identity()

        if MovieSeenModel.find_by_ids(user_id, movie_id):
            return {"message": "This movie is already on "
                    "current user's Movies Seen List"}

        movie_seen = MovieSeenModel(user_id, movie_id, score)
        movie_seen.save_to_db()

        return {"message": "Movie added succesfully "
                "to user movies seen list"}, 201

    @classmethod
    @jwt_required
    def get(cls, movie_id):
        user_id = get_jwt_identity()
        movie_seen = MovieSeenModel.find_by_ids(user_id, movie_id)

        if not movie_seen:
            return {"message": "Movie not found in "
                    "this user 'Movies Seen List'"}, 404
        return {"message": "Movie seen found on this list"}
