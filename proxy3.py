#!/usr/bin/python3

# HOW TO USE
# 1. Launch server
#    $python3 proxy3.py -raw <port> www.google.ca 80 
#    OR $python3 proxy3.py <port> www.google.ca 80
# 2.Open firefox setting -> advanced -> network ->settings ->set manual proxy:
#   <port from above>, server: localhost
# now all client requests are relayed and logged through this proxy server
# can handle TCP requests such as: http, netcat, and ssh.

import socket
import getopt
import sys
import string
from threading import Thread

PROXY_PORT = 0
DST_PORT = 0
PROXY_HOST = ''
DST_HOST = ''
LOG_MODE = 0

def start():

  global PROXY_PORT
  global DST_PORT
  global PROXY_HOST
  global DST_HOST
  global LOG_MODE

  PROXY_HOST = 'localhost' #server_host

  if len(sys.argv) == 5 or len(sys.argv) == 4:
    if len(sys.argv) == 5:
      log_command = str(sys.argv[1])
      #set Log mode function here   
      PROXY_PORT = int(sys.argv[2])
      DST_HOST = str(sys.argv[3])
      DST_PORT  = int(sys.argv[4])
      LOG_MODE = 1  #hard coding raw here regardless of what -arg is entered
    print("Port logger -raw mode enabled: srcPort= host= dstPort=")
    if len(sys.argv) == 4:
      PROXY_PORT = int(sys.argv[1])
      DST_HOST = str(sys.argv[2])
      DST_PORT  = int(sys.argv[3])
      LOG_MODE = 0  

    start_proxy_server()
    
  else:
    print("wrong number of program arguments")

def start_proxy_server():

  server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
  server_sock.bind((PROXY_HOST,PROXY_PORT))
  server_sock.listen(5)
  print("Waiting for client(s) to connect at: "+PROXY_HOST+":"+str(PROXY_PORT))
  
  while True:

    clientSock, addr = server_sock.accept()
    client_ip = str(addr[0])
    client_port = str(addr[1])
    client_ip,client_port = str(addr[0]),str(addr[1])
    print(client_ip + ':' + client_port + ' has connected')
    Thread(target=client_connect, args=(clientSock,client_ip,client_port)).start()

def client_connect(clientSock,client_ip,client_port):

  #get client data from clientSock TCP connection
  buff_size = 4096
  client_request = clientSock.recv(buff_size)

  try:
    dest_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest_server_socket.connect((DST_HOST,DST_PORT))
    mode = 0
    log_request(client_request,mode)

    #Send original client request to server for response
    dest_server_socket.send(client_request)
  
    while True:
      
      #get response from remote server
      response_data = dest_server_socket.recv(buff_size)

      #if server responded with response, log, and 
      #relay this back to the connected client
      if len(response_data) > 0:
        
        mode = 1
        clientSock.send(response_data)
        # THIS will show the response from server, but can't 
        # figure out how to extract the header only!
        #log_request(response_data,mode)

      else:

        print("client disconnected from server")
        break

    #close connection because no data was sent from server
    dest_server_socket.close()
    clientSock.close()

  except:
    #print("some error raised")
    #print("Closing all connections")
    clientSock.close()
    dest_server_socket.close()
    sys.exit(1)

def log_request(client_request,mode):
  
  global LOG_MODE
  
  if mode == 0: #client request
    symbol = "--->"
  if mode == 1: #server response
    symbol = "<---"

  if LOG_MODE == 1: #RAW MODE
    print(symbol)
    print(client_request)
    # HOW TO EXTRACT JUST THE TCP HEADER????????????? grrrr

  elif LOG_MODE == 2:
    print("Port logger -strip mode not implemented")
  elif LOG_MODE == 3:
    print("Port logger -hex mode not implemented")
  elif LOG_MODE == 4:
    print("Port logger -AutoN mode not implemented")

if __name__ == "__main__":
  start()

  




