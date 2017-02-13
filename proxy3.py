#!/usr/bin/python3

# CPSC 526 - Assignment 2
# Written By: Justin Berry, Andrew Lata

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
from functools import reduce
from datetime import datetime
from binascii import hexlify

PROXY_PORT = 0
DST_PORT = 0
PROXY_HOST = ''
DST_HOST = ''
LOG_MODE = 0


# void main ( no arg )
# Description:
# main of program, is responsible for reading command line arguments and starting
# the proxy server.
def main():

  global PROXY_PORT
  global DST_PORT
  global PROXY_HOST
  global DST_HOST
  global LOG_MODE
  global LOG_COMMAND

  PROXY_HOST = 'localhost' #server_host, always localhost.

  if len(sys.argv) == 5 or len(sys.argv) == 4:

    if len(sys.argv) == 5:
      LOG_COMMAND = str(sys.argv[1])
      set_log_mode(LOG_COMMAND)
      PROXY_PORT = int(sys.argv[2])
      DST_HOST = str(sys.argv[3])
      DST_PORT  = int(sys.argv[4])
    
    if len(sys.argv) == 4:
      PROXY_PORT = int(sys.argv[1])
      DST_HOST = str(sys.argv[2])
      DST_PORT  = int(sys.argv[3])
      LOG_MODE = 0  

    print("Port logger running: srcPort="+str(PROXY_PORT)+ " host="+DST_HOST+" dstPort="+str(DST_PORT)+"\n")
    start_proxy_server()
    
  else:
    print("wrong number of program arguments")

# void set_log_mode( arg1=string )
# Description:
# helper function to set the proxy log mode.
def set_log_mode(LOG_COMMAND):
  global LOG_MODE
  if LOG_COMMAND == "-raw":
    mode = 1
    print("-raw mode logging enabled")
  elif LOG_COMMAND == "-strip":
    mode = 2
    print("-strip mode logging enabled")
  elif LOG_COMMAND == "-hex":
    mode = 3
    print("-hex mode logging enabled")
  elif LOG_COMMAND.startswith("-auto"):
    mode = 4
    print("-autoN mode logging enabled")
  else:
    mode = 1
    print("Invalid Input for mode, default at -raw")
  LOG_MODE = mode	

# void start_proxy_server( no args )
# Description:
# Starts the TCP proxy server, and listens for incoming socket connections.
# For each client that connects, spawn a new client socket connection and client_connect
# thread using that client socket connection. Listens for an unlimited # of connections
def start_proxy_server():

  server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
  server_sock.bind((PROXY_HOST,PROXY_PORT))
  server_sock.listen(10)
  #print( "Waiting for client(s) to connect at: "+PROXY_HOST+":"+str(PROXY_PORT) )
  
  while True:

    clientSock, addr = server_sock.accept()
    client_ip = str(addr[0])
    client_port = str(addr[1])
    client_ip,client_port = str(addr[0]),str(addr[1])
    print("New Connection: " + datetime.now().isoformat(sep=' ') + " From " + client_ip + ':' + client_port)
    Thread( target=proxy_listener, args=(clientSock,client_ip,client_port) ).start()

# void proxy_listener( arg1=socket,arg2=string,arg3=int )
# Description:
# This is the primary listener function for the proxy server, listens for TCP data
# packets from the client socket, and TCP data packets from the dest server socket
# and logs the data for each respective TCP packet.
def proxy_listener(clientSock,client_ip,client_port):

  dest_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  dest_server_socket.connect((DST_HOST,DST_PORT))
  
  client_request = b'' #this specifies byte string
  server_response = b'' #this specifies byte string

  while True:

    client_request = get_data(clientSock) #returns a byte string
    symbol = 0

    if len(client_request) > 0: #if client_request has data
      symbol = 1
      log_request( client_request, symbol ) 
      dest_server_socket.send(client_request)

    server_response = get_data(dest_server_socket) #returns a byte string

    if len(server_response) > 0: # if server_response has data
      symbol = 2
 
      log_request( client_request , symbol )
      clientSock.send(server_response)

    if not len(server_response) or not len(client_request):
     clientSock.close()
     dest_server_socket.close()
     break

