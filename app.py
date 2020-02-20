# Python libraries
import os
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
# Own libraries
from resources.user import (
    User,
    UserLogin,
    TokenRefresh,
    UserLogout
)
from resources.movie_seen import (
    MovieSeen,
    MoviesSeenList,
)
from resources.user_profile import (
    Attribute,
    AttributesList,
    UserProfile
)
from resources.fun_fact import FunFact
from blacklist import BLACKLIST

# Initialize the app and configure the database
app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('JAWSDB_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.config["JWT_BLACKLIST_ENABLED"] = True
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = (60 * 60 * 1)  # 1 horas
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = ["access", "refresh"]
app.secret_key = 'cayo'  # app.config["JWT_SECRET_KEY"] defaults to this value
api = Api(app)

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


# Adding the RESOURCES to the API
api.add_resource(User, "/user")
api.add_resource(UserLogin, "/login")
api.add_resource(UserLogout, "/logout")
api.add_resource(TokenRefresh, "/refresh")

api.add_resource(MovieSeen, "/movie-seen/<int:movie_id>")
api.add_resource(MoviesSeenList, "/movies-seen")

api.add_resource(Attribute, "/attr/<string:attr_id>")
api.add_resource(AttributesList, "/attrs")
api.add_resource(UserProfile, "/profile")

api.add_resource(FunFact, "/fun-fact")

# Run the API from this file
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
