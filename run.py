# This file is for running the app from heroku because heroku wont
# run the app.py directly and we are avoiding circular imports
from app import app
from db import db

db.init_app(app)


@app.before_first_request
def create_tables():
    db.create_all()
