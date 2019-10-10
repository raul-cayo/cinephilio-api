# Python libraries
from flask_restful import Resource
from random import randint
# Own libraries
from models.fun_fact import FunFactModel


class FunFact(Resource):
    @classmethod
    def get(cls):
        total = FunFactModel.total_fun_fatcs()
        return FunFactModel.find_by_id(randint(1, total)).json(), 200
