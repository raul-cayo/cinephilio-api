# Python libraries
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
# Own libraries
from models.movie import MovieSeenModel

_score_parser = reqparse.RequestParser()
_score_parser.add_argument(
    "score",
    type=int,
    required=False
)


class MovieSeen(Resource):
    @classmethod
    @jwt_required
    def post(cls, movie_id):
        data = _score_parser.parse_args()

        score = 0
        if data["score"]:
            score = data["score"]

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
    def put(cls, movie_id):
        data = _score_parser.parse_args()

        score = 0
        if data["score"]:
            score = data["score"]

        user_id = get_jwt_identity()
        movie_seen = MovieSeenModel.find_by_ids(user_id, movie_id)
        if not movie_seen:
            movie_seen = MovieSeenModel(user_id, movie_id, score)
        else:
            movie_seen.score = data["score"]

        movie_seen.save_to_db()

        return {"message": "Movie score succesfully updated"}, 200

    @classmethod
    @jwt_required
    def get(cls, movie_id):
        user_id = get_jwt_identity()
        movie_seen = MovieSeenModel.find_by_ids(user_id, movie_id)
        if not movie_seen:
            return {"message": "Movie not found in "
                    "this user 'Movies Seen List'"}, 404
        return movie_seen.json(), 200

    @classmethod
    @jwt_required
    def delete(cls, movie_id):
        user_id = get_jwt_identity()
        movie_seen = MovieSeenModel.find_by_ids(user_id, movie_id)
        if not movie_seen:
            return {"message": "Movie not found in "
                    "this user 'Movies Seen List'"}, 404\

        movie_seen.delete_from_db()
        return {"message": "Movie removed from this user "
                "'Movies Seen List'"}, 200


class MoviesSeenList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        return MovieSeenModel.all_by_user_json(user_id)