# void log_request( arg1=byteString of data)
# Description:
# Helper function that logs packets to and from the proxy server.
def log_request(data,mode):
  
  global LOG_MODE
  global LOG_COMMAND

  if mode == 0: #no data
    symbol = "" 
  if mode == 1: #client request
    symbol = "---> "
  if mode == 2: #server response
    symbol = "<--- "

  if LOG_MODE == 1: #RAW MODE
    # OLD BUG HERE, If you don't "ignore" for error code argument
      # an unicode error will crash the program if ignore is left out
      # server responds with some unicode (byte characters) characters that can't be
      # converted into string. You may need to change this when printing out in 
      # the other modes? https://docs.python.org/3/howto/unicode.html very useful page
      # only if your converting from UNI Code (byte string) to string
    symbol_format = str.replace(str(data,'utf-8',"ignore"), "\n", ("\n{}".format(symbol)))
    print(symbol + symbol_format)

  elif LOG_MODE == 2:
    # isprintable() include characters in the ascii range 32-127
    # New line characters are, officially, not printable
    # UPDATE: See http://web.itu.edu.tr/sgunduz/courses/mikroisl/ascii.html for details on non-printable characters
    symbol_format = str(data,'utf-8',"ignore")
    symbol_format = ''.join(c if c.isprintable() else '.' for c in symbol_format)
    print(symbol + "\n" + symbol_format)
    # FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

  elif LOG_MODE == 3:
    symbol_format = str(data, 'utf-8', "ignore")
    # print(reduce(lambda x,y:x+y+" ", map(lambda p:("0" if ord(p)<=0xf else "")+hex(ord(p))[2:],symbol_format), ""))
    print(hexdump(symbol_format))

  elif LOG_MODE == 4:
    numBytes = LOG_COMMAND[5:]
    counter = 0
    if (numBytes.isdigit()==False):
      print("Invalid number of bytes for -autoN, defaulting to 16-byte lines")
      numBytes = 16
    packet = str(data,'utf-8',"ignore")
    symbol_format = []
    for i in range(0,len(packet),int(numBytes)):
      line = packet[i:i+int(numBytes)]
      text = symbol
      for c in line:
        if not isinstance(c, int):
          c = ord(c)
        if 0x20 <= c < 0x7F:
          text += chr(c)
        else:
          text += hex(c).replace('0x','\\')
      text += '\n'
      symbol_format.append(text)
    print(''.join(symbol_format))
        
# String hexdump (arg1=network data in utf-8)      
# Description:
# This funtion compiles the output for each captured packet in the hexdump format
# Each packet is indexed individually in the leftmost column
# This function was adapted from https://gist.github.com/ImmortalPC/c340564823f283fe530b
def hexdump(src):
  dump = []
  length = 16
  separate = '.'

  for i in range(0, len(src), length):
    subSrc = src[i:i+length]
    hexvals = ''
    for h in range(0,len(subSrc)):
      if h == length/2:
        hexvals += ' '
      h = subSrc[h]
      if not isinstance(h, int):
        h = ord(h)
      h = hex(h).replace('0x','')
      if len(h) == 1:
        h = '0'+h
      hexvals += h+' '
    hexvals = hexvals.strip(' ')
    text = ''
    for c in subSrc:
      if not isinstance(c, int):
        c = ord(c)
      if 0x20 <= c < 0x7F:
        text += chr(c)
      else:
        text += separate
    dump.append(('%08X:  %-'+str(length*(2+1)+1)+'s  |%s|') % (i, hexvals, text))

  return '\n'.join(dump)

# client_connect( arg1=socket), returns byte String (Unicode)
# Description:
# helper function, recieves data from either client socket, or dest server, keeps
# looping until the socket has no more data to recieve, sometimes has more then 4096
def get_data(socket):

    buff_size = 4096
    time_out = 5
    data_buffer = b''
    socket.settimeout(5)
    try:
        while True:
            data = socket.recv(4096)
            if not data:
                break
            data_buffer += data
    except:
        pass
    return data_buffer

if __name__ == "__main__":
  main()






