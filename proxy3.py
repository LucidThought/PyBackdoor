# HOW TO USE
# throw open a terminal, run program as follows
# ex
# $python proxy3.py -raw 2001 www.ucalgary.ca 80
# open web browser, and set proxy to localhost port:2001
# now all GET requests are transmitted via proxy to
# web browsr

#!/usr/bin/python

import socket
import getopt
import sys
import string
import thread
#ex

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

  SRC_HOST = 'localhost' #localhost
  arg_length = len(sys.argv)

  if arg_length == 5:
    log_command = str(sys.argv[1])
    #create function to set the log mode based on cmd line arg
    LOG_MODE = 0
    SRC_PORT = int(sys.argv[2])
    DST_HOST = str(sys.argv[3])
    DST_PORT  = int(sys.argv[4])
    print(SRC_PORT)
    print(SRC_HOST)
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
    clientSock, addr = server_sock.accept()
    clientSock.settimeout(60) #times out after 60 seconds
    clients_connected += 1 #increase counter
    print("Client unknowingly connected to the 666 proxy")
    # need a print statement to show the clients IP address

    thread.start_new_thread(proxy666Listener, (clientSock,addr))
    

def proxy666Listener(clientSock,addr):

  print("Port logger running: srcPort= host= dstPort=")
  buff_size = 4096
  request_data = clientSock.recv(buff_size)

  try:

    print("connection to web server: " + DST_HOST)
    dest_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest_socket.connect((DST_HOST,DST_PORT))
    request_data_array = request_data.split('n')
    print(request_data_array[0])
    # NEED log function to output request data to log (aka console)

  except:
    print("debug error: cannot open that socket.")
    if clientSock:
      clientSock.close()
    print("proxy 6666 closing program and kill connection")
    sys.exit(1)

  dest_socket.send(request_data)
  
  while True:
    response_data = dest_socket.recv(buff_size)

    if response_data:
      # NEED log function to output request data to log (aka console)
      clientSock.send(response_data)
    else:
      print("client disconnected from server")
      break
  dest_socket.close()
  clientSock.close()


if __name__ == "__main__":
  start()

  




