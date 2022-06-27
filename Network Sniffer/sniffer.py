##################### Network sniffer -By CHETHAN ###################

import logging
import subprocess
import sys
from datetime import datetime
import pandas as pd
import os


#This will supress all messages that have a lower level of seriousness than error messages,whie
#running or loading Scapy

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
logging.getLogger("scapy.interactive").setLevel(logging.ERROR)
logging.getLogger("scapy.loading").setLevel(logging.ERROR)

#Recommended way of import(official document)
try:
    from scapy.all import *
except ImportError:
    print("Scapy pakage for Python is not installed on your system")
    sys.exit()


protocols = ["arp","bootp","icmp"]

def ask_no_packets():
    #Asking for the number of packets to sniff
    pkt_to_sniff = input("Enter the number of packets to capture(0 is infinity) : ")

    if int(pkt_to_sniff) != 0:
        print("\n The program will caputre packets %d packets.\n" % int(pkt_to_sniff))
    elif int(pkt_to_sniff) == 0:
        print("\nThe program will capture packets untill the timeout expires.\n")
    return pkt_to_sniff
 
def exit_program():
    print("\nProgram aborted by the user! Exiting ....")
    sys.exit()


def ask_time_interval():
    #Asking the user for the time interval to sniff
    time_to_sniff = input("Enter the number of seconds to run the capture : ")

    if int(time_to_sniff) != 0:
        print("\nThe program will capture packets for %d seconds.\n" % int(time_to_sniff))
    return time_to_sniff

def put_promiscuous_mode(network_interface):
    #Setting the network interface in promiscuous mode(to accept all traffic )
    try:
        subprocess.call(["ifconfig",network_interface,"promisc"],stdout=None,stderr=None,shell=False)
    except:
        print("\nFailed to configure interface as promiscuous.\n")
        ans = input("Retry(Y/N) : ")
        if ans.upper() == 'Y':
            put_promiscuous_mode(network_interface)
        else:
            sys.exit()    
    else:
        #Executes if the try clause does not raise an exception
        print("\nInterface {} was set to PROMISCUOUS mode.\n".format(network_interface))


def ask_protocol_to_sniff():
    #Asking the user for protocol to be filter
    while True:
        try:
            print("1.Enter the protocol to filter \n")
            print("2.Show available protocols :\n")
            choice = input("Enter your choice : ")

            try:
                if int(choice) == 1:
                    protocol_to_sniff = input("\nEnter the protocol : ")
                    protocol_to_sniff = protocol_to_sniff.lower()
                    
                    if protocol_to_sniff == '0':
                        print("\nThe program will capture packets for all packets.\n")
                        return protocol_to_sniff
                    elif protocol_to_sniff in protocols:
                        print("\nThe program will capture packets for {} packets.\n".format(protocol_to_sniff.upper()))
                        return protocol_to_sniff
                    else:
                        print("\nInvalid protocol!! Try again...")
                        continue
                elif int(choice) == 2:
                    for i, protocol in enumerate(protocols):
                        print(str(i+1)+" "+ protocol.upper()+"\n")
                    print(str(i+2)+" "+"0(for all)")
                else:
                    print("\nInvalid Choice!!\n")
            except:
                print("\nInvalid Choice!!")
        except KeyboardInterrupt:
            exit_program()
            



#Function to extract the parameters from the packet and log each packet to the log file
class FileGenerator:
    def __init__(self,f1):
        self.f1=f1
        
    def packet_log(self,packet):
        global protocol_to_sniff

        f1=self.f1

        #Getting the current timestamp
        now = datetime.now()
 
        #Writing the packet information to the log file
        if protocol_to_sniff == "0":
            f1.write(str(now) + ",ALL," + packet[0].src + "," + packet[0].dst + "\n")
        else:
            f1.write(str(now) + "," + protocol_to_sniff.upper() + "," + packet[0].src + "," + packet[0].dst + "\n")
    
            
        
#Always use "sudo scapy" in Linux 
print("\nMake sure to run this program as RO0T!\n")

#Asking the user for some parametrs:interface on which to sniff, the number of packets
# to sniff , the time interval to sniff, the protocol

#The interface to input
network_interface = input("Enter the interface on which to run the sniffer (Eg.eth0) : ")
    
#Setting the network interface in promiscuous mode(to accept all traffic )
put_promiscuous_mode(network_interface)

#Asking for the number of packets to sniff
pkt_to_sniff = ask_no_packets()

#Asking the user for the time interval to sniff
time_to_sniff = ask_time_interval()

protocol_to_sniff=ask_protocol_to_sniff()

        
while True:
    #Asking the user to enter the name and path of the log file to be created
    file_path = input("Please enter a name and path of the file to be created (Eg:C:\\User\\Dell\\Desktop\\mylog.txt) : ")

    try:
        #Creating a text file if it does not exist or opening for packet logging 
        sniffer_log = open(file_path, 'a')
    except:
        print("\nFile Path Invalid!! Try again..\n")
        continue
    else:
        break    
 

f1 = open("temp.csv", 'a')
f1.write("Time,Protocol,SMAC,DMAC\n")
            

func = FileGenerator(f1)    
print("\nStarting the capture...\n")

try:
    #Running the sniffing process
    sniff(iface=network_interface,count=int(pkt_to_sniff),timeout=int(time_to_sniff),prn=func.packet_log)
except KeyboardInterrupt:
    exit_program()
else:
    a = pd.read_csv('temp.csv',sep=",")
    print(a, file=sniffer_log)
    f1.close()
    os.remove("temp.csv")

#Priting the closing message
print("\nPlease check the %s file to see the captured packets.\n" % file_path)           

#Closing the log file
sniffer_log.close()

############################ END ##################################