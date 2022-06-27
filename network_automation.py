############### Network Tak Automation -by CHETHAN ##################

#Import all neccessary functions
import sys
from ip_file_validity import ip_file_validate
from ip_add_validity import ip_add_validate
from ip_add_reachability import ip_reach
from user_and_pass_passer import user_pass_passer
from ssh_connectivity import ssh_connection
from create_thread import create_thread


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
    credentials = user_pass_passer()
except KeyboardInterrupt:
    print("\n\n Program aborted by user. Exiting...\n")
    sys.exit()

#Calling threads creation function for one or multiple SSH connections
create_thread(ip_list,credentials,ssh_connection)

################################ END ##################################  


