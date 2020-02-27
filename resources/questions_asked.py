# Python libraries
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
# Own libraries
from models.questions_asked import QuestionAskedModel

_questions_parser = reqparse.RequestParser()
_questions_parser.add_argument(
    "questions_asked",
    type=int,
    required=True,
    action="append"
)


class QuestionAsked(Resource):
    @classmethod
    @jwt_required
    def put(cls):
        data = _questions_parser.parse_args()
        user_id = get_jwt_identity()

        for question_id in data["questions_asked"]:
            question_asked = QuestionAskedModel.find_by_ids(user_id,
                                                            question_id)
            if not question_asked:
                question_asked = QuestionAskedModel(user_id, question_id, 1)
            else:
                question_asked.times_asked += 1
            question_asked.save_to_db()

        return {"message": "Questions succesfully added or updated"}, 200

    @classmethod
    @jwt_required
    def delete(cls, movie_id):
        user_id = get_jwt_identity()
        question_asked = QuestionAskedModel.find_by_ids(user_id, movie_id)
        if not question_asked:
            return {"message": "Question not found in "
                    "this user 'Questions Asked List'"}, 404

        question_asked.delete_from_db()
        return {"message": "Question removed from this user "
                "'Questions Asked' List'"}, 200


class QuestionsAskedList(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        return QuestionAskedModel.all_by_user_json(user_id)
