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
# the table for a tag of anchors and tags
class tagModel(db.Model):
   __tablename__ = "tags"
   # Unique id that identifies each tag, autoincrements
   tag_id = db.Column(db.Integer, primary_key=True)
   
   # The senior this tag identifies
   senior_name = db.Column(db.String(80), nullable=False)
   
   # The senior's x and y positions, updated every time an anchor updates it's distance
   senior_x = db.Column(db.Numeric(10,2), nullable=False, default = 0)
   senior_y = db.Column(db.Numeric(10,2), nullable=False, default = 0)
   
   # The number of anchors associated with this tag
   num_anchors = db.Column(db.Integer, nullable=False, default = 0)

   def __repr__(self):
      return f"""tag(tag_id = {self.tag_id}, senior_name = {self.senior_name}, 
      senior_x = {self.senior_x}, senior_y = {self.senior_y})"""

# the table for all anchors, including which tag they are associated with, their x and y positions,
# and the distance to their tag tag
class AnchorModel(db.Model):
   __tablename__ = "anchors"
   # Unique id that identifies each tag, autoincrements
   anchor_id = db.Column(db.Integer, primary_key = True)

   # The tag this anchor is associated with
   tag_id = db.Column(db.Integer, db.ForeignKey("tags.tag_id", ondelete = "CASCADE"), nullable=False)

   # The anchor's fixed x and y positions
   anch_x = db.Column(db.Numeric(10,2), nullable=False, default = 0)
   anch_y = db.Column(db.Numeric(10,2), nullable=False, default = 0)

   # The distance between the anchor and it's tag, updated by anchor
   anchor_distance = db.Column(db.Numeric(10,2), nullable=False, default = 0.0)

   def __repr__(self):
      return f"Anchor(anchor_id = {self.anchor_id}, tag_id = {self.tag_id}, anch_x = {self.anch_x}, anch_y = {self.anch_y}, anchor_distance = {self.anchor_distance})"

# Mean Square Error
# locations: [ (x1, y1), ... ]
# distances: [ distance1, ... ]
def mse(x, locations, distances):
    mse = 0.0
    for location, distance in zip(locations, distances):
        distance_calculated = math.dist(x, location)
        mse += math.pow(distance_calculated - distance, 2.0)
    return mse / len(distances)

# Used to calculate location of tag using anchor distances as specified by:
# https://www.alanzucconi.com/2017/03/13/positioning-and-trilateration/
def update_location(anchor: AnchorModel):
   anchortag = anchor.tag_id
   tag = tagModel.query.filter_by(tag_id=anchortag).first()
   xToUpdate = float(tag.senior_x)
   yToUpdate = float(tag.senior_y)
   
   anchorsIntag = AnchorModel.query.filter_by(tag_id=anchortag).all()
   locations = []
   distances = []
   for anchors in anchorsIntag:
      locations.append((int(anchors.anch_x), int(anchors.anch_y)))
      distances.append((float(anchors.anchor_distance)))
   
   initial_guess = (xToUpdate, yToUpdate)
   result = minimize(
      mse,                         # The error function
      initial_guess,            # The initial guess
      args=(locations, distances), # Additional parameters for mse
      method='BFGS',           # The optimisation algorithm
      options={
         'ftol':1e-4,         # Tolerance
         'maxiter': 1e+8      # Maximum iterations
      })
   
   tag.senior_x = result.x[0]
   tag.senior_y = result.x[1]
   db.session.commit()
   return result

# Serialize data for a tag request
tagFields = {
   'tag_id': fields.Integer,
   'senior_name': fields.String,
   'senior_x': fields.Float,
   'senior_y': fields.Float,
   'num_anchors': fields.Integer
}

# Serialize data for a anchor request
anchorFields = {
   'anchor_id': fields.Integer,
   'tag_id': fields.Integer,
   'anch_x': fields.Float,
   'anch_y': fields.Float,
   'anchor_distance': fields.Float
}



