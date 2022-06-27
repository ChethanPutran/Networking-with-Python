import sys
import subprocess


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
