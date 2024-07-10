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

### Calling the API ###

The api for the project can be used to query and update the database. It is broken down into 4 parts. Although all of the functionalities of the API can be accessed through website dashboard, they can also be accessed using HTTP GET/POST requests and therefore, from anchors and tags. The API is broken down as follows:



