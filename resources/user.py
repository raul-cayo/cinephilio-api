# Python libraries
from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
)
# Own libraries
from models.user import UserModel
from blacklist import BLACKLIST


class UserRegister(Resource):
    @classmethod
    def post(cls):
        register_parser = reqparse.RequestParser()
        register_parser.add_argument(
            "username",
            type=str,
            required=True,
            help="Username required"
        )
        register_parser.add_argument(
            "email",
            type=str,
            required=True,
            help="Email required"
        )
        register_parser.add_argument(
            "password",
            type=str,
            required=True,
            help="Password required"
        )
        register_parser.add_argument(
            "birthdate",
            type=str,
            required=True,
            help="Birthdate required"
        )

        data = register_parser.parse_args()

        if UserModel.find_by_email(data["email"]):
            return {"message": "A user with that email already exists"}, 400

        # **data | username=data["username"], password=data["password"], ...
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully"}, 201


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user.json(), 200

    @classmethod
    @jwt_required
    def delete(cls):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if not user:
            return {"message": "User not found"}, 404

        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        user.delete_from_db()
        return {"message": "User deleted"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        login_parser = reqparse.RequestParser()
        login_parser.add_argument(
            "email",
            type=str,
            required=True,
            help="Email required"
        )
        login_parser.add_argument(
            "password",
            type=str,
            required=True,
            help="Password required"
        )

        data = login_parser.parse_args()
        user = UserModel.find_by_email(data["email"])

        if user and safe_str_cmp(user.password, data["password"]):
            access_token = create_access_token(
                identity=user.user_id,
                fresh=True
            )
            refresh_token = create_refresh_token(user.user_id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        return {"message": "Invalid credentials"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is 'JWT ID' a unique identifier
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=False)
        return {"access_token": new_token}, 200
