# Python libraries
from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required
# Own libraries
from models.user_profile import AttributeModel
from models.user_profile import UserProfileModel
from models.user import UserModel


class Attribute(Resource):
    @classmethod
    def post(cls, attr_id):
        attr_parser = reqparse.RequestParser()
        attr_parser.add_argument(
            "description",
            type=str,
            required=True
        )
        data = attr_parser.parse_args()

        if AttributeModel.find_by_id(attr_id):
            return {"message": "This attribute already exists"}

        attribute = AttributeModel(attr_id, data["description"])
        attribute.save_to_db()

        return {"message": "Attribute added succesfully"}, 201

    @classmethod
    def delete(cls, attr_id):
        attribute = AttributeModel.find_by_id(attr_id)
        if not attribute:
            return {"message": "Attribute not found"}, 404

        attribute.delete_from_db()
        return {"message": "Attribute deleted"}, 200


class AttributesList(Resource):
    @classmethod
    def get(cls):
        return AttributeModel.find_all_json()


class UserProfile(Resource):
    @classmethod
    @jwt_required
    def put(cls):
        profile_parser = reqparse.RequestParser()
        profile_parser.add_argument(
            "violence",
            type=int,
            required=True
        )
        profile_parser.add_argument(
            "complexity",
            type=int,
            required=True
        )
        profile_parser.add_argument(
            "tension",
            type=int,
            required=True
        )
        profile_parser.add_argument(
            "realism",
            type=int,
            required=True
        )
        profile_parser.add_argument(
            "originality",
            type=int,
            required=True
        )
        profile_parser.add_argument(
            "education",
            type=int,
            required=True
        )
        profile_parser.add_argument(
            "production",
            type=int,
            required=True
        )
        data = profile_parser.parse_args()
        user_id = get_jwt_identity()

        for attr_id in data:
            attr = UserProfileModel.find_by_ids(user_id, attr_id)
            if not attr:
                attr = UserProfileModel(user_id, attr_id, data[attr_id])
            else:
                attr.value = data[attr_id]
            attr.save_to_db()

        user = UserModel.find_by_id(user_id)
        user.profile_weight += 1
        user.save_to_db()

        return {"message": "User profile succesfully updated"}, 200

    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        return UserProfileModel.user_profile_json(user_id)
