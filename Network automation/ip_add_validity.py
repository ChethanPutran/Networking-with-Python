import sys

# Checking octets


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
        if (len(octet_list) == 4) and (1 <= int(octet_list[0]) <= 223) and (int(octet_list[0]) != 127) and (int(octet_list[0]) != 169 or int(octet_list[1]) != 254) and ((0 <= int(octet_list[1]) <= 255) and (0 <= int(octet_list[2]) <= 255) and (0 <= int(octet_list[3]) <= 255)):
            continue

        else:
            print(
                "\n There is an invalid IP address in the file: {} :(\n".format(ip))
            sys.exit()
