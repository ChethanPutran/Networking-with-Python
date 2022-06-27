import sys
import os.path
import time
import re
import paramiko  #(pip install paramiko)
import threading
import datetime
import subprocess
from graph import Graphh


def user_pass_cmd_passer():
    usernames = []
    passwords = []
   
    #Checking username/password file
    #Prompting user for input -(username/password file)

    user_file = input("\n Enter UserFile path and name (Eg.C:\\User\\Dell\\Desktop\\userfile.txt) : ")

    #Verifying the validity of username/password file
    if os.path.isfile(user_file) == True:
        print(("\n Username/Password file is valid :)\n"))
    else:
        print("\n File {} does not exist :( Please check and try again.\n".format(user_file))
        sys.exit()

    #Opening user/password file for data extraction
    selected_user_file = open(user_file, 'r')

    #Extracting usernames and passwords from the file
    for line in selected_user_file:
        usernames.append(line.split(',')[0].rstrip("\n"))
        passwords.append(line.split(',')[1].rstrip("\n"))
    
    
    #Closing the user file
    selected_user_file.close()

    #Checking command file
    #Prompting user for input -(command file)
    cmd_file = input("\n Enter CommandFile path and name for router (Eg.C:\\User\\Dell\\Desktop\\cmdfile.txt) : ")

    #Verifying the validity of command file
    if os.path.isfile(cmd_file) == True:
        print(("\n Command file is valid :)\n"))
    else:
        print("\n File {} does not exist :( Please check and try again.\n".format(cmd_file))
        sys.exit()  
    return [usernames,passwords,cmd_file]  
  

def ip_file_validate():
    # Prompting user for input
    # (Note: Each Ip Address Must be written in new line in ip file)
    ip_file = input("\n Enter the IPFile path and name (Eg.C:\\User\\Dell\\Desktop\\myfile.txt) : ")

    # Checking if the file exists
    if os.path.isfile(ip_file) == True:
        print(("\n IP file is valid :)\n"))
    else:
        print("\n File {} does not exist :( Please check and try again.\n".format(ip_file))
        sys.exit()

    # Opening user selected file for reading (IP address file)
    selected_ip_file = open(ip_file, 'r', encoding='utf-8')

    # Starting from the beginning of the file
    selected_ip_file.seek(0)

    # Reading each line (IP address) in the file
    ip_list = selected_ip_file.readlines()

    # Closing ther file
    selected_ip_file.close()
   
    return ip_list


def ip_add_validate(ip_list):
    for ip in ip_list:
        ip = ip.rstrip("\n")
        octet_list = ip.split('.')
      
        # Checking for validity ,so that it does not belong the following:
        # 1.Looopback:127.0.0.0-127.255.255.255
        # 2.Multicast:224.0.0.0-239.255.255.255
        # 3.Broadcast:255.255.255.255
        # 4.Link-Local:169.254.0.0-169.254.255.255
        # 5.Reserved for future use:240.0.0.0-255.255.255.254
        if (len(octet_list) == 4) and (1 <= int(octet_list[0]) <= 223)\
            and (int(octet_list[0]) != 127) and (int(octet_list[0]) != 169 or int(octet_list[1]) != 254) and ((0 <= int(octet_list[1]) <= 255) and (0 <= int(octet_list[2]) <= 255) and (0 <= int(octet_list[3]) <= 255)):
            continue

        else:
            print(
                "\n There is an invalid IP address in the file: {} :(\n".format(ip))
            sys.exit()


