"""
@author: Jibril Mohamed
"""
import socket
import time
from List_Manager import ListManager
import threading
import logging
from configparser import ConfigParser
import ast

# Config file configuration
config = ConfigParser()
configFile = 'config.ini'
config.read(configFile)

# Logging configuration
logging.basicConfig(filename="serverLogs.log", format='%(date)s | %(status)s |  %(levelname)s | %(message)s | %(res)s', filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

# List of valid commands
valid_list_commands = ["add", "list", "delete", "replace", "exit", "help" ]

def client_connection(clientsocket,addr, myList):
  client_name = clientsocket.recv(1024).decode()
  currentTime = time.ctime(time.time()) + "\r\n"
  clientsocket.send(currentTime.encode('ascii'))
  
  logger.info(f"Got a connection from `{client_name}` on {addr}", extra={'date': currentTime.strip(), 'status': 'RESPONSE', 'res': 'SENT'})
  
  connected = True
  while connected:
    currentTime = time.ctime(time.time())
    command = clientsocket.recv(1024).decode()
    list_cmd = command.split(',')

    logger.info(f"{client_name}: Recieved command is {list_cmd[0]}", extra={'date': currentTime, 'status': 'REQUEST', 'res': 'RECIEVED'})
    
    if list_cmd[0] not in valid_list_commands:
      time.sleep(1)
      clientsocket.send(bytes("invalid", 'utf-8'))
      
      logger.error(f"{client_name}: Invalid Command detected! [`{list_cmd[0]}`]", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'RECIEVED'})
    
    if list_cmd[0].lower() == "exit":
      clientsocket.send(bytes("exit", 'utf-8'))
      logger.warning(f"{client_name}: Quits, Good Bye.", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
      break
    
    if list_cmd[0].lower() == "help":
      time.sleep(1)
      clientsocket.send(bytes("helpCommand", 'utf-8'))
      
      logger.info(f"{client_name}: Help Command detected! [`{list_cmd[0]}`]", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
    
    if list_cmd[0].lower() == "add":
      try:
        myList.add_new_item(list_cmd[1])
        clientsocket.send(bytes("Item added successfully", 'utf-8'))
        logger.info(f"{client_name}: added Item successfully", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
      except:
        clientsocket.send(bytes("invalid", 'utf-8'))
        logger.error(f"{client_name}: adding Item failed", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
        
    elif list_cmd[0].lower() == "list":
        list_str = ",".join(myList.display_all_items())
        if len(list_str) == 0:
          clientsocket.send(bytes("empty", 'utf-8'))
          logger.info(f"{client_name}: The list is empty", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
        else:
          clientsocket.send(bytes(list_str, 'utf-8'))
    
    elif list_cmd[0].lower() == "delete":
      try:
        myList.delete_item(int(list_cmd[1]))
        clientsocket.send(bytes("Item Deleted successfully", 'utf-8'))
        logger.info(f"{client_name}: deleted Item successfully", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
      except:
        if len(list_cmd) > 1 and not list_cmd[1].strip().isdigit():
          clientsocket.send(bytes("invalid", 'utf-8'))
          logger.error(f"{client_name}: deleting Item failed", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
          continue
        
        if len(list_cmd) >= 2:
          index = int(list_cmd[1])
          if index < 0 or index >= myList.count():
            clientsocket.send(bytes("Index out of range. You can't delete item.", "utf-8"))
            logger.warning(f"{client_name}: Index out of range. You can't delete item.", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
        else:
          clientsocket.send(bytes("invalid", 'utf-8'))
          logger.error(f"{client_name}: deleting Item failed", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
    
    elif list_cmd[0].lower() == "replace":
      try:
        if len(list_cmd) < 3 or len(list_cmd) > 3:
          raise Exception
        myList.replace_item(int(list_cmd[1]), list_cmd[2])
        clientsocket.send(bytes("Item Replaced successfully", 'utf-8'))
        logger.info(f"{client_name}: replaced item successfully", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
      except:
        if len(list_cmd) > 1 and not list_cmd[1].strip().isdigit():
          clientsocket.send(bytes("invalid", 'utf-8'))
          logger.error(f"{client_name}: replacing Item failed", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
          continue
        
        if len(list_cmd) >= 2:
          index = int(list_cmd[1])
          if index < 0 or index >= myList.count():
            clientsocket.send(bytes("Index out of range. You can't replace item.", "utf-8"))
            logger.warning(f"{client_name}: Index out of range. You can't replace item.", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
        else:
          clientsocket.send(bytes("invalid", 'utf-8'))
          logger.error(f"{client_name}: replacing Item failed", extra={'date': currentTime, 'status': 'RESPONSE', 'res': 'SENT'})
          
  clientsocket.close()

# server setup.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = ast.literal_eval(config.get('DEFAULT', 'HOST'))
PORT = int(config['DEFAULT']['PORT'])
server.bind((HOST, PORT))
 
currentTime = time.ctime(time.time())
logger.info(f"Waiting for connection on {(HOST, PORT)}...", extra={'date': currentTime, 'status': 'RESPONSE', 'res': ''})

while True:
  server.listen()
  currentTime = time.ctime(time.time())
  clientsocket,addr = server.accept() 
  myList = ListManager()
  thread = threading.Thread(target=client_connection, args=(clientsocket, addr, myList))  
  thread.start() 
  active_connections = threading.activeCount()-1
  logger.info(f"Active connections: {active_connections}", extra={'date': currentTime, 'status': 'RESPONSE', 'res': ''})

server.close()   
