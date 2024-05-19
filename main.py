from flask import Flask, json
from flask_restful import Api
from api import RoboAPI


app = Flask(__name__)
api = Api(app)

# Building up API endpoints:
api.add_resource(RoboAPI, '/robot/<string:robo_id>', endpoint='robot')


if __name__ == '__main__':
    app.run()
