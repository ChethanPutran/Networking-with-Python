from netmiko import ConnectHandler
from datetime import datetime
from pprint import pprint
import re

#Defining device IP Addresses
with open('ip.txt') as f:
    ip_addrs = f.readlines() 

#pprint(ip_addrs)

#Defining device parameters

cisko1={
    "device type":"cisko_ios",
    "host":ip_addrs[0].rstrip('\n'),
    "username":"admin",
    "password":"admin1"
} 

cisko2={
    "device type":"cisko_ios",
    "host":ip_addrs[1].rstrip('\n'),
    "username":"admin",
    "password":"admin2"
} 

cisko3={
    "device type":"cisko_ios",
    "host":ip_addrs[2].rstrip('\n'),
    "username":"admin",
    "password":"admin3"
} 

#Connecting to the device via SSH
switches=[cisko1,cisko2,cisko3]

#Creating empty list for starting output 
output_list = []

for switch in switches:
    connection = ConnectHandler(**switch)
    syslog_output = connection.send_command("show logging last 1 day")
    output_list.append(syslog_output)

##pprint(output_list)

#Creating an empty dictionary for device output mapping 
output_map = {}

#Searching for LLDP Neighbors-related log messages and extracting it.
for output in output_list:
    #Extracting hostnames
    hostname_regex = re.findall(r".+\d\d:\d\d:\d\d\s(.+?)\s",output) 
    host_name = hostname_regex[0]

    #Extracting the LLDP Neighbor information
    output_lines = output.split('\n')
    
    #Creating an empty list to store LLDP Neighbor-related lines
    lldp_lines = []
    
    for line in output_lines:
        #Finding line with LLDP and neighbor words in it by ignoring case
        if re.findall(r"LLDP",line,re.I) and re.search(r"neighbor",line,re.I):
            lldp_lines.append(line+"\n")
 
#Creating the hostname:output mapping per device    
output_map[host_name] = lldp_lines

#Creating perodical LLDP text report and saving to local folder
#Naming the file using current timestamp

with open("lldp_{}".format(datetime.now().strftime("%Y-%m-%d-%H-%M")),'w') as f:
    for entry in output_map.items():
        f.write(entry[0]+"\n")
        f.writelines(entry[1])
        f.write("\n\n")

     
