# Indoor Positioning Ultra-Wide Band Server (IPS UWB)

## Requirements ##

The following requirements must be satisfied to be able to run the IPS UWB server. 
- Git: Download and install git on your device from the following link https://git-scm.com/downloads
  
  ![alt text](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPteWfILDHmk0RbbZao7PgFtDvdueIFX0LuQ&s)
  
- Python: You must also have python installed. Please consult this tutorial to install Python and add it to the environment variables on your device https://www.digitalocean.com/community/tutorials/install-python-windows-10
  
  ![alt text](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStmzRIlwA0USenF0Ad9inIYjcd-hfD76p8JA&s)
  
---  

## Installation & Setup ##

Once you have git and python installed, you may clone this repository:
- Open a terminal window on your device and use 
```bash
git clone https://github.com/MohammedMAmir/IPS_UWB.git"
```
- The project folders should be cloned onto your device
- Use the following command to navigate to the project folder
```bash
cd IPS_UWB
```

Now you can setup all the dependencies for the project:
- In your terminal window, inside the IPS_UWB folder, enter
```bash
python3  pip install virtualenv
```
- Once the installation is finished, use
```bash
python3 -m venv .venv
```
This will create a virtual environment folder that lets you import all the dependencies of the project without overriding dependency versions already installed on your device.
- To activate the virtual environment use the command
```bash
source .venv/Scripts/activate
```
in your terminal window. You will need to do this everytime you open a new terminal and want to run the server.
- Navigate into the "ips_app" folder using the command
```bash
cd ips_app
```
in the terminal window
- Finally, install all of the modules used by the project by entering the command
```bash
python3 -m install -r requirements.txt
```
- Wait for all of the modules to install
    - if an error occurs or a module is missing, just install it manually using the command
      ```bash
      python3 -m pip install [missing module]
      ```
      (where missing module is replaced by whatever module triggered the error and is missing)

Now you're ready to start the server!

--- 

## Running the Server ##

Running the server for this project is as simple as running the server script
- Open a terminal window and navigate to the ips_app folder using
  ```bash
  cd /path/to/folder/IPS_UWB
  ```
- Start up your virtual environment using
  ```bash
  source .venv/Scripts/activate
  ``` 
- Once the virtual environment is running, navigate into the ips_app folder using
  ```bash
  cd ips_app
  ```
- Once in the ips_app folder, to start the server, use the command
  ```bash
  python3 -m server
  ```
- You should get a message that the server is running on 127.0.0.1:81. You can now type https://127.0.0.1:81 into any browser to view the server responses

--- 

## Using the Database ##
The database currently contains two tables:

| tag_id | senior_name | senior_x | senior_ y | num_anchors |
|--------|-------------|----------|-----------|-------------|
|        |             |          |           |             |

| anchor_id | tag_id | anch_x | anch_ y | anchor_distance |
|-----------|--------|--------|---------|-----------------|
|           |        |        |         |                 |
### Tags: ###

Each tag has 5 fields:
  1) tag_id (integer)
      * A unique id that identifies each tag
      * Autoincrements anytime a new tag is added
            
  2) senior_name (string)
      * The senior this tag identifies
            
  3) senior_x (float)
      * The current x position of the tag
            
  4) senior_y
      * The current y position of the tag
            
  5) num_anchors
      * The number of anchors associate with this tag
              
### Anchors: ###

Each anchor has 5 fields:
  1) anchor_id (integer)
      * A unique id that identifies each anchor
      * Autoincrements anytime a new anchor is added
            
  2) tag_id (integer):
      * The tag that this anchor is associated with
      * There must be a valid tag in the tag table for this to reference
            
  3) anch_x (float):
      * The fixed x position of the anchor in its coordinate space
            
  4) anch_y (float):
      * The fixed y position of the anchor in its coordiante space
  
  5) anchor_distance (float):
      * The distance from the anchor to it's corresponding tag
      * Updated by the anchors using a PATCH request

--- 

## Calling the API ##

The api for the project can be used to query and update the database. It is broken down into 4 parts. Although all of the functionalities of the API can be accessed through website dashboard, they can also be accessed using HTTP GET/POST requests and therefore, from anchors and tags. The API is broken down as follows:

- Tags (available at the url: https://127.0.0.1:81/api/tags)
  * Used to get information on all tags stored in the database
  * [https://127.0.0.1:81 can later be replaced with whatever url the server is hosted at]
    
  * Endpoints:
      - GET:
         - Request takes no parameters and returns a list of all of the tags currently stored in the database
      - POST:
         - Request takes a post request with the following JSON message body:
          ```JSON
          {"senior_name": "[some senior name]"}
          ```
         - The corresponding tag will be created in the database with a unique tag ID and initial senior x and y position of (0, 0)
         - The request will return a list of all the tags in the database
   
- Anchors (available at the url: https://127.0.0.1:81/api/anchors)
    * Used to get information on all anchors stored in the database
    * [https://127.0.0.1:81 can later be replaced with whatever url the server is hosted at]
    * Endpoints:
        - GET:
            - Request takes no parameters and returns a list of all of the anchors currently stored in the database
        - POST: 
            - Request takes a post request with the following JSON message body:
           ```JSON
           {"tag_id": "[some tag id]", "anch_x": "[the anchor x position]", "anch_y": "[the anchor y position]"}
           ```
            - The corresponding anchor attached to the specified tag will be created in the database with a unique anchor ID and anchor x and y positions specified
- Tag (available at the url: https://127.0.0.1:81/api/tag/<id>)
    * Used to get, update, and delete information about tag with tag_id = id
    * [https://127.0.0.1:81 can later be replaced with whatever url the server is hosted at]
    * Endpoints:
        - GET:
            - Request takes no parameters and returns the tag in the url if it is stored in the database
        - PATCH:
            - Request makes a patch request with the following JSON message body:
              ```JSON
              {"senior_name": "[some senior name]"}
              ```
            - The senior name of the tag in the url will then be updated to instead be registered to the senior name specificed in the request
        - DELETE:
            - Request takes no parameters and deletes the tag that in the url if it is stored in the database
            - If the tag has corresponding anchors attached to it, they will also be deleted from the database
- Anchor (available at the url: https://127.0.0.1:81/api/anchor/<id>)
    * Used to get, update, and delete information about tag with anchor_id = id
    * [https://127.0.0.1:81 can later be replaced with whatever url the server is hosted at]
    * Endpoints
        - GET:
            - Request takes no parameters and returns the anchor in the url if it is stored in the database 
        - PATCH:
            - Request makes a patch request with the following JSON message body:
               Request makes a patch request with the following JSON message body:
              ```JSON
              {"anchor_distance": "[the anchor's updated distance from itself to it's tag]"} OR {"anchor_distance:" "[the anchor's updated distance from itself to it's tag], "}
              ```
        - DELETE:
            - Request takes no parameters and deletes the anchor with the anchor_id specified in the url if it is stored in the database

---
## Positioning Calculation ##
The positioning algorithm is called everytime that an anchor makes a PATCH request to the database. Specifically, everytime an anchor updates the distance to its associated anchor, the following two functions are called by the server to calcualate the new position of the tag:
```Python
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
      method='L-BFGS-B',           # The optimisation algorithm
      options={
         'ftol':1e-2,         # Tolerance
         'maxiter': 1e+8      # Maximum iterations
      })
   
   tag.senior_x = result.x[0]
   tag.senior_y = result.x[1]
   db.session.commit()
   return result
```



