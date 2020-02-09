# Python libraries
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
# Own libraries
from models.movie_seen import MovieSeenModel

_score_parser = reqparse.RequestParser()
_score_parser.add_argument(
    "score",
    type=int,
    required=False
)


class MovieSeen(Resource):
    @classmethod
    @jwt_required
    def put(cls, movie_id):
        # data contains: liked_by_user, is_deleted
        data = _score_parser.parse_args()

        user_id = get_jwt_identity()
        movie_seen = MovieSeenModel.find_by_ids(user_id, movie_id)
        if not movie_seen:
            movie_seen = MovieSeenModel(
                user_id,
                movie_id,
                data["liked_by_user"],
                data["is_deleted"]
            )
        else:
            movie_seen.liked_by_user = data["liked_by_user"]
            movie_seen.is_deleted = data["is_deleted"]

        movie_seen.save_to_db()

        return {"message": "Movie succesfully added or updated"}, 200

    @classmethod
    @jwt_required
    def delete(cls, movie_id):
        user_id = get_jwt_identity()
        movie_seen = MovieSeenModel.find_by_ids(user_id, movie_id)
        if not movie_seen:
            return {"message": "Movie not found in "
                    "this user 'Movies Seen List'"}, 404

        movie_seen.delete_from_db()
        return {"message": "Movie removed from this user "
                "'Movies Seen List'"}, 200


class MoviesSeenList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        return MovieSeenModel.all_by_user_json(user_id)
