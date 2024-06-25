#!/usr/bin/python           
# This is server.py file
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort              

### Setup ###
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

### Database tables ###
# the table for a cluster of anchors and tags
class ClusterModel(db.Model):
   __tablename__ = "clusters"
   cluster_id = db.Column(db.Integer, primary_key=True)
   senior_name = db.Column(db.String(80), nullable=False)
   senior_x = db.Column(db.Integer, nullable=False, default = 0)
   senior_y = db.Column(db.Integer, nullable=False, default = 0)

   def __repr__(self):
      return f"Cluster(cluster_id = {self.cluster_id}, senior_name = {self.senior_name})"

# the table for all anchors, including which cluster they are associated with, their x and y positions,
# and the distance to their cluster tag
class AnchorModel(db.Model):
   __tablename__ = "anchors"
   anchor_id = db.Column(db.Integer, primary_key = True)
   cluster_id = db.Column(db.Integer, db.ForeignKey("clusters.cluster_id", ondelete = "CASCADE"), nullable=False)
   anch_x = db.Column(db.Integer, nullable=False, default = 0)
   anch_y = db.Column(db.Integer, nullable=False, default = 0)
   anchor_distance = db.Column(db.Float, nullable=False, default = 0.0)

   def __repr__(self):
      return f"Anchor(anchor_id = {self.anchor_id}, cluster_id = {self.cluster_id}, anch_x = {self.anch_x}, anch_y = {self.anch_y}, anchor_distance = {self.anchor_distance})"

# Serialize data for a cluster request
clusterFields = {
   'cluster_id': fields.Integer,
   'senior_name': fields.String,
   'senior_x': fields.Integer,
   'senior_y': fields.Integer
}

# Serialize data for a anchor request
anchorFields = {
   'anchor_id': fields.Integer,
   'cluster_id': fields.Integer,
   'anchor_x': fields.Integer,
   'anchor_y': fields.Integer,
   'anchor_distance': fields.Float
}

### API calls for all clusters ###
class Clusters(Resource):
   # Parse user arguments in request to API
   user_args = reqparse.RequestParser()
   user_args.add_argument('senior_name', type=str, required=True, help="Senior name cannot be empty")

   # API call to get all of the clusters
   @marshal_with(clusterFields)
   def get(self):
      clusters = ClusterModel.query.all()
      return clusters
   
   # API call to create a new cluster for senior_name
   @marshal_with(clusterFields)
   def post(self):
      
      args = self.user_args.parse_args()
      cluster = ClusterModel(senior_name=args["senior_name"], 
                             senior_x = 0, senior_y = 0)
      db.session.add(cluster)
      db.session.commit()
      clusters = ClusterModel().query.all()
      return clusters, 201

### API calls for a specific cluster ###
class Cluster(Resource):
   # Parse user arguments in request to API
   user_args = reqparse.RequestParser()
   user_args.add_argument('senior_name', type=str, required=True, help="Senior name cannot be empty")   
   # API call to get a specific cluster
   @marshal_with(clusterFields)
   def get(self, id):
      cluster = ClusterModel.query.filter_by(cluster_id=id).first()
      if not cluster:
         abort(404, "Cluster not found")
      return cluster
   
   # API call to update senior name for a specific cluster
   @marshal_with(clusterFields)
   def patch(self, id):
      args = self.user_args.parse_args()
      cluster = ClusterModel.query.filter_by(cluster_id=id).first()
      if not cluster:
         abort(404, "Cluster not found")
      cluster.senior_name = args["senior_name"]
      db.session.commit()
      return cluster
   
   # API call to delete a specific cluster
   @marshal_with(clusterFields)
   def delete(self, id):
      cluster = ClusterModel.query.filter_by(cluster_id=id).first()
      if not cluster:
         abort(404, "Cluster not found")
      db.session.delete(cluster)
      db.session.commit()
      return ClusterModel.query.all(), 200

# API route for updating clusters
api.add_resource(Clusters, '/api/clusters/')
api.add_resource(Cluster, '/api/clusters/<int:id>')

### API calls for all anchors ###
class Anchors(Resource):
   # Parse user arguments in request to API
   user_args = reqparse.RequestParser()
   user_args.add_argument('cluster_id', type=int, required=True, help="Cluster id cannot be empty")
   user_args.add_argument('anch_x', type=int, required=True, help="Anchor x position cannot be empty")
   user_args.add_argument('anch_y', type=int, required=True, help="Anchor y position cannot be empty")

   # API call to get all of the anchors
   @marshal_with(anchorFields)
   def get(self):
      clusters = ClusterModel.query.all()
      return clusters
   
   # API call to create a new anchor for cluster_id
   @marshal_with(anchorFields)
   def post(self):
      args = self.user_args.parse_args()
      cluster = ClusterModel.query.filter_by(cluster_id=args["cluster_id"]).first()
      if not cluster:
         abort(404, "Cluster not found")
      anchor = AnchorModel(cluster_id=args["cluster_id"], anch_x=args["anch_x"],
                           anch_y=args["anch_y"], anchor_distance = 0)
      db.session.add(anchor)
      db.session.commit()
      anchors = AnchorModel().query.all()
      return anchors, 201
   
### API calls for a specific anchor ###
class Anchor(Resource):
   # Parse user arguments in request to API
   user_args = reqparse.RequestParser()
   user_args.add_argument('anchor_id', type=int, required=True, help="Anchor id cannot be empty")

   # API call to get a specific anchor
   @marshal_with(anchorFields)
   def get(self, id):
      anchor = AnchorModel.query.filter_by(anchor_id=id).first()
      if not anchor:
         abort(404, "Anchor not found")
      return anchor
   
   # API call to update distance for a specific anchor
   @marshal_with(anchorFields)
   def patch(self, id):
      args = self.user_args.parse_args()
      user_args = reqparse.RequestParser()
      user_args.add_argument('anchor_distance', type=float, required=True, help="Anchor distance cannot be empty")
      anchor = AnchorModel.query.filter_by(anchor_id=id).first()
      if not anchor:
         abort(404, "Anchor not found")
      anchor.anchor_distance = args["anchor_distance"]
      """TODO Recalculate senior position on anchor update
      ~
      ~
      ~
      ~
      """
      db.session.commit()
      return anchor
   
   # API call to delete a specific anchor
   @marshal_with(anchorFields)
   def delete(self, id):
      anchor = AnchorModel.query.filter_by(anchor_id=id).first()
      if not anchor:
         abort(404, "Cluster not found")
      db.session.delete(anchor)
      db.session.commit()
      return AnchorModel.query.all(), 200

api.add_resource(Anchors, '/api/anchors/')
api.add_resource(Anchor, '/api/anchor/<id>')

# Home page route
@app.route('/')
def home():
   return '<h1>UWB IPS REST API</h1>'

'''
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         
# Create a socket object
host = socket.gethostname()
network = socket.gethostbyname(host)
# Get local machine name
port = 3306                
# Reserve a port for your service.
s.bind((host, port))        
# Bind to the port
s.listen(0)
# Listening on:
print("listening on:", network, " port: ", port)
# Now wait for client connection.
while True:
   c, addr = s.accept()     
# Establish connection with client.
   print('Got connection from', addr)
   c.send('Thank you for connecting')
   c.close()                
# Output the message and Close the connection
'''   

# Run the app
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=80)