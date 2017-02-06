#!/usr/bin/python

import socket
import getopt
import sys
import string
import threading
#ex
#/proxy -raw 2001 www.ucalgary.ca 80
SRC_PORT = 0
DST_PORT = 0
SRC_HOST = ''
DST_HOST = ''
LOG_MODE = 0  #log print mode, raw is default

def start():

  global SRC_PORT
  global DST_PORT
  global SRC_HOST
  global DST_HOST
  global LOG_MODE

  SRC_HOST = '127.0.0.1' #localhost
  arg_length = len(sys.argv)

  if arg_length == 5:
    log_command = str(sys.argv[1])
    #create function to set the log mode based on input
    LOG_MODE = 0
    SRC_PORT = sys.argv[2]
    DST_HOST = str(sys.argv[3])
    DST_PORT  = sys.argv[4]
    server_listen()
    
  else:
    print("wrong number of program arguments")


#this function waits for clients to connect to the proxy
    #start a new proxy listener thread for each client that connects
    #to the server
def server_listen():
  
  clients_connected = 0
  server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
  server_sock.bind((SRC_HOST,SRC_PORT))
  server_sock.listen(5)
  print("Waiting for socket connection at " + SRC_HOST + ":" + str(SRC_PORT))
  
  while True:
    clientSock, addr = server.accept()
    clientSock.settimeout(60) #times out after 60 seconds
    clients_connected += 1 #increase counter
    print("Client unknowingly connected to the 666 proxy")
    # need a print statement to show the clients IP address

    threading.Thread(target = proxy666Listener,args = (clientSock,addr))
    

def proxy666Listener(clientSock,addr):
  buf_size = 4096
  while True:
    try:
      data = clientSock.recv(buff_size)
      if data:
        response = data
        clientSock.send(response)
      else:
        print("Client disconnected")
    except:
      print("Error Exception")
      clientSock.close()
  

if __name__ == "__main__":
  start()

  




