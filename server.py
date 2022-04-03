import socket
import time
from List_Manager import ListManager
import threading
import logging
from configparser import ConfigParser
import ast


config = ConfigParser()
configFile = 'config.ini'
config.read(configFile)

"""Time req/res Info"""

# Logging configuration
logging.basicConfig(filename="serverLogs.log", format='%(asctime)s %(message)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# List of valid commands
valid_list_commands = ["add", "list", "delete", "replace", "exit", "help" ]
active_threads = []

def client_connection(clientsocket,addr, myList):
  """
  Handles client connections
  arguments:
    clientsocket:
    addr:
    myList: 
  
  """
  client_name = clientsocket.recv(1024).decode()
  currentTime = time.ctime(time.time()) + "\r\n"
  clientsocket.send(currentTime.encode('ascii'))
  print(f"Got a connection from {str(addr)}, `{client_name}` on {currentTime}")
  connected = True
  while connected:
    command = clientsocket.recv(1024).decode()
    list_cmd = command.split(',')
    print(f"Recieved command is: {list_cmd}")
    
    if list_cmd[0] not in valid_list_commands:
      print(f"Invalid Command detected! [`{list_cmd[0]}`]")
      time.sleep(2)
      clientsocket.send(bytes("invalid", 'utf-8'))
    
    if list_cmd[0].lower() == "exit":
      print("Server Quits, Good Bye.")
      clientsocket.send(bytes("exit", 'utf-8'))
      break
    
    if list_cmd[0].lower() == "help":
      print(f"Help Command detected! [`{list_cmd[0]}`]")
      time.sleep(2)
      clientsocket.send(bytes("helpCommand", 'utf-8'))
    
    if list_cmd[0].lower() == "add":
      try:
        myList.add_new_item(list_cmd[1])
        clientsocket.send(bytes("Item added successfully", 'utf-8'))
      except:
        print(f"Something went wrong {list_cmd}")
        clientsocket.send(bytes("error", 'utf-8'))
        
    elif list_cmd[0].lower() == "list":
      try:
        list_str = ",".join(myList.display_all_items())
        if len(list_str) == 0:
          clientsocket.send(bytes("empty", 'utf-8'))
        else:
          clientsocket.send(bytes(list_str, 'utf-8'))
      except:
        print(f"Something went wrong {list_cmd}")
    
    elif list_cmd[0].lower() == "delete":
      try:
        myList.delete_item(int(list_cmd[1]))
        clientsocket.send(bytes("Item Deleted successfully", 'utf-8'))
      except:
        print(f"Something went wrong {list_cmd}")
        index = int(list_cmd[1])
        if index < 0 or index >= myList.count():
          clientsocket.send(bytes("Index out of range. You can't delete item.", "utf-8"))
        else:
          clientsocket.send(bytes("error", 'utf-8'))
    
    elif list_cmd[0].lower() == "replace":
      try:
        myList.replace_item(int(list_cmd[1]), list_cmd[2])
        clientsocket.send(bytes("Item Replaced successfully", 'utf-8'))
      except:
        print(f"Something went wrong {list_cmd}")
        index = int(list_cmd[1])
        if index < 0 or index >= myList.count():
          clientsocket.send(bytes("Index out of range. You can't replace item.", "utf-8"))
        else:
          clientsocket.send(bytes("error", 'utf-8'))
  clientsocket.close()

# server setup.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = ast.literal_eval(config.get('DEFAULT', 'HOST'))
PORT = int(config['DEFAULT']['PORT'])
server.bind((HOST, PORT))
 
# client_connection(clientsocket, addr)
while True:
  server.listen(5)
  logger.info(f"Waiting for connection on {(HOST, PORT)}...")
  # logger.info("Waiting for connection...")
  clientsocket,addr = server.accept() 
  myList = ListManager()
  thread = threading.Thread(target=client_connection, args=(clientsocket, addr, myList))  
  thread.start() 
  active_threads.append(thread)
  active_connections = threading.activeCount()-1
  if active_connections <= 0:
    break
  print(f"Active connections: {active_connections}")

for t in active_threads:
  t.join()
print("No more active connections!")
server.close()   
