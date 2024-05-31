from flask import Response
from flask_restful import Resource, reqparse
from pymongo import MongoClient, errors
from bson.json_util import dumps

class RoboAPI(Resource):

  def __init__(self, 
               db_uri = 'mongodb://localhost:27017', 
               db_name = 'schoolX',
               db_col_name = 'robots'):
    # Database settings:
    self._db_uri = db_uri
    self._db_name = db_name 
    self._db_col_name = db_col_name
    # Request parser:
    self._reqparser = reqparse.RequestParser()
      
    self._reqparser.add_argument('num_of_joints', 
                                 type=int,
                                  location='json', 
                                  required=False,
                                  store_missing=False)
      
    self._reqparser.add_argument('links', type=dict,
                                  location='json',
                                  help='The specs of a robot', 
                                  required=False,
                                  store_missing=False)

    # Superclass constructor:
    super(RoboAPI, self).__init__()

  def get(self, robo_id: str):
    # Get your robot's specs from the DB:
    try:
      with MongoClient(self._db_uri) as client_: # The connection will be closed automatically
        res_ = client_[self._db_name][self._db_col_name].find_one({'robo_id': str(robo_id)})
        if res_:
          return Response(status=200, response=dumps(res_), mimetype='application/json')  # jsonify(res_) is bad for ObjectID
        else:
          # It the result is empty, there are three basic opportunities:
          if self._db_name not in client_.list_database_names():
            return Response(status=416, response=f'''Database '{self._db_name}' is not present''')
          elif self._db_col_name not in client_[self._db_name].list_collection_names():
            return Response(status=418, response=f'''Collection '{self._db_col_name}' is not present''')
          else:
            return Response(status=404, response=f'''Robot with id '{robo_id}' is not present''')
    except errors.ConnectionFailure:
      # This will occur if the server will be unavailable:
      return Response(status=500, response=f'''Server '{self._db_uri}' is not available''')
      
   
  def put(self, robo_id: str):
    # Update a robot in DB:
    try:
      with MongoClient(self._db_uri) as client_:
      # Couple of checks:
        if self._db_name not in client_.list_database_names():
          return Response(status=416, response=f'''Database '{self._db_name}' is not present''')
        if self._db_col_name not in client_[self._db_name].list_collection_names():
          return Response(status=418, response=f'''Collection '{self._db_col_name}' is not present''') 

       # Main code:
        col_ = client_[self._db_name][self._db_col_name]
        # request.get_json(force=True)
        data_ = dict(self._reqparser.parse_args())
        print(f'PUT data: {data_}, type = {type(data_)}')
        res_ = col_.update_one(filter={'robo_id': str(robo_id)}, 
                               update={'$set': data_}, 
                               upsert=True)
        return Response(status=200, response=res_.raw_result)
       
    except errors.OperationFailure:
      return Response(status=500, response='Server internal error')
    except errors.ConnectionFailure:
      return Response(status=500, response=f'''Server '{self._db_uri}' is not available''')
    

  def delete(self, robo_id):
      # Delete a robot
      pass
  

  def post(self, robo_id):
    try:
      with MongoClient(self._db_uri) as client_:
        data_ = dict(self._reqparser.parse_args())
        col_ = client_[self._db_name][self._db_col_name]
        doc_ = {'robo_id': robo_id} | data_
        res_ = col_.insert_one(doc_)
        if res_:
          return Response(status=200, response=f'''POSTed new robot to DB: {res_.inserted_id}''')
        else:
          return Response(status=500, response=f'Failed to POST new robot to DB')
    except Exception:
      pass
