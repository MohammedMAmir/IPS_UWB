#!/usr/bin/python           
# This is server.py file built using the tutorial at https://www.youtube.com/watch?v=z3YMz-Gocmw&ab_channel=DaveGray
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort
import math
from scipy.optimize import minimize            

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
   senior_x = db.Column(db.Numeric(10,2), nullable=False, default = 0)
   senior_y = db.Column(db.Numeric(10,2), nullable=False, default = 0)
   num_anchors = db.Column(db.Integer, nullable=False, default = 0)

   def __repr__(self):
      return f"""Cluster(cluster_id = {self.cluster_id}, senior_name = {self.senior_name}, 
      senior_x = {self.senior_x}, senior_y = {self.senior_y})"""

# the table for all anchors, including which cluster they are associated with, their x and y positions,
# and the distance to their cluster tag
class AnchorModel(db.Model):
   __tablename__ = "anchors"
   anchor_id = db.Column(db.Integer, primary_key = True)
   cluster_id = db.Column(db.Integer, db.ForeignKey("clusters.cluster_id", ondelete = "CASCADE"), nullable=False)
   anch_x = db.Column(db.Numeric(10,2), nullable=False, default = 0)
   anch_y = db.Column(db.Numeric(10,2), nullable=False, default = 0)
   anchor_distance = db.Column(db.Numeric(10,2), nullable=False, default = 0.0)

   def __repr__(self):
      return f"Anchor(anchor_id = {self.anchor_id}, cluster_id = {self.cluster_id}, anch_x = {self.anch_x}, anch_y = {self.anch_y}, anchor_distance = {self.anchor_distance})"

# Mean Square Error
# locations: [ (x1, y1), ... ]
# distances: [ distance1, ... ]
def mse(x, locations, distances):
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = math.dist(x, location)
        mse += math.pow(distance_calculated - distance, 2.0)
    return mse / len(distances)

def update_location(anchor: AnchorModel):
   anchorCluster = anchor.cluster_id
   cluster = ClusterModel.query.filter_by(cluster_id=anchorCluster).first()
   xToUpdate = float(cluster.senior_x)
   yToUpdate = float(cluster.senior_y)
   
   anchorsInCluster = AnchorModel.query.filter_by(cluster_id=anchorCluster).all()
   locations = []
   distances = []
   for anchors in anchorsInCluster:
      locations.append((int(anchors.anch_x), int(anchors.anch_y)))
      distances.append((float(anchors.anchor_distance)))
   
   initial_guess = (xToUpdate, yToUpdate)
   result = minimize(
      mse,                         # The error function
      initial_guess,            # The initial guess
      args=(locations, distances), # Additional parameters for mse
      method='L-BFGS-B',           # The optimisation algorithm
      options={
         'ftol':1e-2,         # Tolerance
         'maxiter': 1e+8      # Maximum iterations
      })
   
   cluster.senior_x = result.x[0]
   cluster.senior_y = result.x[1]
   db.session.commit()
   return result

# Serialize data for a cluster request
clusterFields = {
   'cluster_id': fields.Integer,
   'senior_name': fields.String,
   'senior_x': fields.Float,
   'senior_y': fields.Float,
   'num_anchors': fields.Integer
}

# Serialize data for a anchor request
anchorFields = {
   'anchor_id': fields.Integer,
   'cluster_id': fields.Integer,
   'anch_x': fields.Float,
   'anch_y': fields.Float,
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
                             senior_x = 0, senior_y = 0, num_anchors=0)
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
   user_args.add_argument('anch_x', type=float, required=True, help="Anchor x position cannot be empty")
   user_args.add_argument('anch_y', type=float, required=True, help="Anchor y position cannot be empty")

   # API call to get all of the anchors
   @marshal_with(anchorFields)
   def get(self):
      anchors = AnchorModel.query.all()
      return anchors
   
   # API call to create a new anchor for cluster_id
   @marshal_with(anchorFields)
   def post(self):
      args = self.user_args.parse_args()
      cluster = ClusterModel.query.filter_by(cluster_id=args["cluster_id"]).first()
      if not cluster:
         abort(404, "Cluster not found")
      anchor = AnchorModel(cluster_id=args["cluster_id"], anch_x=args["anch_x"],
                           anch_y=args["anch_y"], anchor_distance = 0)
      cluster.num_anchors += 1
      db.session.add(anchor)
      db.session.commit()
      anchors = AnchorModel().query.all()
      return anchors, 201
   
### API calls for a specific anchor ###
class Anchor(Resource):
   # Parse user arguments in request to API
   user_args = reqparse.RequestParser()
   user_args.add_argument('anchor_distance', type=float, required=True, help="Anchor distance cannot be empty")
   user_args.add_argument('anch_x', type=int, required=False, help="Anchor distance cannot be empty")
   user_args.add_argument('anch_y', type=int, required=False, help="Anchor distance cannot be empty")
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
      anchor = AnchorModel.query.filter_by(anchor_id=id).first()
      if not anchor:
         abort(404, "Anchor not found")
      anchor.anchor_distance = args["anchor_distance"]
      if args["anch_x"]:
         anchor.anch_x = args["anch_x"]
      if args["anch_y"]:
         anchor.anch_y = args["anch_y"]

      result = update_location(anchor)
      db.session.commit()
      return anchor, 200
   
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
@app.route('/', methods=['GET', 'POST'])
def home():
   clusters = ClusterModel.query.all()
   anchors = AnchorModel.query.all()
   print(clusters)
   return render_template('index.html', clusters=clusters, anchors=anchors, page="home")

@app.route('/createcluster', methods=['GET', 'POST'])
def createcluster():
   return render_template('createcluster.html', page="cluster")

@app.route('/createanchor', methods=['GET', 'POST'])
def createanchor():
   return render_template('createanchor.html', page="anchor")
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
   app.run(host='0.0.0.0', port=81, debug=True)