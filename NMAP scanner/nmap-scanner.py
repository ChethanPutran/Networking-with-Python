import nmap
from pprint import pprint

while True:
    #User menu
    print("\nWhat you want to do?\n\
        1.Get detailed info about a device\n\
        2.Scan the network for open ports\n\
        3.Exit the applicaton\n" )

    user_choice = input("\nEnter your option :")

    #Handling user option
    if user_choice == '1':
        #Initializing the port scanner
        mynmap = nmap.PortScanner()

        #Asking the user for IP Address to scan
        ip = input("\nPlease enter IP Address to scan :")
        print("\nThis may take couple of minutes...\n")

        #Scanning the device (output is dictionary format)
        scan = mynmap.scan(ip, '1-1024', '-v -sS -sV -O -A -e ens4')
        #pprint(scan)

        #Parsing the relevant information from the scan result
        #Header containing the IP Address
        print("\n______________HOST{}________________".format(ip))
        print("\n\nGeneral Info : \n")
        
        #MAC Address
        try:
            mac = scan['scan'][ip]['address']['mac']
            print("-> MAC Address : {}\n".format(mac))

        except KeyError:
            pass

        #Operating System
        os =scan['scan'][ip]['osmatch'][0]['name']
        print("-> Operating Sysyem : {}\n".format(os))

        #Device Uptime
        uptime =scan['scan'][ip]['uptime']['lastboot']
        print("Device uptime : {}\n".format(uptime))

        #Port states
        print("\n___PORTS___\N\N")

        for port in list(scan['scan'][ip]['tcp'].items()):
            print("-> {} | {} | {}".format(port[0], port[1]['name'], port[1]['state']))

        print("\n\nOther Info\n\n")

        #NMAP command used for Scanning
        print("-> NMAP command : {}".format(scan['nmap']['command_line']))    

        #NMAP version
        version = str(mynmap.nmap_version()[0])+"."+str(mynmap.nmap_version()[1])
        print("-> NMAP version : {}".format(version))

        #Time elapsed
        print("-> Time elapsed : {}".format(scan['nmap']['scanstates']['elapsed'] + 'seconds'))

        #Timestamp
        print("-> Time of scan : {}".format(scan['nmap']['scanstates']['timestr']))

        continue
    elif user_choice == '2':
        #Initializing the port scanner
        mynmap = nmap.PortScanner()


        print("\nThis may take couple of minutes...\n")

        #Scanning the device (output is dictionary format)
        scan = mynmap.scan(ports='1-1024',arguments='-sS -e ens3 -iL /home/osboxes/Destop/ip.txt')
        #pprint(scan)

        for device in scan['scan']:
            print("\nPorts open on {}:".format(device))
            for port in scan['scan'][device]['tcp'].items():
                if port[1]['state'] == 'open':
                    print("-> "+str(port[0])+" | "+port[1]['name'])

        continue
    
    elif user_choice == '3':
        print("\nExiting progran...\n")
        break
        
    else:
        print("\nInvalid input.Try again!\n")           
           

        


