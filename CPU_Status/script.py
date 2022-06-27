import subprocess
import logging
import re
import sys


try:
    from scapy.all import *
except ImportError:
    print("Scapy is not installed in your system.\n")    
    print("Try using : pip3 install scapy\n")
    sys.exit()
#This will suppress all messeges that have a lover level of seriousness than error messeges
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)    
logging.getLogger("scapy.interactive").setLevel(logging.ERROR)    
logging.getLogger("scapy.loading").setLevel(logging.ERROR)    

#Setting the checkIPaddr parameter to False
conf.checkIPaddr = False

#Reading allowed DHCP servers from an external file
with open("dhcp.txt") as f:
    allowed_dhcp_servers = f.read()

#Listing all network interfaces on the ubuntu host
host_if = subprocess.run("ip link", shell=True, stdout=subprocess.PIPE)

#Extracting the interfaces name from the output stored above
interfaces = re.findall(r"\d:\s(.+?):\s", str(host_if))


try:
    #Detecting Rogue DHCP servers per interface (except loopback interface)
    for interface in interfaces:
        if interface != 'lo':
            #Getting the hardware address
            mac_add = get_if_raw_hwaddr(interface)[1]
            # print(mac_add)

            #Creating DHCP discover packet
            dhcp_discover = Ether(dst = 'ff:ff:ff:ff:ff:ff') / IP(src = '0.0.0.0', dst = '255.255.255.255') / UDP(sport = 68, dport = 67) / BOOTP(chaddr = mac_add) / DHCP(options = [('message-type', 'discover'), 'end'])
            
            #Sending the Dicover Packet and accepting multiple answers for the same Discover Packet
            ans, unans = srp(dhcp_discover, multi=True, iface=interface, timeout=5, verbose=0)
            # print(ans)
            # print(unans)

            #Defining a dictionary to store mac-ip pairs
            mac_ip_pair = {}

            for pair in ans:
                mac_ip_pair[pair[1][Ether].src] = pair[1][IP].src

            if ans:
                #Printing the results
                print("\n --> The following DHCP servers found on the {} LAN: \n".format(interface))

                for mac, ip in mac_ip_pair.items():
                    if ip in allowed_dhcp_servers:
                        print("OK! IP Address : {},MAC Address : {}\n".format(ip,mac))
                    else:
                        print("ROGUE! IP Address : {},MAC Address : {}\n".format(ip,mac))    

            else:
                print("\n --> No active DHCP servers found on the {} LAN\n".format(interface))        
        else:
            pass

except KeyboardInterrupt:
    print("\nProgram aborted by the user!!! Exiting...")
    sys.exit()       