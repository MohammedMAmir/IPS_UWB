#!/usr/bin/python           
# This is server.py file
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api, reqparse, fields, marshal_with, abort

# Import socket module
import socket               

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
api = Api(app)

# Database tables
class ClusterModel(db.Model):
   __tablename__ = "clusters"
   cluster_id = db.Column(db.Integer, primary_key=True)
   senior_name = db.Column(db.String(80), nullable=False)
   senior_x = db.Column(db.Integer, nullable=False, default = 0)
   senior_y = db.Column(db.Integer, nullable=False, default = 0)

   def __repr__(self):
      return f"Cluster(cluster_id = {self.cluster_id}, senior_name = {self.senior_name})"

class Anchors(db.Model):
   __tablename__ = "anchors"
   anchor_id = db.Column(db.Integer, primary_key = True)
   cluster_id = db.Column(db.Integer, db.ForeignKey("clusters.cluster_id", ondelete = "CASCADE"), nullable=False)

   def __repr__(self):
      return f"Cluster(anchor = {self.anchor_id}, cluster = {self.cluster_id})"

# Parse user arguments in request to API
user_args = reqparse.RequestParser()
user_args.add_argument('senior_name', type=str, required=True, help="Senior name cannot be empty")

# Serialize data
clusterFields = {
   'cluster_id': fields.Integer,
   'senior_name': fields.String,
   'senior_x': fields.Integer,
   'senior_y': fields.Integer
}

# API calls to get all of the clusters, create new clusters, and update clusters
class Clusters(Resource):
   # API call to get all of the clusters
   @marshal_with(clusterFields)
   def get(self):
      clusters = ClusterModel.query.all()
      return clusters
   
   # API call to create a new cluster for senior_name
   @marshal_with(clusterFields)
   def post(self):
      args = user_args.parse_args()
      cluster = ClusterModel(senior_name=args["senior_name"], 
                             senior_x = 0, senior_y = 0)
      db.session.add(cluster)
      db.session.commit()
      clusters = ClusterModel().query.all()
      return clusters, 201

class Cluster(Resource):   
   # API call to get a specific cluster
   @marshal_with(clusterFields)
   def get(self, id):
      cluster = ClusterModel.query.filter_by(cluster_id=id).first()
      if not cluster:
         abort(404, "Cluster not found")
      return cluster

# API route for updating clusters
api.add_resource(Clusters, '/api/clusters/')
api.add_resource(Cluster, '/api/clusters/<int:id>')

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
   app.run(debug=True)