#Checking IP reachabity
def ip_reach(ip_list):

    for ip in ip_list:
        ip = ip.rstrip("\n")

        #Pinging to the client to check reachabity with 2 packets(For mac: -c 2)
        #Supressing any output or errors from the ping command
        ping_reply = subprocess.call('ping %s /n 3' % (ip), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        #Checking echo reply   
        if ping_reply == 0:
            print("\n {} is reachable :) \n".format(ip))
            continue
        else:
            print("\n {} is not reachable :( Check connectivity and try again.".format(ip))
            sys.exit()


#Open SSHv2 connection to the device
def ssh_connection(ip,username,password,cmd_file):
    #Creating SSH connection
    
    try:
        #Loging into the device
        session = paramiko.SSHClient()

        #For testing purposes,this allows auto-accepting unknown host keeys
        #Do not use in the production! The default would be RejectPlolicy
        session.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        #Connect to the device using username and passsword
        session.connect(ip.rstrip("\n"), username=username, password=password)
        
        #Start an interactive shell session on the router
        connection = session.invoke_shell()

        #Entering user privilege mode and
        #Setting terminal length for entire output (For:disable pagination)
        connection.send("enable\n")
        connection.send("terminal length 0\n")
        time.sleep(1)

        
        #Entering global config mode
        connection.send("\n")
        connection.send("configure terminal\n")
        time.sleep(1)

        #Opening command file for Reading
        selected_cmd_file = open(cmd_file,'r')

        #Starting from the beginning of the file
        selected_cmd_file.seek(0)

        #Writing each line in the command file to the device
        for each_line in selected_cmd_file:
            connection.send(each_line+'\n')
            time.sleep(2)


        #Closing the command file
        selected_cmd_file.close()

        #Checking command output for IOS syntax errors
        router_output = connection.recv(65535)

        if re.search(b"% Invalid input", router_output):
            print("\n Something went wrong on the device {} :(\n".format(ip))
            show_op = input("Show more?(y/n) : ")
            if (show_op.lower() == 'y'):
                router_output = str(router_output)
                router_output = router_output.split("\\r\\n")
                for i, item in enumerate(router_output):
                    if i>8:
                        print(item+"\n")
        
        else:
            print("\nDone for device {}. Data sent to file at {}\n".format(ip,str(datetime.datetime.now())))


        #Searching for the CPU utilization value within the output of "show processes top once"    
        cpu = re.search(b"%Cpu\(s\):(\s)+(.+?)(\s)+us,",router_output)

        #Exttracting the second group ,which matches the actual  value of the CPU utilization
        #and decoding the bytes object to produce a string (encode to the popular utf-8 format)
        utilization = cpu.group(2).decode('utf-8')

        #Open the CPU utilization text file and appending the results
        with open(".\\cpu.txt", 'a') as file:
            # file.write("{},{}\n".format(str(datetime.datetime.now()),utilization))
            file.write("{}\n".format(utilization))

        #Closing the connection
        session.close()    

    except paramiko.AuthenticationException:
        print("\n Invalid username or password :(.\n Please check the username/password file or device configuration.")
        print("Closing the program.... Bye .....")


#Saving the list of IP addresses in ip.txt to a variable
ip_list = ip_file_validate()

#Verifying the validity of each IP address in the list
try:
    ip_add_validate(ip_list)
except KeyboardInterrupt:
    print("\n\n Program aborted by user. Exiting...\n")
    sys.exit()

#Verifying the reachability of each IP address in the list
try:
    ip_reach(ip_list)
except KeyboardInterrupt:
    print("\n\n Program aborted by user. Exiting...\n")
    sys.exit()
#Extracting the usernames and passwords from the users/passwords file 
try:
    passer = user_pass_cmd_passer()
except KeyboardInterrupt:
    print("\n\n Program aborted by user. Exiting...\n")
    sys.exit()

jobs = [1, 2]
threads = []
graph = Graphh()

#passer=[usernames,passwords,cmd_file]
try:
    while True:
        for job in jobs:
            if job == 1:
                for i,ip in enumerate(ip_list):
                    th = threading.Thread(target=ssh_connection,args=(ip,passer[0][i],passer[1][i],passer[2]))#args is a tuple with single element
                    th.start()
                    threads.append(th)
            
        #Instruct the program to wait until all thread has finished
        for th in threads:
            th.join()
    time.sleep(2)
except Exception as e:
    print(e)    
      


################################ END ##################################  



