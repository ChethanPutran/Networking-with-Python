########################## Subnet Calculator -By CHETHAN ###################


import random
import sys


def binary_to_ip(binary_num):
    ip_octets = []

    #Slicing the 32 bits binary to 4 sets of 8bits
    for bit in range(0, 32, 8):
        ip_octet = binary_num[bit: bit + 8]
        ip_octets.append(ip_octet)
        

    ip_address_sep = []
    #Converting binary octates to integer numbers
    for octet in ip_octets:
        ip_address_sep.append(str(int(octet, 2)))

    #Adding '.' between two integers to get IP Address Form
    ip_address = ".".join(ip_address_sep)

    return [ip_address,ip_address_sep]

def ip_add_validate():  
    while True:
        ip = input("\nEnter an IP Address: ")
        octet_list = ip.split('.')
        # Checking for validity ,so that it does not belong the following:
        # 1.Looopback:127.0.0.0-127.255.255.255
        # 2.Multicast:224.0.0.0-239.255.255.255
        # 3.Broadcast:255.255.255.255
        # 4.Link-Local:169.254.0.0-169.254.255.255
        # 5.Reserved for future use:240.0.0.0-255.255.255.254
        if (len(octet_list) == 4) and (1 <= int(octet_list[0]) <= 223) and (int(octet_list[0]) != 127) \
            and (int(octet_list[0]) != 169 or int(octet_list[1]) != 254) and ((0 <= int(octet_list[1]) <= 255) \
            and (0 <= int(octet_list[2]) <= 255) and (0 <= int(octet_list[3]) <= 255)):
            return octet_list
            break

        else:
            print("\n The IP Address is invalid!! Try again...\n")
            continue


def mask_validator():
    masks = [255, 254, 252, 248, 240, 224, 192, 128, 0]
    while True:
        subnet_mask = input("\nEnter the Subnet Mask: ")

        #Checking octets
        mask_octets = subnet_mask.split('.')

        #Checking for validity
        if (len(mask_octets) == 4) and (int(mask_octets[0]) == 255) and (int(mask_octets[1]) in masks) \
            and (int(mask_octets[2]) in masks) and (int(mask_octets[2]) in masks) and \
            (int(mask_octets[3]) in masks) and ((int(mask_octets[1])) >= \
            (int(mask_octets[2])) >= (int(mask_octets[3]))):
            return mask_octets
            break
        else:
            print("\n The subnet mask is INVALID! Please Try Again!\n")
            continue    


def subnet_calculator():
    try:
        #Checking IP Address validity
        octet_list=ip_add_validate()
        
        # Checking for subnet mask validity 
        mask_octets=mask_validator()

        #######################  Subnet calculations   #####################
        mask_octets_binary = []

        for octet in mask_octets:
            #Converting each octets to binary and stripping 0b from the front
            binary_octet = bin(int(octet)).lstrip('0b')
            #Converted binary is appended with exactly 8 digits(Eg:2-->00000010)
            mask_octets_binary.append(binary_octet.zfill(8))

        #Joining converted binary octets together to obtain binary mask
        binary_mask = "".join(mask_octets_binary)
        #(Example:-255.255.255.9-->11111111.1111111.11111111.00000000)

        #Counting the host bits i.e no of zeros
        no_of_zeros = binary_mask.count('0')
        no_of_ones = 32 - no_of_zeros  #Since IP Address is a 32 bit number
        no_of_hosts = abs(2 ** no_of_zeros - 2)  #Formula to calculate number of hosts in a network

        ################### Wildcard Mask ###############################
        
        wildcard_octets = []
        #Calculates the wildcard mask
        for octet in mask_octets:
            wildcard_octet = 255 - int(octet)
            wildcard_octets.append(str(wildcard_octet))

        #Getting valid IP foramt 
        wildcard_mask = '.'.join(wildcard_octets)


        #Convert IP to binary stripping
        ip_octets_binary = []

        for octet in octet_list:
            binary_octet = bin(int(octet)).lstrip('0b')
            ip_octets_binary.append(binary_octet.zfill(8))

        #Joining binary octets to get binary IP Address
        binary_ip = ''.join(ip_octets_binary)


        #Calculating the Network Address
        network_add_binary = binary_ip[:no_of_ones] + '0'* no_of_zeros

        #Calculating the Broadcast Address
        broadcast_add_binary = binary_ip[:no_of_ones] + '1' * no_of_zeros
        
        #Converting bimary to valid IP format
        network_ip_address= binary_to_ip(network_add_binary)
        broadcast_ip_address = binary_to_ip(broadcast_add_binary)

        ############### Priting The Results ###############
    
        print("\nNetwork Address is : %s" % network_ip_address[0])    
        print("\nBroadcast Address is : %s" % broadcast_ip_address[0])    
        print("\nNumber of valid hosts per subnet is : %s" % no_of_hosts)    
        print("\nWildcard Mask is : %s" % wildcard_mask)    
        print("\nMask Bits : %s\n" % no_of_ones)  

        #################   Generating Random IP Address  ###############
        while True:
            generate = input('\nGenerate random IP Address from this subnet? (Y/N)')

            if generate.lower() == 'y':
                generated_ip =[] 

                #Obtain available IP address in range ,based on the difference between octets of
                #broadcast address and network address(Algorithm to calculate the ramdom IP Adress)
                for idx_bst, oct_bst in enumerate(broadcast_ip_address[1]):
                    for idx_net, oct_net in enumerate(network_ip_address[1]):
                        if idx_net == idx_bst:
                            if oct_bst == oct_net:
                                #Adds identical octets to the generated ip list
                                generated_ip.append(oct_bst)
                            else:
                                #Generate random number between network octet and broadcast octet(when the octets are different)
                                generated_ip.append(str(random.randint(int(oct_net), int(oct_bst))))

                random_ip = '.'.join(generated_ip)
                print("\nRandom IP Address is : %s \n" % random_ip)
                continue               
            else:
                print("\n Exiting.... Bye!!!")
                break
    except KeyboardInterrupt:
        print("\n Program aborted by the user!!! Exiting.....")
        sys.exit()
        
subnet_calculator()        