import os.path
import sys


def user_pass_passer():
    usernames = []
    passwords = []
   
    #Checking username/password file
    #Prompting user for input -(username/password file)

    user_file = input("\n Enter UserFile path and name (Eg.C:\\User\\Dell\\Desktop\\userfile.txt) : ")

    #Verifying the validity of username/password file
    if os.path.isfile(user_file) == True:
        print(("\n Username/Password file is valid :)\n"))
    else:
        print("\n File {} does not exist :( Please check and try again.\n".format(user_file))
        sys.exit()

    #Opening user/password file for data extraction
    selected_user_file = open(user_file, 'r')

    #Extracting usernames and passwords from the file
    for line in selected_user_file:
        usernames.append(line.split(',')[0].rstrip("\n"))
        passwords.append(line.split(',')[1].rstrip("\n"))
    
    
    #Closing the user file
    selected_user_file.close()     
    return [usernames,passwords]  
  