### API calls for all tags ###
class tags(Resource):
   # Parse user arguments in request to API
   user_args = reqparse.RequestParser()
   user_args.add_argument('senior_name', type=str, required=True, help="Senior name cannot be empty")

   # API call to get all of the tags
   @marshal_with(tagFields)
   def get(self):
      tags = tagModel.query.all()
      return tags
   
   # API call to create a new tag for senior_name
   @marshal_with(tagFields)
   def post(self):
      
      args = self.user_args.parse_args()
      tag = tagModel(senior_name=args["senior_name"], 
                             senior_x = 0, senior_y = 0, num_anchors=0)
      db.session.add(tag)
      db.session.commit()
      tags = tagModel().query.all()
      return tags, 201


### API calls for a specific tag ###
class tag(Resource):
   # Parse user arguments in request to API
   user_args = reqparse.RequestParser()
   user_args.add_argument('senior_name', type=str, required=True, help="Senior name cannot be empty")   
   # API call to get a specific tag
   @marshal_with(tagFields)
   def get(self, id):
      tag = tagModel.query.filter_by(tag_id=id).first()
      if not tag:
         abort(404, "tag not found")
      return tag
   
   # API call to update senior name for a specific tag
   @marshal_with(tagFields)
   def patch(self, id):
      args = self.user_args.parse_args()
      tag = tagModel.query.filter_by(tag_id=id).first()
      if not tag:
         abort(404, "tag not found")
      tag.senior_name = args["senior_name"]
      db.session.commit()
      return tag
   
   # API call to delete a specific tag
   @marshal_with(tagFields)
   def delete(self, id):
      tag = tagModel.query.filter_by(tag_id=id).first()
      if not tag:
         abort(404, "tag not found")
      db.session.delete(tag)
      db.session.commit()
      return tagModel.query.all(), 200

# API route for updating tags
api.add_resource(tags, '/api/tags/')
api.add_resource(tag, '/api/tags/<int:id>')



### API calls for all anchors ###
class Anchors(Resource):
   # Parse user arguments in request to API
   user_args = reqparse.RequestParser()
   user_args.add_argument('tag_id', type=int, required=True, help="tag id cannot be empty")
   user_args.add_argument('anch_x', type=float, required=True, help="Anchor x position cannot be empty")
   user_args.add_argument('anch_y', type=float, required=True, help="Anchor y position cannot be empty")

   # API call to get all of the anchors
   @marshal_with(anchorFields)
   def get(self):
      anchors = AnchorModel.query.all()
      return anchors
   
   # API call to create a new anchor for tag_id
   @marshal_with(anchorFields)
   def post(self):
      args = self.user_args.parse_args()
      tag = tagModel.query.filter_by(tag_id=args["tag_id"]).first()
      if not tag:
         abort(404, "tag not found")
      anchor = AnchorModel(tag_id=args["tag_id"], anch_x=args["anch_x"],
                           anch_y=args["anch_y"], anchor_distance = 0)
      tag.num_anchors += 1
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
         abort(404, "tag not found")
      db.session.delete(anchor)
      db.session.commit()
      return AnchorModel.query.all(), 200

api.add_resource(Anchors, '/api/anchors/')
api.add_resource(Anchor, '/api/anchor/<id>')



# Route to Home Page
@app.route('/', methods=['GET'])
def home():
   tags = tagModel.query.all()
   anchors = AnchorModel.query.all()
   print(tags)
   # Send all the tags, all of the anchors, and the Home Page
   return render_template('index.html', tags=tags, anchors=anchors, page="home")

# Route to Create a Tag Page
@app.route('/createtag', methods=['GET', 'POST'])
def createtag():
   # Send the create a tag page
   return render_template('createtag.html', page="tag")

# Route to Create an Anchor Page
@app.route('/createanchor', methods=['GET', 'POST'])
def createanchor():
   # Send the create an anchor page and all of the current tags that exist in the db
   tags = tagModel.query.all()
   return render_template('createanchor.html', tags=tags, page="anchor")

# Route to Visualize a Specific Tag
@app.route('/tag/<id>', methods=['GET'])
def viewtag(id):
   tag = tagModel.query.filter_by(tag_id=id).first()
   anchors= AnchorModel.query.filter_by(tag_id=id).all()
   # Send the tag page, the current tag, and all of the anchors for that tag
   return render_template('tag.html', tag=tag, anchors=anchors)


# Run the app
if __name__ == '__main__':
   app.run(host='0.0.0.0', port=81, debug=True)