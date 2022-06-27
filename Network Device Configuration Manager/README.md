############### Program to Automate Network Task (For linux) #################

1.Install neccesary modules and packages
$ sudo apt-get install libssl-dev
$ sudo pip3 insatll netmiko
2.Enter the IP Address of the device in ipaddress.txt file
3.Run the conf.bat file(*Only for the first time)

###### Creating a Schedule for Sending E-mails on a Daily Basis #######
$ sudo crontab -e
Select a text editor to edit
Add the folllowing:-
(m h dom mon dow command)
(time/step)
0 5 * * * cd /home/username && sudo python3 config_management.py
(Executes the program everyday @5am)
*You can change the prefferable time for you
