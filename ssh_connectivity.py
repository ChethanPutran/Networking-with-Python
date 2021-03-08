import sys
import os.path
import time
import re
import paramiko  #(pip install paramiko)

#Open SSHv2 connection to the device
def ssh_connection(ip,username,password):
    #Creating SSH connection
    try:
        #Checking command file
        #Prompting user for input -(command file)

        cmd_file = input("\n Enter CommandFile path and name for router {} (Eg.C:\\User\\Dell\\Desktop\\cmdfile.txt) : ".format(ip))

        #Verifying the validity of command file
        if os.path.isfile(cmd_file) == True:
            print(("\n Command file is valid :)\n"))
        else:
            print("\n File {} does not exist :( Please check and try again.\n".format(cmd_file))
            sys.exit()

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
                opt = str(router_output).split('\r\n')
                for line in opt:
                    print(line+"\n")
        
        print("\nDone for device {} :)\n".format(ip))
        router_output = str(router_output)
        router_output = router_output.split("\r\n")
        print(router_output)

        #Closing the connection
        session.close()    

    except paramiko.AuthenticationException:
        print("\n Invalid username or password :(.\n Please check the username/password file or device configuration.")
        print("Closing the program.... Bye .....")
        


