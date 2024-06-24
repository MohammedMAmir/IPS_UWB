#!/usr/bin/python           
# This is server.py file

import socket               
# Import socket module

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