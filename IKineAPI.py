from flask import Response
from flask_restful import Resource, reqparse
from pymongo import MongoClient, errors
from bson.json_util import dumps
from RoboCalc import ikine

class IKineAPI(Resource):

    def __init__(self,
                 db_uri='mongodb://localhost:27017',
                 db_name='schoolX',
                 db_col_name='robots'):
        # Database settings:
        self._db_uri = db_uri
        self._db_name = db_name
        self._db_col_name = db_col_name
        # Request parser:
        self._reqparser = reqparse.RequestParser()

        self._reqparser.add_argument('pos', 
                                     type=float,
                                     action='append', 
                                     location='json', 
                                     help='Positions in globs', 
                                     required=True,
                                     store_missing=False)
        
        self._reqparser.add_argument('eul', 
                                     type=float,
                                     action='append', 
                                     location='json', 
                                     help='Euler angles of effector, rads', 
                                     required=True,
                                     store_missing=False)
        
        self._reqparser.add_argument('XYZ', 
                                     type=str,
                                     location='json', 
                                     help='XYZ | ZXY | etc.', 
                                     required=True,
                                     store_missing=False)

        # Superclass constructor:
        super(IKineAPI, self).__init__()

    def get(self, robo_id: str):
        # Get your robot's specs from the DB:
        try:
            with MongoClient(self._db_uri) as client_:  # The connection will be closed automatically
                robo_doc_ = client_[self._db_name][self._db_col_name].find_one({'robo_id': str(robo_id)})
                if robo_doc_:
                    robo_ = {'robo_id': robo_id} | dict(robo_doc_['links'])
                    data_ = dict(self._reqparser.parse_args())
                    # Perform forward kinematics calculation here using robocalc
                    response = ikine(robo__=robo_, position__=data_['pos'], 
                                     orientationEul__=(data_['eul'], data_['XYZ']))
                    return Response(status=200, response=response,
                                    mimetype='application/json')
                else:
                    return Response(status=404, response=f'''Robot with id '{robo_id}' is not present''')
        except errors.ConnectionFailure:
            return Response(status=500, response=f'''Server '{self._db_uri}' is not available''')
