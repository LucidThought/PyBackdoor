import socket
import getopt
import sys

# get opts makes it easier to parse the program arguments
# backdoor.py -l -p 2017 -c     creates the backdoor listen server
# python backdoor.py -h localhost -p 2017
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

    myopts, args = getopt.getopt(sys.argv[1:], "l:h:p:c")
    # o == option
    # a == argument
    for o, a in myopts:
        if o == '-l':
            LISTEN = True  # set the listen (server) flag
        elif o == '-h':
            HOST = a
        elif o == '-p':
            PORT = a
        elif o == '-c':
            SHELL_COMMAND = a

    # if true, run in netcat listen mode (server).
    if LISTEN == True:
        HOST = '0.0.0.0'
        server_listen()

        # if false, run in netcat client mode
        # if LISTEN == False:

def server_listen():
    #Create a simple waiting loop for clients to connect to
    #the server
    server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
    server.bind(( TARGET, PORT))
    server.listen(1)  ## only need to allow 1 client connection

    while True:
        clientSocket, addr = server.accept()

if __name__ == '__main__':
    start()
