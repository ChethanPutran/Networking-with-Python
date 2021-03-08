import os.path
import sys

# Checking IP address file and content validity


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
