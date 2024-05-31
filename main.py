from flask import Flask, json
from flask_restful import Api
from RoboAPI import RoboAPI
from FKineAPI import FKineAPI
from IKineAPI import IKineAPI


app = Flask(__name__)
api = Api(app)

# Building up API endpoints:
api.add_resource(RoboAPI, '/robot/<string:robo_id>', endpoint='robot')
api.add_resource(FKineAPI, '/fkine/<string:robo_id>', endpoint='fkine')
api.add_resource(IKineAPI, '/ikine/<string:robo_id>', endpoint='ikine')


if __name__ == '__main__':
    app.run(host='0.0.0.0')
