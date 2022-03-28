import enum
from pydoc import cli
import socket
import time
from List_Manager import ListManager


LMananger = ListManager()

PORT = 9999
HOST = "localhost"

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

# connection to hostname on the port.
client.connect((HOST, PORT))      
name = input("What is your client name: ")
client.send(bytes(name, 'utf-8'))
# Receive no more than 1024 bytes
tm = client.recv(1024)                                     

print("Connected to the server at %s" % tm.decode('ascii'))
client_connected = True
LMananger.display_valid_commands()
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
    print(result)
        
  if result.lower() == "exit":
    print("Client Quits, Goodbye.")
    break
client.close()


