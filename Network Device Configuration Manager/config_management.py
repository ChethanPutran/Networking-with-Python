

import difflib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler  #(pip3 install netmiko)


#Extracting the IP Address of the device to be monitored
ip_file = open("ipaddres.text", 'r')
ip=ip_file.readlines()[0].lstrip('\n')


#Defining the device type for running netmiko
device_type = 'arista_eos'

#Defining the username and password for running netmiko
username = 'admin'
password = 'admin1'

#Defining the command to send 
command = 'show running'

#Definig email parameters
fromAddr = 'caarts.tech@gmail.com'
toAddr = '4nm19me025@nmamit.in'

#MIME(Multipurpus Internet Mail Extension) is used to send Non-Ascii characters like images ,video etc.
msg = MIMEMultipart()
msg['From'] = fromAddr
msg['To'] = toAddr
mag['Subject'] = 'Daily Configuration Management Report'


def sendEmail(fromAddr, toAddr, msg):   
    #Sending email via Gmail's SMTP server on port 587
    server = smtplib.SMTP('smtp.gmail.com',587)

    #SMTP connection is in TLS(Transport Layer Security) mode.All SMTP commands that follow will be encrypted
    server.starttls()

    #Logging in to Gmail and sending the e-Mail
    server.login('caarts.tech','Arts_Are_Beautiful@595')
    server.sendmail(fromAddr, toAddr, msg.as_string())

    #Ending session or logging out
    server.quit()


#Connecting to the device via ssh
session = ConnectHandler(device_type=device_type,ip=ip,username=username,password=password,global_delay_factor=3)


#Entering the enable mode
enable = session.enable()

#Sending the command and storing the output
output = session.send(command)

#Defining the file from previous day and present day for comparision
old_device_config = "config_files/"+ip+'_'+(datetime.date.today()-datetime.timedelta(days=1)).isoformat()
new_device_config_fname = "config_files/"+ip+ '_' + datetime.date.today().isoformat()

#Writing the command output to a file for present day
with open(new_device_config_fname, 'w') as new_device_config:
    new_device_config.write(output+'\n')

# Extracting the difference between old and new file in HTML format    
with open(old_device_config, 'r') as old_file, open(new_device_config_fname, 'r') as new_file:
    difference = difflib.HtmlDiff().make_file(fromlines=old_file.readlines(), tolines=new_file.readlines(), fromdesc='Yesterday', todesc='Today')


#Attaching the differences to be send as HTML format
msg.attach(MIMEText(difference,'html'))

#Sending email
sendEmail(fromAddr, toAddr, msg)

