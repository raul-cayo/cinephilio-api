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
import requests
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
# Own libraries
from models.user import UserModel
from blacklist import BLACKLIST
from email_token import generate_confirmation_token

_user_parser = reqparse.RequestParser()
_user_parser.add_argument(
    "username",
    type=str,
    required=True,
    help="Username required"
)
_user_parser.add_argument(
    "email",
    type=str,
    required=True,
    help="Email required"
)
_user_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="Password required"
)
_user_parser.add_argument(
    "birthdate",
    type=str,
    required=True,
    help="Birthdate required"
)


class User(Resource):
    @classmethod
    def post(cls):
        data = _user_parser.parse_args()
        if UserModel.find_by_email(data["email"]):
            return {"message": "A user with that email already exists"}, 400

        user = UserModel(data["username"], data["email"],
                         data["password"], data["birthdate"], False)
        user.save_to_db()
        return {"message": "User created successfully"}, 201

    @classmethod
    @jwt_required
    def put(cls):
        data = _user_parser.parse_args()
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)

        if not user:
            return {"message": "User not found"}, 404

        if user.email != data["email"] and \
                UserModel.find_by_email(data["email"]):
            return {"message": "A user with that email already exists"}, 400

        # Update user information
        user.username = data["username"]
        user.email = data["email"]
        user.password = data["password"]
        user.birthdate = data["birthdate"]

        user.save_to_db()
        return {"message": "User updated successfully"}, 200

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
                "refresh_token": refresh_token,
                "username": user.username
            }, 200

        return {"message": "Invalid credentials"}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()["jti"]  # jti is 'JWT ID' a unique identifier
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class TokenRefresh(Resource):
    @jwt_required
    def get(self):
        return {"message": "Token is still valid"}, 200

    @jwt_refresh_token_required
    def post(self):
        user_id = get_jwt_identity()
        new_token = create_access_token(identity=user_id, fresh=False)
        return {"access_token": new_token}, 200

class UserAuth(Resource):
    # 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 llave de sendGrid
    @classmethod
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.find_by_id(user_id)
        
        token = generate_confirmation_token(user.email)

        message = Mail(
                from_email='no-reply@cinephilio.com',
                to_emails=user.email,
                subject='Confirmación de Cinephilio',
                html_content='<strong>Es la primera prueba de un envío, este sería tu token '+ token +'</strong>')

        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            return {"auth_token": "Token enviado"}, 200
        except Exception as e:
            print(e.message)