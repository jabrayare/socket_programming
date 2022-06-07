"""
@author: Jibril Mohamed
"""
import socket
import time
from List_Manager import ListManager
from configparser import ConfigParser
import ast

# Config file configuration
config = ConfigParser()
configFile = 'config.ini'
config.read(configFile)

HOST = ast.literal_eval(config.get('DEFAULT', 'HOST'))
PORT = int(config['DEFAULT']['PORT'])

# This class maintains each client's list.
LMananger = ListManager()

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# connection to hostname on the port.
client.connect((HOST, PORT))      
name = input("What is your client name: ")
client.send(bytes(name, 'utf-8'))
# Receive no more than 1024 bytes
tm = client.recv(1024)                                     

print(f"`{name}` Connected to the server at %s" % tm.decode('ascii'))
LMananger.display_valid_commands()

client_connected = True
while client_connected:
  command = input("command: ")
  list_cmd = command.split(',')
  client.send(bytes(command, 'utf-8'))
  
  result = client.recv(1024).decode()
  if result.lower() == 'invalid':
    print("Invalid Command recieved!")
    LMananger.display_valid_commands()
    
  elif result.lower() == 'helpcommand':
    print("Help Command recieved!")
    LMananger.display_valid_commands()
     
  if list_cmd[0].lower() == 'list':
    if result == "empty":
      print("The list is Empty.")
    else:
      list_items = result.split(',')
      for i, item in enumerate(list_items):
        print(f"{i}: {item}")
  
  if list_cmd[0] == "add" or list_cmd[0] == "delete" or list_cmd[0] == "replace":
    if result.lower() != 'invalid':
      print(result)
        
  if result.lower() == "exit":
    print(f"`{name}` Quits, Goodbye.")
    break
client.close()


