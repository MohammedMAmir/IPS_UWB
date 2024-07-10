# Indoor Positioning Ultra-Wide Band Server (IPS UWB)

## Installations and Setup ###

### Installations ###

The following requirements must be satisfied to be able to run the IPS UWB server. 
- Git: Download and install git on your device from the following link https://git-scm.com/downloads
  
  ![alt text](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPteWfILDHmk0RbbZao7PgFtDvdueIFX0LuQ&s)
  
- Python: You must also have python installed. Please consult this tutorial to install Python and add it to the environment variables on your device https://www.digitalocean.com/community/tutorials/install-python-windows-10
  
  ![alt text](https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStmzRIlwA0USenF0Ad9inIYjcd-hfD76p8JA&s)
  

### Setup ###

Once you have git and python installed, you may clone this repository:
- Open a terminal window on your device and type "git clone https://github.com/MohammedMAmir/IPS_UWB.git"
- The project folders should be cloned onto your device
- Type "cd IPS_UWB" to navigate to the project folder

Now you can setup all the dependencies for the project:
- In your terminal window, inside the IPS_UWB folder, type "python3  pip install virtualenv".
- Once the installation is finished, type "python3 -m venv .venv". This will create a virtual environment folder that lets you import all the dependencies of the project without overriding dependency versions already installed on your device.
- To activate the virtual environment use the command "source .venv/Scripts/activate" in your terminal window. You will need to do this everytime you open a new terminal and want to run the server.
- Navigate into the "ips_app" folder using the command "cd ips_app" in the terminal window
- Finally, enter the command "python3 -m install -r requirements.txt" to install all of the modules used by the project
- Wait for all of the modules to install and if an error occurs or a module is missing, just install it manually using the command "python3 -m pip install [missing module]" (where missing module is replaced by whatever module triggered the error and is missing)

Now you're ready to start the server!

## Usage ##
### Running the Server ###

Running the server for this project is as simple as running the server script
- Open a terminal window and navigate to the ips_app folder using "cd /path/to/folder/IPS_UWB"
- Start up your virtual environment using "source .venv/Scripts/activate" 
- Once the virtual environment is running, navigate into the ips_app folder using "cd ips_app"
- Once in the ips_app folder, use the command "python3 -m server" to start the server
- You should get a message that the server is running on 127.0.0.1:81. You can now type https://127.0.0.1:81 into any browser to view the server responses

### Using the Database ###
The database currently contains two tables:

#### Tags: ####

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
              
#### Anchors: ####

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

### Calling the API ###

The api for the project can be used to query and update the database. It is broken down into 4 parts. Although all of the functionalities of the API can be accessed through website dashboard, they can also be accessed using HTTP GET/POST requests and therefore, from anchors and tags. The API is broken down as follows:

- Tags (available at the url: https://127.0.0.1:81/api/tags) [https://127.0.0.1:81 can later be replaced with whatever url the server is hosted at]:
  - GET:
    - Request takes no parameters and returns a list of all of the tags currently stored in the database
  - POST:
    - Request takes a post request with the following JSON message body:
       - {"senior_name": "[some senior name]"}
    - The corresponding tag will be created in the database with a unique tag ID and initial senior x and y position of (0, 0)
    - The request will return a list of all the tags in the database
   
- Anchors (available at the url: https://127.0.0.1:81/api/anchors) [https://127.0.0.1:81 can later be replaced with whatever url the server is hosted at]:
  - GET:
    - Request takes no parameters and returns a list of all of the anchors currently stored in the database
  - POST: 
    - Request takes a post request with the following JSON message body:
        - {"tag_id": "[some tag id]", "anch_x": "[the anchor x position]", "anch_y": "[the anchor y position]"}
    - The corresponding anchor attached to the specified tag will be created in the database with a unique anchor Id and anchor x and y positions specified


